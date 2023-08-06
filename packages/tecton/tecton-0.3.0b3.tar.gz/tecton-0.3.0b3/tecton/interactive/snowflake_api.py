from datetime import datetime
from typing import Dict
from typing import Optional
from typing import Union

import pandas
import pendulum

from tecton.interactive.data_frame import DataFrame
from tecton.interactive.feature_set_config import FeatureSetConfig
from tecton.interactive.run_api import validate_ondemand_mock_inputs_keys
from tecton.snowflake_context import SnowflakeContext
from tecton_proto.data.feature_view_pb2 import FeatureView as FeatureViewProto
from tecton_spark.snowflake import sql_helper


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, DataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: bool = False,
    save: bool = False,
    save_as: Optional[str] = None,
    start_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    end_time: Optional[Union[pendulum.DateTime, datetime]] = None,
    entities: Optional[Union["snowflake.snowpark.DataFrame", pandas.DataFrame, DataFrame]] = None,
) -> DataFrame:
    if spine is None:
        raise ValueError("Spine is required for snowflake")

    if timestamp_key is None:
        raise ValueError("timestamp_key must be specified with Snowflake compute")

    # TODO(TEC-6991): Dataset doesn't really work with snowflake as it has spark dependency.
    # Need to rewrite it with snowflake context or remove this param for snowflake.
    if save or save_as is not None:
        raise NotImplementedError("Save is not supported for Snowflake")

    # TODO(TEC-6996): Implement this
    if entities is not None:
        raise NotImplementedError("Entities is not supported for Snowflake")

    # TODO(TEC-7010): Implement this
    if start_time is not None or end_time is not None:
        raise NotImplementedError("start_time and end_time are not supported for Snowflake")

    df = DataFrame._create_with_snowflake(
        sql_helper.get_historical_features(
            spine=spine,
            session=SnowflakeContext.get_instance().get_session(),
            timestamp_key=timestamp_key,
            feature_set_items=[
                config.to_proto() for config in feature_set_config._get_feature_definitions_and_join_configs()
            ],
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
        )
    )
    return df


def run_batch(
    fv_proto: FeatureViewProto,
    feature_start_time: Optional[Union[pendulum.DateTime, datetime]],
    feature_end_time: Optional[Union[pendulum.DateTime, datetime]],
    mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]],
    aggregation_level: str = None,
) -> DataFrame:
    # TODO(TEC-7053): Implement this
    if len(mock_inputs) > 0:
        raise NotImplementedError("mock_inputs is not supported for Snowflake")
    # TODO(TEC-7054): Implement this
    if aggregation_level is not None:
        raise NotImplementedError("aggregation_level is not supported for Snowflake")
    # TODO(TEC-7060): Implement this
    if fv_proto.HasField("temporal_aggregate"):
        raise NotImplementedError("BatchWindowAggregateFeatureView is not supported for Snowflake")

    df = DataFrame._create_with_snowflake(
        sql_helper.run_batch(
            session=SnowflakeContext.get_instance().get_session(),
            feature_view=fv_proto,
            feature_start_time=feature_start_time,
            feature_end_time=feature_end_time,
        )
    )
    return df


def run_ondemand(
    fv_proto: FeatureViewProto, mock_inputs: Dict[str, Union[pandas.DataFrame, DataFrame]]
) -> "tecton.interactive.data_frame.DataFrame":
    # Convert all inputs to pandas dataframes
    for key in mock_inputs:
        if isinstance(mock_inputs[key], DataFrame):
            mock_inputs[key] = mock_inputs[key].toPandas()

    # Validate that all the mock_inputs matchs with FV inputs, and that num rows match across all mock_inputs.
    validate_ondemand_mock_inputs_keys(mock_inputs, fv_proto)

    # Execute Pandas pipeline to get output DataFrame.
    return DataFrame._create_with_snowflake(
        sql_helper.run_ondemand(
            session=SnowflakeContext.get_instance().get_session(),
            feature_view=fv_proto,
            mock_inputs=mock_inputs,
        )
    )
