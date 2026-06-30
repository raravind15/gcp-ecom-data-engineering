import os
from google.cloud import storage
from google.cloud import bigquery

LANDING_BUCKET = os.environ.get("LANDING_BUCKET")
ARCHIVE_BUCKET = os.environ.get("ARCHIVE_BUCKET")
ERROR_BUCKET = os.environ.get("ERROR_BUCKET")

RAW_DATASET = os.environ.get("RAW_DATASET")
AUDIT_DATASET = os.environ.get("AUDIT_DATASET")

def get_storage_client():
    return storage.Client()

def get_bq_client():
    return bigquery.Client()
