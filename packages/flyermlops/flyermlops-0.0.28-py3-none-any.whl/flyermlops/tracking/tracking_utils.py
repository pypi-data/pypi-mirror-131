from sqlalchemy import create_engine, MetaData, Table, desc, select, insert, update
from sqlalchemy.orm import sessionmaker, Session
from flyermlops.tracking.base.params import (
    FlightParams,
    Metrics,
    Params,
    FlightArtifacts,
)
import uuid
from typing import Type, Dict, Any, Callable, List
from sqlalchemy.ext.declarative import declarative_base
import datetime
import time
from re import search
from .. import exceptions
import os
from shutil import copyfile, make_archive
from botocore.exceptions import ClientError
import boto3
from pathlib import Path
from ..tracking.base.sql_base import SqlModelRegistrySchema

base = declarative_base()


def set_registry_type(registry_schema):
    schema_name = registry_schema.__name__.lower()
    # Identify schema type
    for schema_type in ["data", "model", "flight", "param", "metric"]:
        if schema_type in schema_name:
            if schema_type == "flight":
                if "artifact" in schema_name:
                    registry_type = "artifact"
                else:
                    registry_type = schema_type
            else:
                registry_type = schema_type

    return registry_type


def write_to_s3_model_registry(
    tracking_id, model_name, s3_bucket, project_name, requirements=True,
):
    model_dir = "model_dir"
    sub_dir = "model_folder"

    if not os.path.exists(model_dir):
        os.makedirs(f"{model_dir}/{sub_dir}")

    with open(f"{model_dir}/metadata.txt", "a") as out:
        out.write(f"FLIGHT_ID={tracking_id}")

    if requirements:
        parent_path = Path().resolve()
        for path in Path(parent_path).rglob("requirements.txt"):
            req_path = path.absolute()
        copyfile(req_path, f"{model_dir}/requirements.txt")

    # Copy model to directory
    copyfile(model_name, f"{model_dir}/{sub_dir}/{model_name}")

    # zip file
    make_archive(model_dir, "zip", model_dir)

    # Upload the file
    s3 = boto3.resource("s3")
    try:
        s3.Bucket(s3_bucket).upload_file(
            f"{model_dir}.zip", f"deployed-models/{project_name}/{model_dir}.zip"
        )
        print(
            f'Saved model to registry "s3://{s3_bucket}/deployed-models/{project_name}'
        )
    except ClientError as e:
        raise e
    return True


def select_sql_statement(registry_type, registry_schema):

    if registry_type == "data":
        return select(registry_schema.data_tracking_id, registry_schema.in_flight)

    elif registry_type == "model":
        return select(registry_schema.model_tracking_id, registry_schema.in_flight)

    elif registry_type == "flight":
        return select(registry_schema.flight_tracking_id, registry_schema.in_flight)


def clean_data(registry_type, data):

    if any(x in registry_type for x in ["data", "model", "flight"]):
        data = FlightParams(data).get_params()

    elif "params" in registry_type:
        data = Params(data).get_params()

    elif "metric" in registry_type:
        data = Metrics(data).get_params()

    elif "artifact" in registry_type:
        data = FlightArtifacts(data).get_params()

    return data


def update_registry_sql(
    registry_type, registry_schema, data_to_log, tracking_id,
):
    if registry_type == "data":
        sql = update(registry_schema).where(
            registry_schema.data_tracking_id == tracking_id
        )
    elif registry_type == "model":
        sql = update(registry_schema).where(
            registry_schema.model_tracking_id == tracking_id
        )
    elif registry_type == "flight":
        sql = update(registry_schema).where(
            registry_schema.flight_tracking_id == tracking_id
        )
    return sql.values(**data_to_log)


def get_or_create_table(engine, sql_schema):
    sql_schema.__table__.create(bind=engine, checkfirst=True)


def check_for_existing_record(
    project_name,
    engine,
    registry_schema,
    flight_registry_schema=None,
    flight_tracking_id=None,
):

    """Checks metadata table for an existing data or model tracking id.
    If a pipeline id is provided, the pipeline registry is checked for an existing tracking id for a pipeline.

    Args:
        project_name: Name of project
        engine: Sqlaclhemy engine.
        registry_schema: Registry schema.
        flight_registry_schema: Pipeline registry schema.
        flight_tracking_id: Optional unique id associated with a pipeline run.

    Returns:
        Returns either "None" or a data or model tracking id.
    """
    registry_type = set_registry_type(registry_schema)

    if flight_tracking_id is not None:
        sql_statement = (
            select_sql_statement(registry_type, flight_registry_schema)
            .where(flight_registry_schema.flight_tracking_id == flight_tracking_id)
            .limit(1)
        )

    else:
        sql_statement = (
            select_sql_statement(registry_type, registry_schema)
            .where(registry_schema.in_flight == True)
            .where(registry_schema.project_name == project_name)
            .limit(1)
        )

    return engine.execute(sql_statement).scalar()


def check_if_id_active(engine, tracking_id, registry_schema):
    registry_type = set_registry_type(registry_schema)

    if registry_type == "data":
        sql_statement = (
            select(registry_schema.in_flight)
            .where(registry_schema.data_tracking_id == tracking_id)
            .where(registry_schema.in_flight == True)
        )

    elif registry_type == "model":
        sql_statement = (
            select(registry_schema.in_flight)
            .where(registry_schema.model_tracking_id == tracking_id)
            .where(registry_schema.in_flight == True)
        )

    elif registry_type == "flight":
        sql_statement = (
            select(registry_schema.in_flight)
            .where(registry_schema.flight_tracking_id == tracking_id)
            .where(registry_schema.in_flight == True)
        )
    return engine.execute(sql_statement).scalar()


def set_tracking_id(
    project_name: str,
    engine: Callable,
    registry_schema: Callable,
    flight_registry_schema: Callable = None,
    flight_tracking_id: str = None,
    code_link: str = None,
) -> str or None:

    """Creates a new tracking id if there is no active id available.
    registry_schema is used to determine which tracking registry to search and record id to.
    If a pipeline id is provided, the pipeline registry is checked for an existing tracking id.

    Args:
        project_name: Name of project.
        engine: Sqlaclhemy engine.
        registry_schema: Registry schema. This table schema is used to determine which registry is searched for an active id.
        pipeline_registry_schema: Pipeline registry table schema.
        pipeline_tracking_id: Optional unique id associated with a pipeline run
        code_link: Link to code repository

    Returns:
        Returns either "None" or a tracking id.
    """

    hex_id = uuid.uuid4().hex
    id_dict = {
        "data": {"data_tracking_id": hex_id},
        "model": {"model_tracking_id": hex_id},
        "flight": {"flight_tracking_id": hex_id},
    }

    # Identify schema type
    registry_type = set_registry_type(registry_schema)

    # check for existing record first
    # if registry_type == "flight":
    existing_id = check_for_existing_record(
        project_name,
        engine,
        registry_schema,
        flight_registry_schema,
        flight_tracking_id,
    )

    if existing_id is None:
        new_id = id_dict[registry_type]

        # if flight id is not none add to flight registry
        if flight_tracking_id is not None:
            log_registry_values(
                engine, flight_registry_schema, new_id, tracking_id=flight_tracking_id,
            )

        # Add to registry
        values = {
            **new_id,
            **{
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "timestamp": time.time(),
                "project_name": project_name,
                "git_link": code_link,
                "in_flight": 1,
            },
        }

        log_registry_values(engine, registry_schema, values)

    return existing_id or new_id[f"{registry_type}_tracking_id"]


def pull_registry_values(
    engine: Callable,
    registry_schema: Type[base],
    columns: List[str],
    tracking_id: str = None,
):
    registry_type = set_registry_type(registry_schema)

    select_columns = [registry_schema.__table__.c[col] for col in columns]
    select_statement = select(select_columns)

    if registry_type == "data":
        sql_statement = select_statement.where(
            registry_schema.data_tracking_id == tracking_id
        )
    elif registry_type == "model":
        sql_statement = select_statement.where(
            registry_schema.model_tracking_id == tracking_id
        )
    elif registry_type == "flight":
        sql_statement = select_statement.where(
            registry_schema.flight_tracking_id == tracking_id
        )

    result = engine.execute(sql_statement).mappings().all()

    result_dict = {
        key: [dict_.get(key) for dict_ in result] for key in set().union(*result)
    }

    return result_dict


def log_registry_values(
    engine: Callable,
    registry_schema: Type[base],
    data: Dict[str, Any],
    tracking_id: str = None,
) -> None:

    """
    Logs values to registry table. Sql_schema is used to determine which registry to write to.
    Function defaults to insert statements unless a tracking id is provided, which then defaults to an update.
    """
    registry_type = set_registry_type(registry_schema)
    data_to_log = clean_data(registry_type, data)

    # id is only provided for updates
    if tracking_id is None:
        engine.execute(registry_schema.__table__.insert(data_to_log))

    else:
        sql_statement = update_registry_sql(
            registry_type, registry_schema, data_to_log, tracking_id,
        )
        result = engine.execute(sql_statement)
        result.close()


def log_metric(
    engine: Callable,
    registry_schema: Type[base],
    metric_name: str,
    value: any,
    tracking_id: str,
    existing_metrics: dict = None,
) -> None:

    if existing_metrics is not None:
        new_data = {"metrics": {**existing_metrics, **{metric_name: value}}}

    else:
        new_data = {"metrics": {metric_name: value}}

    data_to_log = clean_data(registry_type="FlightParams", data=new_data)

    sql_statement = (
        update(registry_schema)
        .where(registry_schema.model_tracking_id == tracking_id)
        .values(**data_to_log)
    )

    result = engine.execute(sql_statement)


def log_metrics(
    engine: Callable,
    registry_schema: Type[base],
    metrics: dict,
    tracking_id: str,
    overwrite: False,
) -> None:

    sql_statement = select(registry_schema.metrics).where(
        registry_schema.model_tracking_id == tracking_id
    )

    result = engine.execute(sql_statement).scalar()

    if result is not None and overwrite == False:
        raise exceptions.MetricsExist(
            """Metrics column in database is not null. If you'd like to overwrite this data set overwrite=True"""
        )

    new_data = {"metrics": metrics}
    data_to_log = clean_data(registry_type="FlightParams", data=new_data)

    sql_statement = (
        update(registry_schema)
        .where(registry_schema.model_tracking_id == tracking_id)
        .values(**data_to_log)
    )

    result = engine.execute(sql_statement)


def log_params(
    engine: Callable, registry_schema: Type[base], data: Dict[str, Any],
) -> None:

    data_to_log = clean_data(registry_type="params", data=data)
    engine.execute(registry_schema.__table__.insert(data_to_log))


# log params should always use model registry
def log_model_metadata(
    engine: Callable,
    data: Dict[str, Any],
    project_name: str,
    model_tracking_id: str,
    params_schema: Type[base],
    model_registry_schema: Type[base],
):

    # check if model tracking id is active
    active = check_if_id_active(engine, model_tracking_id, model_registry_schema)

    if active:
        # This funtion should always receive a model tracking id

        data = {
            **{
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "timestamp": time.time(),
                "project_name": project_name,
                "model_tracking_id": model_tracking_id,
            },
            **data,
        }

        # Insert to table
        log_registry_values(
            engine, registry_schema=params_schema, data=data,
        )
    else:
        raise exceptions.NonActiveModelTrackingID


# log metrics should always use model registry
# def log_metrics(engine, data, registry_schema, stage):


def set_storage_location(
    tracker_type,
    tracking_engine: callable,
    tracking_registry: callable,
    s3_bucket: str = None,
    project_name: str = None,
    flight_tracking_id: str = None,
    tracking_id: str = None,
    log_data: bool = False,
):
    if tracker_type == "model":
        tracker_keyword = "model_dir"
    elif tracker_type == "data":
        tracker_keyword = "data_dir"
    else:
        tracker_keyword = tracker_type

    if flight_tracking_id is not None:
        main_tracking_id = flight_tracking_id
        second_tracking_id = None or tracking_id
    else:
        main_tracking_id = tracking_id
        second_tracking_id = None

    if s3_bucket is not None:
        bucket_prefix = None
        if project_name is not None:
            bucket_prefix = f"projects/{project_name}"
        if main_tracking_id is not None:
            if bucket_prefix is not None:
                bucket_prefix = f"{bucket_prefix}/{main_tracking_id}/{tracker_keyword}"
            else:
                bucket_prefix = f"{main_tracking_id}/{tracker_keyword}"

        elif main_tracking_id is None:
            if bucket_prefix is not None:
                bucket_prefix = f"{bucket_prefix}/{tracker_keyword}"
            else:
                bucket_prefix = f"{tracker_keyword}"

        if second_tracking_id is not None:
            bucket_prefix = f"{bucket_prefix}/{second_tracking_id}"

    if log_data:
        log_registry_values(
            engine=tracking_engine,
            registry_schema=tracking_registry,
            data={"s3_location": f"s3://{s3_bucket}/{bucket_prefix}"},
            tracking_id=tracking_id,
        )
    return bucket_prefix
