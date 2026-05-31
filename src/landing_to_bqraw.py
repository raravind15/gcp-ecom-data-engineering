import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import storage
from google.cloud import bigquery
import logging
import os
import yaml
import pandas as pd
from io import BytesIO

logging.basicConfig(level=logging.INFO)

LANDING_BUCKET = os.environ.get("LANDING_BUCKET")
ARCHIVE_BUCKET = os.environ.get("ARCHIVE_BUCKET")
ERROR_BUCKET = os.environ.get("ERROR_BUCKET")

RAW_DATASET = os.environ.get("RAW_DATASET")
AUDIT_DATASET = os.environ.get("AUDIT_DATASET")

storage_client = storage.Client()
bq_client = bigquery.Client()

def get_entity_name(file_name):

    file_base_name = file_name.split("/")[-1]

    entity_name = file_base_name.split("_")[0]

    return entity_name

def load_yaml_config(entity_name):

    config_file_path = f"configs/{entity_name}.yaml"

    with open(config_file_path, "r") as yaml_file:

        config = yaml.safe_load(yaml_file)

    return config

def validate_file_extension(file_name, config):

    allowed_extensions = config["file_config"]["allowed_extensions"]

    for extension in allowed_extensions:

        if file_name.lower().endswith(extension.lower()):
            return True

    raise Exception(
        f"Invalid file extension for file: {file_name}"
    )

def read_parquet_file(file_name):

    bucket = storage_client.bucket(LANDING_BUCKET)

    blob = bucket.blob(file_name)

    parquet_bytes = blob.download_as_bytes()

    df = pd.read_parquet(
        BytesIO(parquet_bytes)
    )

    return df
@functions_framework.cloud_event
def landing_trigger(cloud_event: CloudEvent):

    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    logging.info(f"Landing file received: {file_name}")

    entity_name = get_entity_name(file_name)

    logging.info(f"Entity identified: {entity_name}")

    config = load_yaml_config(entity_name)

    logging.info(
        f"Target Table: "
        f"{config['target_dataset']}."
        f"{config['target_table']}"
    )

    validate_file_extension(
        file_name,
        config
    )

    logging.info(
        "File extension validation passed"
    )

    df = read_parquet_file(file_name)

    logging.info(
        f"Total rows in file: {len(df)}"
    )