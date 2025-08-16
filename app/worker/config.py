import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()


def get_redis_url():
    """
    Get the Redis URL for Celery configuration.

    Returns:
        str: The Redis URL.
    """
    # Prefer explicit REDIS_URL if provided (local dev override)
    explicit_redis_url = os.getenv("REDIS_URL")
    if explicit_redis_url:
        return explicit_redis_url

    # Fallbacks: use Docker service name when PROJECT_NAME is set,
    # otherwise default to localhost for local development
    project_name = os.getenv("PROJECT_NAME")
    redis_host = f"{project_name}_redis" if project_name else "localhost"
    return f"redis://{redis_host}:6379/0"


def get_celery_config():
    """
    Get the Celery configuration.

    Returns:
        dict: The Celery configuration.
    """
    redis_url = get_redis_url()
    return {
        "broker_url": redis_url,
        "result_backend": redis_url,
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "enable_utc": True,
        "broker_connection_retry_on_startup": True,
    }


celery_app = Celery("tasks")
celery_app.config_from_object(get_celery_config())

# Automatically discover and register tasks
celery_app.autodiscover_tasks(["app.worker.tasks"], force=True)
