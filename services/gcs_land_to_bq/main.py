import functions_framework
from cloudevents.http import CloudEvent
import logging
import yaml
import config as app_config
from services import storage_service
from services import validation_service
from services import bq_service
from services import audit_service
from services import procedure_service
from services import processing_service
from services import firestore_service
from utils import helper
from utils import config_loader
from handler import pubsub_publisher

logging.basicConfig(level=logging.INFO)

@functions_framework.cloud_event

def landing_trigger(cloud_event: CloudEvent):
    logging.info(f"Cloud Event ID: {cloud_event['id']}")

    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    logging.info(f"Landing file received: {file_name}")

    entity_name = helper.get_entity_name(file_name)
    
    if not firestore_service.claim_file(
        file_name,
        cloud_event["id"]
    ):

        logging.info(
            f"Skipping duplicate file: {file_name}"
        )

        return

    try:

        logging.info(f"Entity identified: {entity_name}")

        config = config_loader.load_yaml_config(entity_name)
        logging.info(f"Config Loaded: {config}")

        logging.info(
            f"Target Table: "
            f"{config['target_dataset']}."
            f"{config['target_table']}"
        )

        validation_service.validate_file_extension(
            file_name,
            config
        )

        logging.info(
            "File extension validation passed"
        )

        df = storage_service.read_parquet_file(app_config.LANDING_BUCKET,file_name)

        if df is None:

            logging.info(
                f"No file available for processing: {file_name}"
            )

            return

        logging.info(
            f"Total rows in file: {len(df)}"
        )

        validation_service.validate_mandatory_columns(
            df,
            config
        )

        validation_service.validate_mandatory_non_null_columns(
        df,
        config
        )

        df = processing_service.process_dataframe(
        df,
        file_name
        )

        bq_service.load_to_bigquery(
        df,
        config
        )

        pubsub_publisher.publish_event(
        table_name=config['target_table'],
        status="SUCCESS",
        rows_loaded=len(df)
        )

        validation_service.validate_row_count_reconciliation(
            file_name=file_name,
            source_row_count=len(df),
            config=config
        )

        procedure_service.call_transform_procedure(entity_name)

        procedure_service.call_curated_procedure(entity_name)

        audit_service.insert_audit_record(
        entity_name=entity_name,
        file_name=file_name,
        records_loaded=len(df),
        status="SUCCESS"
        )

        firestore_service.mark_success(file_name)
        bq_service.mark_file_success(file_name)

        storage_service.move_to_archive(app_config.LANDING_BUCKET,app_config.ARCHIVE_BUCKET,
        file_name
        )
    
    except Exception as e:
        logging.error(
        f"Pipeline failed: {str(e)}"
        )

        audit_service.insert_audit_record(
            entity_name=entity_name,
            file_name=file_name,
            records_loaded=0,
            status="FAILED",
            error_message=str(e)
        )

        firestore_service.mark_failed(file_name)
        bq_service.mark_file_failed(file_name)

        storage_service.move_to_error(app_config.LANDING_BUCKET,app_config.ERROR_BUCKET,
            file_name
        )

        return