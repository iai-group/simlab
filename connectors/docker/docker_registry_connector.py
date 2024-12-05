"""Docker connector module.

Establishes a connection to the private Docker registry.
"""

import os

import docker

DOCKER_BASE_URL = os.environ.get(
    "DOCKER_BASE_URL", "unix://var/run/docker.sock"
)
DOCKER_REGISTRY_URI = os.environ.get("DOCKER_REGISTRY_URI", "localhost:5000")
DOCKER_ADMIN_USERNAME = os.environ.get("DOCKER_ADMIN_USERNAME", "")
DOCKER_ADMIN_PASSWORD = os.environ.get("DOCKER_ADMIN_PASSWORD", "")


class DockerRegistryConnector:
    def __init__(
        self,
        registry_uri: str = DOCKER_REGISTRY_URI,
        docker_url: str = DOCKER_BASE_URL,
        admin_username: str = DOCKER_ADMIN_USERNAME,
        admin_password: str = DOCKER_ADMIN_PASSWORD,
    ) -> None:
        """Initializes the Docker registry connector.

        Args:
            registry_uri: Docker registry URI. Defaults to DOCKER_REGISTRY_URI.
            docker_url: Docker URL. Defaults to DOCKER_BASE_URL.
            admin_username: Docker admin username. Defaults to
              DOCKER_ADMIN_USERNAME.
            admin_password: Docker admin password. Defaults to
              DOCKER_ADMIN_PASSWORD.
        """
        super().__init__()
        self.registry_uri = registry_uri
        self.client = docker.DockerClient(base_url=docker_url)

        # Login to the Docker registry
        self.client.login(
            username=admin_username,
            password=admin_password,
            registry=registry_uri,
        )

    def close(self) -> None:
        """Closes the connection to the Docker registry."""
        self.client.close()
