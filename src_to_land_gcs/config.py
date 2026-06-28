import os
from google.cloud import storage

SOURCE_BUCKET = os.getenv("SOURCE_BUCKET")

LANDING_BUCKET = os.getenv("LANDING_BUCKET")

storage_client = storage.Client()