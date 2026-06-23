import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import storage
import logging
import os

logging.basicConfig(level=logging.INFO)

SOURCE_BUCKET = os.environ.get("SOURCE_BUCKET")
LANDING_BUCKET = os.environ.get("LANDING_BUCKET")

storage_client=storage.Client()

@functions_framework.cloud_event
def gcs_trigger(cloud_event: CloudEvent):
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]
    if file_name.endswith("/"):
        logging.info("Folder event detected. Ignoring.")
        return
    logging.info(f"File received: {file_name}")
    source_bucket = storage_client.bucket(SOURCE_BUCKET)
    source_blob = source_bucket.blob(file_name)
    landing_bucket = storage_client.bucket(LANDING_BUCKET)
    source_bucket.copy_blob(
    source_blob,
    landing_bucket,
    file_name
    )
    logging.info(
        f"File copied successfully to landing bucket: {file_name}"
    )