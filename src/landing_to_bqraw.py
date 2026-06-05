import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import storage
from google.cloud import bigquery
import logging
import os
import yaml
import pandas as pd
from io import BytesIO
from datetime import datetime,timezone
from decimal import Decimal

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

    config_file_path = f"{entity_name}.yaml"

    with open(config_file_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config

def validate_file_extension(file_name, config):

    allowed_extensions = config["allowed_extensions"]

    for extension in allowed_extensions:

        if file_name.lower().endswith(extension.lower()):
            return True

    raise Exception(
        f"Invalid file extension for file: {file_name}"
    )

def read_parquet_file(file_name):

    bucket = storage_client.bucket(LANDING_BUCKET)

    blob = bucket.blob(file_name)

    if not blob.exists():

        logging.info(
            f"File not found, skipping: {file_name}"
        )

        return

    parquet_bytes = blob.download_as_bytes()

    df = pd.read_parquet(
        BytesIO(parquet_bytes)
    )

    df.columns = [col.lower() for col in df.columns]

    return df

def validate_mandatory_columns(df, config):

    mandatory_columns = config["mandatory_columns"]

    for column in mandatory_columns:

        if column not in df.columns:

            raise Exception(
                f"Mandatory column missing: {column}"
            )

    logging.info(
        "Mandatory column validation passed"
    )

def validate_mandatory_non_null_columns(df, config):

    mandatory_non_null_columns = config[
        "mandatory_non_null_columns"
    ]

    for column in mandatory_non_null_columns:

        null_count = df[column].isnull().sum()

        if null_count > 0:

            raise Exception(
                f"Column {column} contains "
                f"{null_count} null values"
            )

    logging.info(
        "Mandatory non-null validation passed"
    )

def add_audit_columns(df, file_name):

    df["source_file_name"] = file_name

    df["load_timestamp"] = datetime.now()

    return df

def load_to_bigquery(df, config):

    table_id = (
        f"{bq_client.project}."
        f"{config['target_dataset']}."
        f"{config['target_table']}"
    )

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    job = bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()

    logging.info(
        f"Loaded {len(df)} rows into {table_id}"
    )

def validate_row_count_reconciliation(
    file_name,
    source_row_count,
    config
):

    table_id = (
        f"{bq_client.project}."
        f"{config['target_dataset']}."
        f"{config['target_table']}"
    )

    query = f"""
    SELECT COUNT(*) AS loaded_rows
    FROM `{table_id}`
    WHERE source_file_name = @file_name
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "file_name",
                "STRING",
                file_name
            )
        ]
    )

    result = bq_client.query(
        query,
        job_config=job_config
    ).result()

    for row in result:

        loaded_rows = row.loaded_rows

        if loaded_rows != source_row_count:

            raise Exception(
                f"Row count mismatch. "
                f"Source={source_row_count}, "
                f"BigQuery={loaded_rows}"
            )

    logging.info(
        f"Row count reconciliation passed. "
        f"Source={source_row_count}, "
        f"BigQuery={loaded_rows}"
    )

def insert_audit_record(
    entity_name,
    file_name,
    records_loaded,
    status,
    error_message=None
):

    table_id = (
        f"{bq_client.project}."
        f"{AUDIT_DATASET}."
        f"load_audit"
    )

    rows_to_insert = [
        {
            "table_name": entity_name,
            "source_file_name": file_name,
            "file_received_timestamp": datetime.now(timezone.utc).isoformat(),
            "load_timestamp": datetime.now(timezone.utc).isoformat(),
            "records_loaded": records_loaded,
            "records_rejected": 0,
            "status": status,
            "error_message": error_message
        }
    ]

    errors = bq_client.insert_rows_json(
        table_id,
        rows_to_insert
    )

    if errors:
        raise Exception(
            f"Audit insert failed: {errors}"
        )

    logging.info(
        "Audit record inserted successfully"
    )

def move_to_archive(file_name):

    landing_bucket = storage_client.bucket(
        LANDING_BUCKET
    )

    archive_bucket = storage_client.bucket(
        ARCHIVE_BUCKET
    )

    source_blob = landing_bucket.blob(
        file_name
    )

    if not source_blob.exists():

        logging.info(
            f"File already moved: {file_name}"
        )


    landing_bucket.copy_blob(
        source_blob,
        archive_bucket,
        file_name
    )

    source_blob.delete()

    logging.info(
        f"File archived successfully: {file_name}"
    )

def move_to_error(file_name):

    landing_bucket = storage_client.bucket(
        LANDING_BUCKET
    )

    error_bucket = storage_client.bucket(
        ERROR_BUCKET
    )

    source_blob = landing_bucket.blob(
        file_name
    )
    
    if not source_blob.exists():

        logging.info(
            f"File already moved: {file_name}"
        )
        return


    landing_bucket.copy_blob(
        source_blob,
        error_bucket,
        file_name
    )

    source_blob.delete()

    logging.info(
        f"File moved to error bucket: {file_name}"
    )

def is_file_already_processed(file_name):

    query = f"""
    SELECT COUNT(*) AS cnt
    FROM `{bq_client.project}.{AUDIT_DATASET}.load_audit`
    WHERE source_file_name = @file_name
      AND status = 'SUCCESS'
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "file_name",
                "STRING",
                file_name
            )
        ]
    )

    result = bq_client.query(
        query,
        job_config=job_config
    ).result()

    for row in result:

        if row.cnt > 0:

            logging.info(
                f"File already processed: {file_name}"
            )

            return True

    return False

@functions_framework.cloud_event
def landing_trigger(cloud_event: CloudEvent):

    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    logging.info(f"Landing file received: {file_name}")

    entity_name = get_entity_name(file_name)
    
    if is_file_already_processed(file_name):

        logging.info(
            f"Skipping duplicate file: {file_name}"
        )

        return

    try:

        logging.info(f"Entity identified: {entity_name}")

        config = load_yaml_config(entity_name)
        logging.info(f"Config Loaded: {config}")

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

        if df is None:

            logging.info(
                f"No file available for processing: {file_name}"
            )

            return

        logging.info(
            f"Total rows in file: {len(df)}"
        )

        validate_mandatory_columns(
            df,
            config
        )

        validate_mandatory_non_null_columns(
        df,
        config
        )

        df = add_audit_columns(
        df,
        file_name
        )

        if "order_date" in df.columns:

            df["order_date"] = pd.to_datetime(
                df["order_date"],
                format="%d-%m-%y"
            ).dt.date

        if "last_updated_date" in df.columns:

            df["last_updated_date"] = pd.to_datetime(
                df["last_updated_date"],
                format="%d-%m-%y"
            ).dt.date


        numeric_columns = [
            "unit_price",
            "order_amount"
        ]

        for col in numeric_columns:

            if col in df.columns:

                df[col] = df[col].apply(
                    lambda x: Decimal(str(x))
                )

        load_to_bigquery(
        df,
        config
        )

        validate_row_count_reconciliation(
            file_name=file_name,
            source_row_count=len(df),
            config=config
        )

        insert_audit_record(
        entity_name=entity_name,
        file_name=file_name,
        records_loaded=len(df),
        status="SUCCESS"
        )

        move_to_archive(
        file_name
        )
    
    except Exception as e:
        logging.error(
        f"Pipeline failed: {str(e)}"
        )

        insert_audit_record(
            entity_name=entity_name,
            file_name=file_name,
            records_loaded=0,
            status="FAILED",
            error_message=str(e)
        )

        move_to_error(
            file_name
        )

        return