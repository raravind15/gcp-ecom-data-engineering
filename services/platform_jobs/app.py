"""
Main application entry point.
"""
import os
from flask import Flask

from shared.core.config import AppInfo
from shared.core.logger import get_logger
from services.platform_jobs.routes.run_procedure import run_procedure_bp

logger = get_logger(__name__)

app = Flask(__name__)

app.register_blueprint(run_procedure_bp)

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