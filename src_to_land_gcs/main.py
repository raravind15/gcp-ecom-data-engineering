import functions_framework
from cloudevents.http import CloudEvent
import logging
import storage_service

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@functions_framework.cloud_event
def gcs_trigger(cloud_event: CloudEvent):
    
    data = cloud_event.data
    
    file_name = data["name"]

    if file_name.endswith("/"):
        logging.info("Folder event detected. Ignoring.")
        return
    
    logging.info(f"File received: {file_name}")

    storage_service.copy_file(file_name)
    
    logging.info(
        f"File copied successfully to landing bucket: {file_name}"
    )