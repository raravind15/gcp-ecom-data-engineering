import base64
import json

from shared.core.logger import get_logger

logger = get_logger(__name__)


def process_event(message):

    decoded_message = base64.b64decode(
        message["data"]
    ).decode("utf-8")

    logger.info("Decoded Message = [%s]", decoded_message)

    try:
        event = json.loads(decoded_message)

        logger.info("Received Event: %s", event)

    except Exception as ex:
        logger.exception("Invalid JSON received")
        raise

    return {
        "status": "SUCCESS",
        "message": "Event processed successfully."
    }