import logging
import config as config
import pandas as pd
from io import BytesIO

storage_client=config.get_storage_client()
bq_client=config.get_bq_client()

def read_parquet_file(bucket_name,file_name):

    bucket = storage_client.bucket(bucket_name)

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

def move_to_archive(source_bucket,target_bucket,file_name):

    landing_bucket = storage_client.bucket(
        source_bucket
    )

    archive_bucket = storage_client.bucket(
        target_bucket
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
        archive_bucket,
        file_name
    )

    source_blob.delete()

    logging.info(
        f"File archived successfully: {file_name}"
    )

def move_to_error(source_bucket,target_bucket,file_name):

    landing_bucket = storage_client.bucket(
        source_bucket
    )

    error_bucket = storage_client.bucket(
        target_bucket
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