import base64
import json

from shared.core.logger import get_logger

logger = get_logger(__name__)


def process_event(message):

    decoded_message = base64.b64decode(
        message["data"]
    ).decode("utf-8")

    event = json.loads(decoded_message)

    logger.info(
        "Received Event: %s",
        event
    )

    return {
        "status": "SUCCESS",
        "message": "Event processed successfully."
    }