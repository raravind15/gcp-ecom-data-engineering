from shared.core.logger import get_logger
from google.cloud import bigquery

logger = get_logger(__name__)
bq_client=bigquery.Client()


def execute(dataset: str, procedure_name: str):

    logger.info(
        "Executing BigQuery Stored Procedure %s.%s",
        dataset,
        procedure_name,
    )

    try:

        bq_client.query(
            f"CALL `{dataset}.{procedure_name}`();"
        ).result()

        logger.info(
            "Stored Procedure %s.%s executed successfully.",
            dataset,
            procedure_name,
        )

    except Exception:

        logger.exception(
            "Failed to execute Stored Procedure %s.%s",
            dataset,
            procedure_name,
        )

        raise