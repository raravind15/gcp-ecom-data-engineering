import logging
import config
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


