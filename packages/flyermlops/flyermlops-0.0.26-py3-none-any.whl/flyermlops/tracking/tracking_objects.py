from flyermlops.ml_pipelines.flight_utils import write_landing
from .. import exceptions
from ..tracking.base.tracking_base import TrackingBase

from ..tracking import tracking_utils
from ..data.connector import PostgresHelper, AthenaHelper, TeradataHelper
from ..drift import data_drift_utils as drift_utils
import pandas as pd
from typing import Iterable, List, Dict, Optional
import datetime
import time
import joblib
import boto3
from botocore.exceptions import ClientError


class FlightTracker(TrackingBase):
    def __init__(
        self,
        project_name=None,
        tracking_uri=None,
        tracking_schema=None,
        part_of_flight: bool = False,
        flight_tracking_id: str = None,
        *args,
        **kwargs,
    ):

        super().__init__(
            project_name=project_name,
            tracking_uri=tracking_uri,
            tracking_schema=tracking_schema,
            part_of_flight=part_of_flight,
            flight_tracking_id=flight_tracking_id,
            tracker_type="flight",
            *args,
            **kwargs,
        )

    def start_flight(self, engine: str = "postgres"):
        self.set_tracking_connection(engine)

    def set_tracking_connection(self, engine):
        super().set_tracking_connection(
            engine=engine,
            flight_tracking_id=self.flight_tracking_id,
            tracking_id=self.tracking_id,
        )

        return self.flight_tracking_id

    def end_flight(self):
        data = {"in_flight": 0}
        self.log_to_registry(data=data, tracking_id=self.flight_tracking_id)

    def log_artifacts(
        self, key, value, tag=None,
    ):

        data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": time.time(),
            "flight_tracking_id": self.flight_tracking_id,
            "project_name": self.project_name,
            "key": key,
            "value": value,
            "tag": tag,
        }

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
        )

    def log_to_registry(self, data: dict, tracking_id):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["flight"],
            data=data,
            tracking_id=tracking_id,
        )


class DataTracker(TrackingBase):
    def __init__(
        self,
        project_name=None,
        tracking_uri=None,
        tracking_schema=None,
        s3_bucket=None,
        part_of_flight: bool = False,
        log_data: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            project_name=project_name,
            tracking_uri=tracking_uri,
            tracking_schema=tracking_schema,
            part_of_flight=part_of_flight,
            s3_bucket=s3_bucket,
            tracker_type="data",
            *args,
            **kwargs,
        )

        self.log_data = log_data

        if log_data:
            self.set_tracking_connection()

    def set_tracking_connection(self, engine="postgres"):
        # Set tracking ids
        super().set_tracking_connection(
            engine=engine, flight_tracking_id=self.flight_tracking_id
        )

    def _set_storage_location(self):
        return super()._set_storage_location()

    def set_data_connector(self, style, kwarg_dict):
        super().set_data_connector(style, **kwarg_dict)

    def log_features(self, feature_dict: dict):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        if type(feature_dict) is not dict:
            raise exceptions.NotofTypeDictionary(
                "A dictionary of feature names and types is expected"
            )

        data = {"feature_info": feature_dict}
        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
            tracking_id=self.tracking_id,
        )

    def log_metrics(self, data: dict, tag: str = None):
        """Logs data metrics to data metrics registry
        
        Args:
            data: Dictionary of key, values ({'key': value}).
            tag: Optional tag to append to data dictionary.
        """

        values = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "project_name": self.project_name,
            "data_tracking_id": self.tracking_id,
        }

        for key, val in data.items():
            metrics = {
                "key": key,
                "value": val,
                "timestamp": int((time.time_ns()) / 1000000),
            }

            if tag is not None:
                metrics["tag"] = tag

            metadata = {**values, **metrics}
            tracking_utils.log_metrics(
                engine=self.tracking_engine,
                registry_schema=self.registries["metric"],
                data=metadata,
            )

    def run_drift_diagnostics(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature_mapping: dict = None,
        target_feature: str = None,
        current_label: str = "current",
        reference_label: str = "reference",
        log_data: bool = True,
        return_df: bool = False,
    ):

        """Computes drift diagnostics between reference and current data based upon column mapping
        
        Args:
            reference_data: Pandas dataframe of reference or background data to compare against.
            current_data: Pandas dataframe containing current data.
            column_mapping: Dictionary containing features (keys) and their column types.
            reference_label: Label for reference data.
            current_label: Label for current data.

        """

        # Compute feature drift
        feature_dict = {}

        if feature_mapping is None:
            feature_mapping = drift_utils.get_feature_types(dict(reference_data.dtypes))

        feature_list = feature_mapping.keys()

        # Create global model and compute feature importance
        feature_importance = drift_utils.compute_drift_feature_importance(
            reference_data,
            current_data,
            feature_list=feature_list,
            target_feature=target_feature,
        )

        if target_feature is not None:
            if not isinstance(target_feature, list):
                target_feature = [target_feature]
        else:
            target_feature = []

        for feature in [*feature_list, *target_feature]:
            feature_dict[feature] = dict.fromkeys(
                [
                    "type",
                    "intersection",
                    "missing_records",
                    "unique",
                    "reference_distribution",
                    "current_distribution",
                    "feature_importance",
                    "feature_auc",
                    "reference_label",
                    "current_label",
                    "target_feature",
                ]
            )

            feature_dict[feature]["type"] = feature_mapping[feature]

            # Subset data
            ref_data = reference_data[feature]
            cur_data = current_data[feature]

            # Create distributions and intersection between current and reference data
            results = drift_utils.compute_feature_stats(
                reference_data=ref_data,
                current_data=cur_data,
                reference_label=reference_label,
                current_label=current_label,
            )

            feature_dict[feature]["intersection"] = results["intersection"]
            feature_dict[feature]["missing_records"] = results["missing_records"]
            feature_dict[feature]["unique"] = results["unique"]

            feature_dict[feature]["feature_importance"] = feature_importance[feature][
                "feature_importance"
            ]
            feature_dict[feature]["feature_auc"] = feature_importance[feature][
                "feature_auc"
            ]

            feature_dict[feature]["reference_distribution"] = results[
                f"{reference_label}_histogram"
            ]
            feature_dict[feature]["current_distribution"] = results[
                f"{current_label}_histogram"
            ]

            feature_dict[feature]["reference_label"] = reference_label
            feature_dict[feature]["current_label"] = current_label

            if feature in target_feature:
                feature_dict[feature]["target_feature"] = 1

            else:
                feature_dict[feature]["target_feature"] = 0

        if log_data:
            dict_to_upload = {"drift_diagnostics": feature_dict}
            tracking_utils.log_registry_values(
                engine=self.tracking_engine,
                registry_schema=self.registries["tracker"],
                data=dict_to_upload,
                tracking_id=self.tracking_id,
            )

        if return_df:
            return (
                pd.DataFrame.from_dict(feature_dict, orient="index")
                .reset_index()
                .rename(columns={"index": "feature"})
            )

    def data_to_s3(
        self, data: pd.DataFrame, name: str, path_key: str = None,
    ):
        """
        Takes a pandas dataframe and writes a parquet file to s3.
        Write location: "s3://{s3_bucket}/{bucket_prefix}/{name}/".
        The S3 bucket and prefix are inferred from the instantiated Data Tracker.

        Args:
            data: Pandas dataframe to use to writing to parquet
            name: Name of specific s3 folder to write to
        """
        # Set storage location
        self._set_storage_location()
        self.set_data_connector(style="athena", kwarg_dict={"bucket": self.s3_bucket})
        save_path = f"{self.bucket_prefix}/{name}/{name}.parquet"
        self.athena_client.df_to_s3(data, save_path)

        print(f"Successfully saved data to s3://{self.s3_bucket}/{save_path}/{name}")

    def load_data(
        self,
        tracking_path: Optional[str] = None,
        name: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ):
        return super().load_data(
            tracking_path=tracking_path, name=name, columns=columns,
        )

    def log_to_registry(self, data: dict, tracking_id):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
            tracking_id=tracking_id,
        )

    def end_tracking(self):
        data = {"in_flight": 0}
        self.log_to_registry(data=data, tracking_id=self.tracking_id)


class ModelTracker(TrackingBase):
    def __init__(
        self,
        project_name=None,
        tracking_uri=None,
        tracking_schema=None,
        s3_bucket=None,
        part_of_flight: bool = False,
        log_data: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            project_name=project_name,
            tracking_uri=tracking_uri,
            tracking_schema=tracking_schema,
            part_of_flight=part_of_flight,
            s3_bucket=s3_bucket,
            tracker_type="model",
            *args,
            **kwargs,
        )

        self.log_data = log_data

        if log_data:
            self.set_tracking_connection()

        if self.flight_tracking_id is not None:
            self._get_data_tracking_id()

    def set_tracking_connection(self, engine="postgres"):
        # Set tracking ids
        super().set_tracking_connection(
            engine=engine, flight_tracking_id=self.flight_tracking_id
        )

    def set_data_connector(self, style, kwarg_dict):
        super().set_data_connector(style, **kwarg_dict)

    def _get_data_tracking_id(self):
        self.data_tracking_id = tracking_utils.set_tracking_id(
            project_name=self.project_name,
            engine=self.tracking_engine,
            registry_schema=self.registries["data"],
            flight_registry_schema=self.registries["flight"],
            flight_tracking_id=self.flight_tracking_id,
            code_link=self.code_link,
        )

        self.log_to_registry(
            {"data_tracking_id": self.data_tracking_id}, tracking_id=self.tracking_id
        )

    def _set_storage_location(self):
        return super()._set_storage_location()

    def load_data(
        self,
        tracking_path: Optional[str] = None,
        name: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ):
        return super().load_data(
            tracking_path=tracking_path, name=name, columns=columns,
        )

    def save_model(
        self, model, file_name, type_="sklearn", write_to_registry: bool = False,
    ):
        self._set_storage_location()

        if type_ == "sklearn":
            file_name = f"{file_name}.pkl"
            joblib.dump(model, file_name)

            # Upload the file
            s3 = boto3.resource("s3")
            save_path = f"{self.bucket_prefix}/{file_name}"
            try:
                s3.Bucket(self.s3_bucket).upload_file(file_name, save_path)
                print(f'Saved model to "s3://{self.s3_bucket}/{save_path}')
            except ClientError as e:
                raise e

        try:
            if write_to_registry:
                tracking_utils.write_to_s3_model_registry(
                    self.tracking_id, file_name, self.s3_bucket, self.project_name,
                )
        except Exception as e:
            raise exceptions.FailedtoUploadtoModelRegistry(
                f"""Failed to upload model to registry. {e}"""
            )

    def log_to_registry(self, data: dict, tracking_id):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
            tracking_id=tracking_id,
        )

    def end_tracking(self):
        data = {"in_flight": 0}
        self.log_to_registry(data=data, tracking_id=self.tracking_id)
