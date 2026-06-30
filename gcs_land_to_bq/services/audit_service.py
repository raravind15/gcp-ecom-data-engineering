import logging
import config
from datetime import datetime,timezone

bq_client=config.get_bq_client()


def insert_audit_record(
    entity_name,
    file_name,
    records_loaded,
    status,
    error_message=None
):

    table_id = (
        f"{bq_client.project}."
        f"{config.AUDIT_DATASET}."
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