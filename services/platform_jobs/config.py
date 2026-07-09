import os

class AppInfo:
    SERVICE_NAME = os.getenv("SERVICE_NAME", "platform_jobs")

    SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

class Config:
    """Application configuration."""

    PROJECT_ID = os.getenv("PROJECT_ID", "")

    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")