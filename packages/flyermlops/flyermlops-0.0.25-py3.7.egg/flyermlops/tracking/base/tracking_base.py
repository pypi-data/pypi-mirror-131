from abc import ABC, abstractmethod

from ..tracking_utils import (
    get_or_create_table,
    set_tracking_id,
    log_registry_values,
    pull_registry_values,
)
from flyermlops.data.connector import (
    DataConnector,
    TeradataHelper,
    PostgresHelper,
    AthenaHelper,
)
from .sql_base import (
    SqlDataRegistrySchema,
    SqlFlightArtifactRegistrySchema,
    SqlFlightRegistrySchema,
    SqlModelRegistrySchema,
    SqlMetricRegistrySchema,
    SqlParamRegistrySchema,
    SqlDataMetricSchema,
)
import datetime
import time
from typing import Optional, List


class TrackingBase(ABC):
    def __init__(
        self,
        project_name: str,
        host: str = None,
        user: str = None,
        password: str = None,
        port: int = None,
        database: str = None,
        flight_tracking_id: str = None,
        tracking_id: str = None,
        code_link: str = None,
        tracking_uri: str = None,
        part_of_flight: bool = None,
        tracking_schema: str = None,
        tracker_type: str = None,
        s3_bucket: str = None,
        **kwargs,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.project_name = project_name
        self.flight_tracking_id = flight_tracking_id
        self.tracking_id = tracking_id
        self.code_link = code_link
        self.tracking_uri = tracking_uri
        self.part_of_flight = part_of_flight
        self.tracking_schema = tracking_schema
        self.tracker_type = tracker_type
        self.s3_bucket = s3_bucket

        self.registries = {}
        self.registries["flight"] = SqlFlightRegistrySchema

        if tracker_type == "data":
            self.registries["tracker"] = SqlDataRegistrySchema
            self.registries["metric"] = SqlDataMetricSchema

        elif tracker_type == "model":
            self.registries["tracker"] = SqlModelRegistrySchema
            self.registries["metric"] = SqlMetricRegistrySchema
            self.registries["param"] = SqlParamRegistrySchema
            self.registries["data"] = SqlDataRegistrySchema

        elif tracker_type == "flight":
            self.registries["tracker"] = SqlFlightArtifactRegistrySchema

    @abstractmethod
    def set_tracking_connection(
        self, engine="postgres", flight_tracking_id=None, tracking_id=None,
    ):
        """ Establishes connection to postgres database and schema.
            Creates 

        Args:
            uri: Postgres connection uri.
            tracking_schema: Schema where tracking client writes data to.
            pipeline: Whether data tracking object is part of pipeline (True or False).
            If True, the pipeline registery is searched for an active pipeline associated with the project.
            If an active pipeline is not found, a new pipeline tracking id is created.
        """
        if engine == "postgres":
            data_sess = DataConnector(engine).client
            if self.tracking_uri is not None:
                self.tracking_engine = data_sess(uri=self.tracking_uri).set_connection(
                    connector="sqlalchemy"
                )
            else:
                self.tracking_engine = data_sess(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    database=self.database,
                ).set_connection(connector="sqlalchemy")

        # Set postgres schema and metric schema
        for registry, schema in self.registries.items():

            # Set tracking schema
            schema.__table__.schema = self.tracking_schema

            # create table
            get_or_create_table(self.tracking_engine, schema)

        if flight_tracking_id is None:
            if self.part_of_flight:
                self.set_flight_tracking_id()

        if tracking_id is None:
            if "flight" not in self.registries["tracker"].__name__.lower():
                self.set_tracking_id()

    def set_tracking_id(self):
        self.tracking_id = set_tracking_id(
            project_name=self.project_name,
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            flight_registry_schema=self.registries["flight"],
            flight_tracking_id=self.flight_tracking_id,
            code_link=self.code_link,
        )

    def set_flight_tracking_id(self):
        # if pipeline
        self.flight_tracking_id = set_tracking_id(
            project_name=self.project_name,
            engine=self.tracking_engine,
            registry_schema=self.registries["flight"],
        )

    def set_data_connector(self, style, **kwargs):
        if style == "athena":
            self.athena_client = AthenaHelper(**kwargs)

        elif style == "teradata":
            self.teradata_client = TeradataHelper(**kwargs)

        elif style == "postgres":
            self.postgres_client = PostgresHelper(**kwargs)

    def _set_storage_location(self):

        # Set buckets
        if self.flight_tracking_id is not None:
            main_tracking_id = self.flight_tracking_id
            if self.tracking_id is not None:
                second_tracking_id = self.tracking_id
        else:
            main_tracking_id = self.tracking_id
            second_tracking_id = None

        if self.s3_bucket is not None:
            bucket_prefix = None
            if self.project_name is not None:
                bucket_prefix = f"projects/{self.project_name}"
            if main_tracking_id is not None:
                if bucket_prefix is not None:
                    bucket_prefix = (
                        f"{bucket_prefix}/{main_tracking_id}/{self.tracker_type}"
                    )
                else:
                    bucket_prefix = f"{main_tracking_id}/{self.tracker_type}"

            elif main_tracking_id is None:
                if bucket_prefix is not None:
                    bucket_prefix = f"{bucket_prefix}/{self.tracker_type}"
                else:
                    bucket_prefix = f"{self.tracker_type}"

            if second_tracking_id is not None:
                bucket_prefix = f"{bucket_prefix}/{second_tracking_id}"

        self.bucket_prefix = bucket_prefix

        if self.log_data:
            log_registry_values(
                engine=self.tracking_engine,
                registry_schema=self.registries["tracker"],
                data={"s3_location": f"s3://{self.s3_bucket}/{self.bucket_prefix}"},
                tracking_id=self.tracking_id,
            )

    def load_data(
        self,
        tracking_path: Optional[str] = None,
        name: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ):
        """
        Reads a parquet file from a specified s3 tracking path.
        A name argument can be given to specify the folder in which to read data from
        in the tracking path.

        Args:
            tracking_path: S3 object path associated with a given tracking id
            name: Specific folder within the tracking path to read from. Optional
        """

        self.set_data_connector(style="athena", kwarg_dict={"bucket": self.s3_bucket})
        if tracking_path is None:
            # get data path from tracking id
            query_result = pull_registry_values(
                engine=self.tracking_engine,
                registry_schema=self.registries["data"],
                columns=["s3_location"],
                tracking_id=self.data_tracking_id,
            )
            path = query_result["s3_location"][0]

        else:
            path = f"s3://{tracking_path}"

        if name is not None:
            path = f"{path}/{name}/"
        else:
            path = f"{path}/"

        df = self.athena_client.read_parquet(path, columns)
        return df

