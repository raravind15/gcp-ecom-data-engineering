import os

from flask import Flask

from shared.core.config import AppInfo
from shared.core.logger import get_logger

from services.event_consumer.routes.events import events_bp

logger = get_logger(__name__)

app = Flask(__name__)

app.register_blueprint(events_bp)


@app.route("/")
def home():

    return {
        "service": AppInfo.SERVICE_NAME,
        "message": "Event Consumer Service is running."
    }


if __name__ == "__main__":

    logger.info("Starting Event Consumer...")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        debug=False,
    )