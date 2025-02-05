"""Docker connector module.

Establishes a connection to the external private Docker registry.
"""

import os
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
        self.username = username
        self.password = password
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

    def get_remote_image_tag(self, image: str) -> str:
        """Gets the image tag in the Docker registry.

        Args:
            image: Image to get the tag for.

        Returns:
            Image tag.
        """
        registry_host = urlparse(self.registry_uri).netloc
        return f"{registry_host}/{self.repository}/{image}"

    def pull_image(self, image: str) -> Image:
        """Pulls an image from the Docker registry.

        Args:
            image: Image to pull.
        """
        image_tag = self.get_remote_image_tag(image)
        return self.client.images.pull(image_tag)

    def push_image(self, image_name: str) -> None:
        """Pushes an image to the Docker registry.

        Args:
            image_name: Image name to push.
        """
        image_tag = self.get_remote_image_tag(image_name)

        image = self.client.images.get(image_name)
        image.tag(image_name, tag=image_tag)

        # Push the image
        self.client.images.push(image_tag)

        # Remove the image from the local repository
        self.client.images.remove(image_name)
        self.client.images.remove(image_tag)
