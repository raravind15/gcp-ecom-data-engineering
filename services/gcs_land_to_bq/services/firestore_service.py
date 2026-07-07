import logging

import config as config
from google.cloud import firestore
from google.api_core.exceptions import AlreadyExists

firestore_client = config.get_firestore_client()

COLLECTION_NAME = "processed_files"


def claim_file(file_name, event_id):
    """
    Atomically claims a file for processing.
    Returns True if this Cloud Run instance owns the file.
    Returns False if another instance has already claimed it.
    """

    doc_ref = firestore_client.collection(
        COLLECTION_NAME
    ).document(file_name)

    try:

        doc_ref.create(
            {
                "event_id": event_id,
                "status": "PROCESSING",
                "created_timestamp": firestore.SERVER_TIMESTAMP
            }
        )

        logging.info(
            f"File claimed successfully: {file_name}"
        )

        return True

    except AlreadyExists:

        logging.info(
            f"Duplicate event detected: {file_name}"
        )

        return False


def mark_success(file_name):

    firestore_client.collection(
        COLLECTION_NAME
    ).document(file_name).update(
        {
            "status": "SUCCESS"
        }
    )

    logging.info(
        f"File marked SUCCESS: {file_name}"
    )


def mark_failed(file_name):

    firestore_client.collection(
        COLLECTION_NAME
    ).document(file_name).update(
        {
            "status": "FAILED"
        }
    )

    logging.info(
        f"File marked FAILED: {file_name}"
    )