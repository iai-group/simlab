"""Celery worker."""

import os

from celery import Celery
from flask import logging

from webapp.backend.app import docker_registry_connector

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost"
)

celery = Celery(
    "simlab_background_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery.task
def upload_image_task(image_name: str, file_path: str) -> bool:
    """Uploads an image to the Docker registry in background.

    Args:
        image_name: Image name.
        file_path: Path to the image file.
    """
    try:
        docker_registry_connector.client.images.load(open(file_path, "rb"))
        docker_registry_connector.push_image(image_name)
    except Exception as e:
        logging.error(f"Failed to push image: {e}")
        return False
    finally:
        os.remove(file_path)

    return True
