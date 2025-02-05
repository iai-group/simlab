"""Celery worker."""

import os
from datetime import datetime

from celery import Celery
from flask import logging

from connectors.mongo.utils import insert_record
from webapp.backend.app import docker_registry_connector, mongo_connector

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
    """
    try:
        image = docker_registry_connector.client.images.load(
            open(file_path, "rb")
        )[0]

        if not image.labels.get("type"):
            raise ValueError("Image type not found")

        docker_registry_connector.push_image(image_name)

        # Save system image information in MongoDB
        insert_record(
            mongo_connector,
            "system_images",
            {
                "name": image_name,
                "tag": docker_registry_connector.get_remote_image_tag(
                    image_name
                ),
                "type": image.labels.get("type", None),
                "description": image.labels.get("description", None),
                "author": image.labels.get("author", None),
                "version": image.labels.get("version", None),
                "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
    except Exception as e:
        logging.error(f"Failed to push image: {e}")
        return False
    finally:
        os.remove(file_path)

    return True
