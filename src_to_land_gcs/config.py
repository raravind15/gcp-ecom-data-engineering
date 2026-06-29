import os
from google.cloud import storage

SOURCE_BUCKET = os.getenv("SOURCE_BUCKET")

LANDING_BUCKET = os.getenv("LANDING_BUCKET")

def get_storage_client():
    return storage.Client()