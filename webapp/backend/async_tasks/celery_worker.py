"""Celery worker."""

import os
import tempfile
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
def upload_image_task(image_name: str, file) -> bool:
    """Uploads an image to the Docker registry in background.

    A record of the image is saved in the MongoDB as docker connector cannot
    directly access the list of tags in the remote registry.

    Args:
        image_name: Image name.
        file: File to upload.

    Returns:
        True if the image was successfully uploaded, False otherwise.
    """
    try:
        # Temporary save the file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".tar"
        ) as temp_file:
            file.save(temp_file.name)
            temp_file.close()
            file_path = temp_file.name

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
                )[0],
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
