from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
import pendulum
import sqlparse

from tecton_proto.common import aggregation_function_pb2 as afpb
from tecton_proto.data.feature_service_pb2 import FeatureSetItem
from tecton_proto.data.feature_view_pb2 import FeatureView as FeatureViewProto
from tecton_proto.data.feature_view_pb2 import NewTemporalAggregate
from tecton_spark import time_utils
from tecton_spark.id_helper import IdHelper
from tecton_spark.schema import Schema
from tecton_spark.snowflake.pipeline_helper import pipeline_to_df_with_input
from tecton_spark.snowflake.pipeline_helper import pipeline_to_df_with_mock_input
from tecton_spark.snowflake.pipeline_helper import pipeline_to_sql_string
from tecton_spark.snowflake.snowflake_utils import get_snowflake_feature_view_name
from tecton_spark.snowflake.templates_utils import load_template

TEMP_SPINE_TABLE_NAME = "_TEMP_SPINE_TABLE_FROM_DF"

HISTORICAL_FEATURES_TEMPLATE = None
MATERIALIZATION_TILE_TEMPLATE = None
MATERIALIZATION_TEMPLATE = None
TIME_LIMIT_TEMPLATE = None

# TODO(TEC-6204): Last and LastN are not currently supported
#
# Map of proto function type -> set of (output column prefix, snowflake function name)
AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: {("SUM", "SUM")},
    afpb.AGGREGATION_FUNCTION_MIN: {("MIN", "MIN")},
    afpb.AGGREGATION_FUNCTION_MAX: {("MAX", "MAX")},
    afpb.AGGREGATION_FUNCTION_COUNT: {("COUNT", "COUNT")},
    afpb.AGGREGATION_FUNCTION_MEAN: {("COUNT", "COUNT"), ("MEAN", "AVG")},
}


def _load_template():
    # TODO: Do this at module loading time once we sort out including the templates in the public SDK build
    global HISTORICAL_FEATURES_TEMPLATE
    if not HISTORICAL_FEATURES_TEMPLATE:
        HISTORICAL_FEATURES_TEMPLATE = load_template("historical_features.sql.j2")
    global MATERIALIZATION_TILE_TEMPLATE
    if not MATERIALIZATION_TILE_TEMPLATE:
        MATERIALIZATION_TILE_TEMPLATE = load_template("materialization_tile.sql.j2")
    global MATERIALIZATION_TEMPLATE
    if not MATERIALIZATION_TEMPLATE:
        MATERIALIZATION_TEMPLATE = load_template("materialization.sql.j2")
    global TIME_LIMIT_TEMPLATE
    if not TIME_LIMIT_TEMPLATE:
        TIME_LIMIT_TEMPLATE = load_template("time_limit.sql.j2")


def _format_sql(sql_str: str) -> str:
    return sqlparse.format(sql_str, reindent=True, keyword_case="upper")


@dataclass
class _FeatureSetItemInput:
    """A simplified version of FeatureSetItem which is passed to the SQL template."""

    name: str
    timestamp_key: str
    join_keys: Dict[str, str]
    features: List[str]
    sql: str
    aggregation: Optional[NewTemporalAggregate]
    ttl_seconds: Optional[int]


def get_historical_features(
    spine: Union[pandas.DataFrame, str, "snowflake.snowpark.DataFrame"],
    session: "snowflake.snowpark.Session",
    feature_set_items: List[FeatureSetItem],
    timestamp_key: str,
    include_feature_view_timestamp_columns: bool = False,
    # Whether to use the registered snowflake view for features.
    from_registered_view: bool = True,
) -> "snowflake.snowpark.DataFrame":
    from snowflake.snowpark import DataFrame

    _load_template()
    if include_feature_view_timestamp_columns:
        raise NotImplementedError()
    if isinstance(spine, str):
        spine_sql = spine
    elif isinstance(spine, DataFrame):
        _create_temp_table_for_df(session=session, df=spine, table_name=TEMP_SPINE_TABLE_NAME)
        spine.write.mode("append").saveAsTable(TEMP_SPINE_TABLE_NAME)
        spine_sql = f"SELECT * FROM {TEMP_SPINE_TABLE_NAME}"
    elif isinstance(spine, pandas.DataFrame):
        # TODO: Use write_pandas once snowflake support to create a temp table with it.
        spine_df = session.createDataFrame(spine)

        _create_temp_table_for_df(session=session, df=spine_df, table_name=TEMP_SPINE_TABLE_NAME)
        spine_df.write.mode("append").saveAsTable(TEMP_SPINE_TABLE_NAME)
        spine_sql = f"SELECT * FROM {TEMP_SPINE_TABLE_NAME}"

    input_items = []
    for item in feature_set_items:
        feature_view = item.enrichments.feature_view
        # Change the feature view name if it's for internal udf use.
        if item.namespace.startswith("_udf_internal"):
            name = item.namespace.upper()
        else:
            name = feature_view.fco_metadata.name

        if not feature_view.HasField("on_demand_feature_view"):
            join_keys = {k.package_column_name: k.spine_column_name for k in item.join_configuration_items}
            features = [
                col.name
                for col in feature_view.schemas.view_schema.columns
                if col.name not in (list(join_keys.keys()) + [feature_view.timestamp_key])
            ]
            if len(feature_view.online_serving_index.join_keys) != len(feature_view.join_keys):
                raise ValueError("SQL string does not support wildcard")
            if from_registered_view:
                source = f"SELECT * FROM {get_snowflake_feature_view_name(feature_view.fco_metadata.name)}"
            else:
                source = pipeline_to_sql_string(
                    pipeline=feature_view.pipeline,
                    data_sources=feature_view.enrichments.virtual_data_sources,
                    transformations=feature_view.enrichments.transformations,
                )
            sql_str = TIME_LIMIT_TEMPLATE.render(
                source=source,
                timestamp_key=feature_view.timestamp_key,
                # Apply time limit from feature_start_time
                start_time=feature_view.materialization_params.start_timestamp.ToDatetime(),
            )
            input_items.append(
                _FeatureSetItemInput(
                    name=name,
                    timestamp_key=feature_view.timestamp_key,
                    join_keys=join_keys,
                    features=features,
                    sql=sql_str,
                    aggregation=(
                        feature_view.temporal_aggregate if feature_view.HasField("temporal_aggregate") else None
                    ),
                    ttl_seconds=(
                        int(time_utils.proto_to_duration(feature_view.temporal.serving_ttl).total_seconds())
                        if feature_view.HasField("temporal")
                        else None
                    ),
                )
            )
    sql_str = HISTORICAL_FEATURES_TEMPLATE.render(
        feature_set_items=input_items,
        spine_timestamp_key=timestamp_key,
        spine_sql=spine_sql,
        include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
    )
    output_df = session.sql(sql_str)

    # Apply ODFV to the spine
    for item in feature_set_items:
        feature_view = item.enrichments.feature_view
        if feature_view.HasField("on_demand_feature_view"):
            output_df = pipeline_to_df_with_input(
                session=session,
                input_df=output_df,
                pipeline=feature_view.pipeline,
                transformations=feature_view.enrichments.transformations,
                output_schema=Schema(feature_view.schemas.view_schema).to_spark(),
                name=feature_view.fco_metadata.name,
                fv_id=IdHelper.to_string(feature_view.feature_view_id),
            )
    columns_to_drop = [column for column in output_df.columns if "_UDF_INTERNAL_" in column]
    if len(columns_to_drop) > 0:
        output_df = output_df.drop(*columns_to_drop)
    return output_df


def _create_temp_table_for_df(
    session: "snowflake.snowpark.Session", table_name: str, df: "snowflake.snowpark.DataFrame"
):
    """
    Create a temporary table for the given dataframe.
    """
    # TODO: This implementation uses some internal snowflake APIs, we should replace this when they
    # have official support for our use case.
    from snowflake.snowpark._internal.analyzer.analyzer_package import AnalyzerPackage
    from snowflake.snowpark._internal.analyzer.sf_attribute import Attribute

    attributes = [Attribute(f.name, f.datatype, f.nullable) for f in df.schema.fields]
    pkg = AnalyzerPackage()
    schema_string = pkg.attribute_to_schema_string(attributes)
    create_tmp_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {table_name} ({schema_string})"
    session.sql(create_tmp_table_sql).collect()


def run_batch(
    session: "snowflake.snowpark.Session",
    feature_view: FeatureViewProto,
    # start is inclusive and end is exclusive
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
) -> "snowflake.snowpark.DataFrame":
    # Smart default feature_start_time and feature_end_time if unset.
    if feature_end_time is None:
        feature_end_time = pendulum.now()
    if feature_start_time is None:
        schedule_interval = time_utils.proto_to_duration(feature_view.materialization_params.schedule_interval)
        feature_start_time = feature_end_time - schedule_interval
    sql_str = get_materialization_sql_str(
        feature_view=feature_view,
        time_limits=pendulum.period(feature_start_time, feature_end_time),
    )
    df = session.sql(sql_str)
    return df


def run_ondemand(
    session: "snowflake.snowpark.Session", feature_view: FeatureViewProto, mock_inputs: Dict[str, pandas.DataFrame]
) -> "snowflake.snowpark.DataFrame":
    return pipeline_to_df_with_mock_input(
        session=session,
        pipeline=feature_view.pipeline,
        transformations=feature_view.enrichments.transformations,
        output_schema=Schema(feature_view.schemas.view_schema).to_spark(),
        name=feature_view.fco_metadata.name,
        fv_id=IdHelper.to_string(feature_view.feature_view_id),
        mock_inputs=mock_inputs,
    )


def get_materialization_sql_str(
    feature_view: FeatureViewProto,
    # start is inclusive and end is exclusive
    time_limits: pendulum.Period,
    destination: str = None,
    storage_integration: Optional[str] = None,
) -> str:
    _load_template()
    source = get_snowflake_feature_view_name(feature_view.fco_metadata.name)
    if feature_view.HasField("temporal_aggregate"):
        aggregations = defaultdict(set)
        for feature in feature_view.temporal_aggregate.features:
            aggregate_function = AGGREGATION_PLANS[feature.function]
            if not aggregate_function:
                raise ValueError(f"Unsupported aggregation function {feature.function} in snowflake pipeline")
            aggregations[feature.input_feature_name].update(aggregate_function)

        # Need to order the functions for deterministic results.
        for key, value in aggregations.items():
            aggregations[key] = sorted(value)

        source = MATERIALIZATION_TILE_TEMPLATE.render(
            source=source,
            join_keys=list(feature_view.join_keys),
            aggregations=aggregations,
            slide_interval=feature_view.temporal_aggregate.slide_interval,
            timestamp_key=feature_view.timestamp_key,
        )
    return _format_sql(
        MATERIALIZATION_TEMPLATE.render(
            source=source,
            materialization_schema=feature_view.schemas.materialization_schema,
            timestamp_key=feature_view.timestamp_key,
            start_time=time_limits.start,
            end_time=time_limits.end,
            destination=destination,
            storage_integration=storage_integration,
        )
    )


def get_features_sql_str_for_spine(
    feature_set_items: List[FeatureSetItem],
    timestamp_key: str,
    spine_sql: str = None,
    include_feature_view_timestamp_columns: bool = False,
) -> str:
    """
    Get a SQL string to fetch features given the spine and feature set.
    spine_sql and spine_table_name cannot be both empty.

    :param feature_set_items: FeatureSetItems for the features.
    :param timestamp_key: Name of the time column in the spine.
    :param spine_sql: SQL str to get the spine.
    :param include_feature_view_timestamp_columns: (Optional) Include timestamp columns for every individual feature definitions.
    :return: A SQL string that can be used to fetch features.
    """
    _load_template()
    if include_feature_view_timestamp_columns:
        raise NotImplementedError()

    input_items = []
    for item in feature_set_items:
        feature_view = item.enrichments.feature_view
        join_keys = {k.package_column_name: k.spine_column_name for k in item.join_configuration_items}
        features = [
            col.name
            for col in feature_view.schemas.view_schema.columns
            if col.name not in (list(join_keys.keys()) + [feature_view.timestamp_key])
        ]
        if len(feature_view.online_serving_index.join_keys) != len(feature_view.join_keys):
            raise ValueError("SQL string does not support wildcard")
        sql_str = TIME_LIMIT_TEMPLATE.render(
            source=pipeline_to_sql_string(
                pipeline=feature_view.pipeline,
                data_sources=feature_view.enrichments.virtual_data_sources,
                transformations=feature_view.enrichments.transformations,
            ),
            timestamp_key=feature_view.timestamp_key,
            # Apply time limit from feature_start_time
            start_time=feature_view.materialization_params.start_timestamp.ToDatetime(),
        )
        input_items.append(
            _FeatureSetItemInput(
                name=feature_view.fco_metadata.name,
                timestamp_key=feature_view.timestamp_key,
                join_keys=join_keys,
                features=features,
                sql=sql_str,
                aggregation=(feature_view.temporal_aggregate if feature_view.HasField("temporal_aggregate") else None),
                ttl_seconds=(
                    int(time_utils.proto_to_duration(feature_view.temporal.serving_ttl).total_seconds())
                    if feature_view.HasField("temporal")
                    else None
                ),
            )
        )
    return _format_sql(
        HISTORICAL_FEATURES_TEMPLATE.render(
            feature_set_items=input_items,
            spine_timestamp_key=timestamp_key,
            spine_sql=spine_sql,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
        )
    )
