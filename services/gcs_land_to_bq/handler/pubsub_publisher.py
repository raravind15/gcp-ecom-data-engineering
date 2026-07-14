import json
import logging
import os

from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)

publisher = pubsub_v1.PublisherClient()


def publish_event(table_name, status, rows_loaded):

    topic_path = publisher.topic_path(
        os.environ["PROJECT_ID"],
        "event-notifications"
    )

    message = {
        "table_name": table_name,
        "status": status,
        "rows_loaded": rows_loaded
    }

    future = publisher.publish(
        topic_path,
        json.dumps(message).encode("utf-8")
    )

    logger.info(
        "Published message %s",
        future.result()
    )