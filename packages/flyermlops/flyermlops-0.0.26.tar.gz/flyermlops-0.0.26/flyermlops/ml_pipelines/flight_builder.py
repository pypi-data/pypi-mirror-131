# Core
from typing import Dict
import logging
import os
import re
from flyermlops.tracking.tracking_objects import FlightTracker
from pathlib import Path
import click
import yaml
import sys

# Sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.tensorflow import TensorFlow
from sagemaker.workflow.steps import TrainingStep
from sagemaker.workflow.lambda_step import LambdaStep
from sagemaker.lambda_helper import Lambda
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.retry import (
    StepRetryPolicy,
    StepExceptionTypeEnum,
    SageMakerJobExceptionTypeEnum,
    SageMakerJobStepRetryPolicy,
)

# Flyermlops
from .cli_utils import stdout_msg
from . import flight_utils


# Get logger
logger = logging.getLogger(__name__)


def retry_policy(max_retry):
    return [
        StepRetryPolicy(
            exception_types=[
                StepExceptionTypeEnum.SERVICE_FAULT,
                StepExceptionTypeEnum.THROTTLING,
            ],
            expire_after_mins=5,
            interval_seconds=10,
            backoff_rate=2.0,
        ),
        SageMakerJobStepRetryPolicy(
            exception_types=[SageMakerJobExceptionTypeEnum.RESOURCE_LIMIT],
            expire_after_mins=120,
            interval_seconds=60,
            backoff_rate=2.0,
        ),
        SageMakerJobStepRetryPolicy(
            failure_reason_types=[
                SageMakerJobExceptionTypeEnum.INTERNAL_ERROR,
                SageMakerJobExceptionTypeEnum.CAPACITY_ERROR,
            ],
            max_attempts=max_retry,
            interval_seconds=30,
            backoff_rate=2.0,
        ),
    ]


def build_leg(leg, resources, vpc_config, sm_role, config):
    dags = {}
    logging.info(f"Building {leg} DAGs")

    # Verify flight arguments
    flight_utils.verify_args(
        resources["engine"],
        resources["number_engines"],
        resources["ac_type"],
        resources["dependencies"],
    )

    if config["part_of_flight"]:
        hyperparameters = {"flight_tracking_id": config["flight_tracking_id"]}

    # find leg path
    for path in Path(config["project_name"]).rglob(f"{leg}.py"):
        entry_point = "/".join(str(path.absolute()).split("/")[-2:])

    try:

        if resources["ac_type"] == "sklearn":
            processor = SKLearn(
                entry_point=entry_point,  # entry_point,
                source_dir=f"{config['project_name']}/pipeline",
                code_location=f"s3://{config['s3_bucket']}/{config['s3_flight_path_key']}/{leg}",
                role=sm_role,
                instance_count=resources["number_engines"],
                instance_type=resources["engine"],
                output_path=f"s3://{config['s3_bucket']}/{config['s3_flight_path_key']}/{leg}",
                framework_version="0.20.0",
                py_version="py3",
                script_mode=True,
                subnets=None or vpc_config.subnets,
                security_group_ids=None or vpc_config.security_group_ids,
                hyperparameters=None or hyperparameters,
            )

            dag = TrainingStep(
                name=leg,
                estimator=processor,
                depends_on=resources["dependencies"] or None,
                retry_policies=retry_policy(resources["retry"]),
            )

        elif resources["ac_type"] == "tensorflow":
            processor = TensorFlow(
                entry_point=entry_point,  # entry_point,
                source_dir=f"{config['project_name']}/pipeline",
                code_location=f"s3://{config['s3_bucket']}/{config['s3_flight_path_key']}/{leg}",
                role=sm_role,
                instance_count=resources["number_engines"],
                instance_type=resources["engine"],
                output_path=f"s3://{config['s3_bucket']}/{config['s3_flight_path_key']}/{leg}",
                framework_version="2.4",
                py_version="py37",
                script_mode=True,
                subnets=None or vpc_config.subnets,
                security_group_ids=None or vpc_config.security_group_ids,
                hyperparameters=None or hyperparameters,
            )

            dag = TrainingStep(
                name=leg,
                estimator=processor,
                depends_on=resources["dependencies"] or None,
                retry_policies=retry_policy(resources["retry"]),
            )

    # Add custom exception statement in exceptions.py
    except Exception as e:
        print(f"Dag build error for: {leg}")
        raise e

    return dag


def get_flight(config: dict, sm_role: str = None) -> Dict:

    # flight legs
    flight_leg_dags = {}

    # od_pairs
    od_pairs = {}

    stdout_msg(
        f"Provisioning resources for flight!", fg="red", bold=True,
    )

    # Sagemaker session
    sage_sess = flight_utils.get_session(config["s3_bucket"], config.get("region_name"))

    # VPC
    if "vpc_config" in config.keys():
        vpc_config = flight_utils.get_vpc_config(config)

    logger.info("Getting flight legs")

    # Get od pairs
    flight_legs = config.get("flight_plan")
    for leg, resources in flight_legs.items():
        destinations = resources["destinations"]
        if isinstance(destinations, str):
            destinations = destinations.split(",")
        od_pairs[leg] = destinations

    # run order
    flight_order = flight_utils.topological_sort(od_pairs)

    # construct dependencies from od pairs
    leg_dependencies = flight_utils.get_step_dependencies(od_pairs)
    for leg in leg_dependencies.keys():
        flight_legs[leg]["dependencies"] = leg_dependencies[leg]

    # build flight legs
    for leg in flight_order:
        resources = flight_legs[leg]
        stdout_msg(f"Building flight leg: {leg}", fg="white")
        flight_leg_dags[leg] = build_leg(leg, resources, vpc_config, sm_role, config,)

    flight_name = flight_utils.clean_text(config["project_name"])[0]
    flight_workflow = Pipeline(name=flight_name, steps=[*flight_leg_dags.values()],)

    return flight_workflow, flight_name


@click.command()
@click.option("--sm_role", default=None, type=str)
def run_flight(sm_role: str = None):

    sm_role = sm_role or os.environ["SAGEMAKER_EXEC_ROLE"]

    try:
        # Set up flight tracker
        config = flight_utils.get_config()

        # Variables
        STORAGE_BUCKET = config.get("s3_bucket")
        PROJECT_NAME = config.get("project_name")

        if config["part_of_flight"]:
            flight_tracker = FlightTracker(**config)
            flight_tracker.start_flight()

            # Variables
            FLIGHT_ID = flight_tracker.flight_tracking_id
            S3_FLIGHT_PATH = f"projects/{PROJECT_NAME}/{FLIGHT_ID}"

            # Load storage location to flight_tracker
            data = {"storage_location": f"s3://{STORAGE_BUCKET}/{S3_FLIGHT_PATH}"}
            flight_tracker.log_to_registry(
                data=data, tracking_id=flight_tracker.flight_tracking_id
            )

            # Add to config
            config["flight_tracking_id"] = FLIGHT_ID

        else:
            S3_FLIGHT_PATH = f"projects/{PROJECT_NAME}"

        config["s3_flight_path_key"] = S3_FLIGHT_PATH

        flight, flight_name = get_flight(config=config, sm_role=sm_role)

        flight.upsert(role_arn=sm_role)

        if config["part_of_flight"]:
            flight.start(execution_display_name=config["flight_tracking_id"])
            stdout_msg(
                f"Takeoff!", fg="red", bold=True,
            )
        else:
            flight.start()

    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)
