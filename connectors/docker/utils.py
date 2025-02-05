"""Utility functions for Docker connector."""

import logging
from typing import Any, Dict, List

import requests
from docker.models.containers import Container
from docker.models.images import Image

from connectors.docker.docker_registry_connector import DockerRegistryConnector


def find_remote_images(
    connector: DockerRegistryConnector, filters: Dict[str, Any]
) -> List[Image]:
    """Finds images in remote repository by label.

    This function uses the Docker API to find images in the remote repository
    as the connector list method works only for local images.

    Args:
        connector: Docker registry connector.
        filters: Filters.

    Returns:
        List of images.
    """
    url = f"{connector.registry_uri}/v2/{connector.repository}/tags/list"
    auth = (connector.username, connector.password)
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        data = response.json()
        tags = data.get("tags", [])

        # Pull the images and filter by labels
        images = []
        for tag in tags:
            image = connector.pull_image(f"{tag}")
            if all(
                label in image.labels.items()
                for label in filters.get("label", {}).items()
            ):
                images.append(image)
            else:
                connector.client.images.remove(image.id, noprune=True)
        return images
    except Exception as e:
        logging.error(f"Error finding images: {e}")
    return []


def get_image(connector: DockerRegistryConnector, image_id: str) -> Image:
    """Gets an image by ID.

    Args:
        connector: Docker registry connector.
        image_id: Image ID.

    Returns:
        Image.
    """
    try:
        return connector.pull_image(image_id)
    except Exception as e:
        logging.error(f"Error getting image: {e}")
    return None


def run_image(
    connector: DockerRegistryConnector,
    image_id: str,
    run_args: Dict[str, Any] = {},
) -> Container:
    """Runs an image.

    Args:
        connector: Docker registry connector.
        image_id: Image ID.
        run_args: Arguments for the run command.

    Returns:
        Container running the image.
    """
    # Pull the image
    image = connector.client.images.pull(image_id)

    # Run the image
    container = connector.client.containers.run(image, detach=True, **run_args)
    return container


def stop_container(
    connector: DockerRegistryConnector, container_id: str
) -> None:
    """Stops a container.

    Args:
        connector: Docker registry connector.
        container_id: Container ID.
    """
    container = connector.client.containers.get(container_id)
    container.stop()


def delete_image(connector: DockerRegistryConnector, image_id: str) -> None:
    """Deletes an image.

    Args:
        connector: Docker registry connector.
        image_id: Image ID.
    """
    connector.client.images.remove(image_id, noprune=False)
