import config   

def copy_file(file_name):
    source_bucket = config.storage_client.bucket(config.SOURCE_BUCKET)

    source_blob = source_bucket.blob(file_name)

    landing_bucket = config.storage_client.bucket(config.LANDING_BUCKET)

    source_bucket.copy_blob(
    source_blob,
    landing_bucket,
    file_name
    )