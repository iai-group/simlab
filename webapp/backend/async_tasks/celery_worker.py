"""Celery worker."""

import logging
import os

from celery import Celery

from connectors.docker.commands import (
    docker_stream_push_image,
    get_remote_image_tag,
    load_image,
)
from connectors.mongo.utils import upsert_records
from webapp.backend.app import docker_registry_metadata, mongo_connector

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

    A record of the image is saved in the MongoDB as docker connector cannot
    directly access the list of tags in the remote registry.

    Args:
        image_name: Image name.
        file_path: Path to the image file.

    Returns:
        True if the image was successfully uploaded, False otherwise.
    """
    try:
        image_info = load_image(file_path)
        image_labels = image_info.get("Config", {}).get("Labels", {})

        if not image_labels.get("type"):
            raise ValueError("Image type not found")

        for log_line in docker_stream_push_image(
            image_name, docker_registry_metadata
        ):
            logging.info(f"[docker] {log_line}")

        # Save or update system image information in MongoDB
        repo, tag = get_remote_image_tag(image_name, docker_registry_metadata)

        record = {
            "image_name": image_name,
            "repository": repo,
            "tag": tag,
        }
        record.update(image_labels)
        upsert_records(mongo_connector, "system_images", [record])

    except Exception as e:
        logging.error(f"Failed to push image: {e}")
        return False
    finally:
        # TODO: Remove new image from local registry to free space
        os.remove(file_path)
