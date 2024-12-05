"""Utility functions for Docker connector."""

import logging
from typing import Any, Dict, List

from docker.models.images import Image

from connectors.docker.docker_registry_connector import DockerRegistryConnector


def find_images(
    connector: DockerRegistryConnector, filters: Dict[str, Any]
) -> List[Image]:
    """Finds images by label.

    Args:
        connector: Docker registry connector.
        filters: Filters.

    Returns:
        List of images.
    """
    try:
        return connector.client.images.list(filters=filters)
    except Exception as e:
        logging.error(f"Error finding images: {e}")
    return []


def run_image(connector: DockerRegistryConnector, image_id: str) -> None:
    """Runs an image.

    Args:
        connector: Docker registry connector.
        image_id: Image ID.
    """
    # Pull the image
    image = connector.client.images.pull(image_id)

    # Run the image
    connector.client.containers.run(image)


def stop_image(connector: DockerRegistryConnector, image: Image) -> None:
    """Stops an image.

    Args:
        connector: Docker registry connector.
        image: Image.
    """
    container = connector.client.containers.get(image.id)
    container.stop()
    container.remove()


def delete_image(connector: DockerRegistryConnector, image_id: str) -> None:
    """Deletes an image.

    Args:
        connector: Docker registry connector.
        image_id: Image ID.
    """
    connector.client.images.remove(image_id, noprune=False)
