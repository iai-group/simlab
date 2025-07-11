"""Docker connector module.

Establishes a connection to the external private Docker registry.
"""

import os
from typing import Tuple
from urllib.parse import urlparse

import docker
import docker.models.images as Image

DOCKER_BASE_URL = os.environ.get(
    "DOCKER_BASE_URL", "unix://var/run/docker.sock"
)
DOCKER_REGISTRY_URI = os.environ.get("DOCKER_REGISTRY_URI", "localhost:5000")
DOCKER_USERNAME = os.environ.get("DOCKER_USERNAME", "")
DOCKER_PASSWORD = os.environ.get("DOCKER_PASSWORD", "")
DOCKER_REPOSITORY = os.environ.get("DOCKER_REPOSITORY", "simlab-systems")


class DockerRegistryConnector:
    def __init__(
        self,
        registry_uri: str = DOCKER_REGISTRY_URI,
        docker_url: str = DOCKER_BASE_URL,
        username: str = DOCKER_USERNAME,
        password: str = DOCKER_PASSWORD,
        repository: str = DOCKER_REPOSITORY,
    ) -> None:
        """Initializes the Docker registry connector.

        Args:
            registry_uri: Docker registry URI. Defaults to DOCKER_REGISTRY_URI.
            docker_url: Docker URL. Defaults to DOCKER_BASE_URL.
            username: Docker username. Defaults to DOCKER_USERNAME.
            password: Docker password. Defaults to DOCKER_PASSWORD.
            repository: Docker repository. Defaults to DOCKER_REPOSITORY.
        """
        super().__init__()
        self.registry_uri = registry_uri
        self.repository = repository
        self.client = docker.DockerClient(base_url=docker_url)

        # Login to the Docker registry
        self.client.login(
            username=username,
            password=password,
            registry=registry_uri,
        )

    def close(self) -> None:
        """Closes the connection to the Docker registry."""
        self.client.close()

    def get_remote_image_tag(self, image: str) -> Tuple[str, str]:
        """Gets the image tag in the Docker registry.

        Args:
            image: Image to get the tag for.

        Returns:
            Remote repository and tag.
        """
        registry_host = urlparse(self.registry_uri).netloc

        if ":" not in image:
            return f"{registry_host}/{self.repository}/{image}", None

        tag = image.split(":")[-1]
        name = image.split(":")[0]
        return f"{registry_host}/{self.repository}/{name}", tag

    def pull_image(self, image: str) -> Image:
        """Pulls an image from the Docker registry.

        Args:
            image: Image to pull.
        """
        remote_repo, tag = self.get_remote_image_tag(image)

        if not tag:
            return self.client.images.pull(remote_repo)

        image_tag = f"{remote_repo}:{tag}"
        return self.client.images.pull(image_tag)

    def push_image(self, image_name: str) -> None:
        """Pushes an image to the Docker registry.

        Args:
            image_name: Image name to push.
        """
        remote_repo, tag = self.get_remote_image_tag(image_name)

        if not tag:
            image_tag = remote_repo
        else:
            image_tag = f"{remote_repo}:{tag}"

        image = self.client.images.get(image_name)
        image.tag(remote_repo, tag=tag)

        # Push the image
        self.client.images.push(image_tag)

        # Remove the image from the local repository
        self.client.images.remove(image_name)
        self.client.images.remove(image_tag)
