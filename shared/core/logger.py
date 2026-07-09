"""
Reusable logging configuration for all Cloud Run services.
"""

import logging
import sys

from shared.core.config import Config

_CONFIGURED = False


def _configure_logging() -> None:
    """
    Configure root logging exactly once.
    """
    global _CONFIGURED

    if _CONFIGURED:
        return

    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        stream=sys.stdout,
        force=True,   # Python 3.8+
    )

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Example:
        logger = get_logger(__name__)
    """

    _configure_logging()

    return logging.getLogger(name)