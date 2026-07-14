import json

from google.cloud import pubsub_v1

from shared.core.config import AppInfo
from shared.core.logger import get_logger

logger = get_logger(__name__)

publisher = pubsub_v1.PublisherClient()

TOPIC_PATH = publisher.topic_path(
    AppInfo.PROJECT_ID,
    "event-notifications"
)


def publish_event(
    table_name: str,
    status: str,
    rows_loaded: int
):

    message = {
        "table_name": table_name,
        "status": status,
        "rows_loaded": rows_loaded
    }

    future = publisher.publish(
        TOPIC_PATH,
        json.dumps(message).encode("utf-8")
    )

    logger.info(
        "Published Event: %s",
        future.result()
    )