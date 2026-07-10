"""
Main application entry point.
"""
import os
from flask import Flask

from shared.core.config import AppInfo
from shared.core.logger import get_logger
from services.platform_jobs.handlers.jobs.health import health_check

logger = get_logger(__name__)

app = Flask(__name__)

# Register endpoints
app.add_url_rule("/health", view_func=health_check, methods=["GET"])


@app.route("/")
def home():
    return {
        "service": AppInfo.SERVICE_NAME,
        "message": "Platform Jobs Service is running"
    }


if __name__ == "__main__":
    logger.info(f"Starting {AppInfo.SERVICE_NAME} service...")

    app.run(
        host="0.0.0.0",
        port = int(os.getenv("PORT", 8080)),
        debug=False
    )