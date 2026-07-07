import logging
import services.gcs_land_to_bq.config as config
from google.cloud import bigquery
from datetime import datetime,timezone

bq_client=config.get_bq_client()

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


# def is_file_already_processed(file_name):

#     query = f"""
#     SELECT COUNT(*) cnt
#     FROM `{bq_client.project}.{config.AUDIT_DATASET}.processed_files`
#     WHERE file_name = @file_name
#     """

#     job_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter(
#                 "file_name",
#                 "STRING",
#                 file_name
#             )
#         ]
#     )

#     result = bq_client.query(
#         query,
#         job_config=job_config
#     ).result()

#     for row in result:

#         if row.cnt > 0:

#             logging.info(
#                 f"File already processed: {file_name}"
#             )

#             return True

#     return False

# def mark_file_processing(file_name):

#     table_id = (
#         f"{bq_client.project}."
#         f"{config.AUDIT_DATASET}."
#         f"processed_files"
#     )

#     rows = [
#         {
#             "file_name": file_name,
#             "status": "PROCESSING",
#             "created_timestamp":
#                 datetime.now(timezone.utc).isoformat()
#         }
#     ]

#     result=bq_client.insert_rows_json(
#         table_id,
#         rows
#     )

def mark_file_success(file_name):

    table_id = (
        f"{bq_client.project}."
        f"{config.AUDIT_DATASET}."
        f"processed_files"
    )

    rows = [
        {
            "file_name": file_name,
            "status": "SUCCESS",
            "created_timestamp":
                datetime.now(timezone.utc).isoformat()
        }
    ]

    errors = bq_client.insert_rows_json(
        table_id,
        rows
    )

    if errors:
        raise Exception(
            f"Processed file insert failed: {errors}"
        )

    logging.info(
        f"File marked as SUCCESS: {file_name}"
    )

    def mark_file_failed(file_name):

        query = f"""
        UPDATE `{bq_client.project}.{config.AUDIT_DATASET}.processed_files`
        SET
            status = 'FAILED'
        WHERE file_name = @file_name
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

        bq_client.query(
            query,
            job_config=job_config
        ).result()

        logging.info(
            f"File marked as FAILED: {file_name}"
        )