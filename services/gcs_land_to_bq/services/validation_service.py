import logging
from google.cloud import bigquery
import services.gcs_land_to_bq.config as config

bq_client=config.get_bq_client()

def validate_file_extension(file_name, config):

    allowed_extensions = config["allowed_extensions"]

    for extension in allowed_extensions:

        if file_name.lower().endswith(extension.lower()):
            return True

    raise Exception(
        f"Invalid file extension for file: {file_name}"
    )



def validate_mandatory_columns(df, config):

    mandatory_columns = config["mandatory_columns"]

    for column in mandatory_columns:

        if column not in df.columns:

            raise Exception(
                f"Mandatory column missing: {column}"
            )

    logging.info(
        "Mandatory column validation passed"
    )

def validate_mandatory_non_null_columns(df, config):

    mandatory_non_null_columns = config[
        "mandatory_non_null_columns"
    ]

    for column in mandatory_non_null_columns:

        null_count = df[column].isnull().sum()

        if null_count > 0:

            raise Exception(
                f"Column {column} contains "
                f"{null_count} null values"
            )

    logging.info(
        "Mandatory non-null validation passed"
    )

def validate_row_count_reconciliation(
    file_name,
    source_row_count,
    config
):

    table_id = (
        f"{bq_client.project}."
        f"{config['target_dataset']}."
        f"{config['target_table']}"
    )

    query = f"""
    SELECT COUNT(*) AS loaded_rows
    FROM `{table_id}`
    WHERE source_file_name = @file_name
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "file_name",
                "STRING",
                file_name
            )
        ]
    )

    result = bq_client.query(
        query,
        job_config=job_config
    ).result()

    for row in result:

        loaded_rows = row.loaded_rows

        if loaded_rows != source_row_count:

            raise Exception(
                f"Row count mismatch. "
                f"Source={source_row_count}, "
                f"BigQuery={loaded_rows}"
            )

    logging.info(
        f"Row count reconciliation passed. "
        f"Source={source_row_count}, "
        f"BigQuery={loaded_rows}"
    )