"""
Health endpoint.
"""

from flask import jsonify

from shared.core.config import AppInfo, Config
from shared.core.logger import get_logger

logger = get_logger(__name__)


def health_check():
    """
    Health check endpoint.
    """

    logger.info("Health endpoint invoked")

    return jsonify(
        {
            "status": "SUCCESS",
            "service": AppInfo.SERVICE_NAME,
            "version": AppInfo.SERVICE_VERSION,
            "environment": Config.ENVIRONMENT,
            "message": "Service is healthy"
        }
    ), 200