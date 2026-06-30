import config   

def copy_file(file_name):
    storage_client=config.get_storage_client()
    source_bucket =storage_client.bucket(config.SOURCE_BUCKET)

    source_blob = source_bucket.blob(file_name)

    landing_bucket =storage_client.bucket(config.LANDING_BUCKET)

    # source_bucket.copy_blob(
    # source_blob,
    # landing_bucket,
    # file_name
    # )
    print("Bug introduced")