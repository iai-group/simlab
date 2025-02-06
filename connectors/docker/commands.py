"""Utilities for running Docker commands."""

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, Tuple
from urllib.parse import urlparse

DOCKER_REGISTRY_URI = os.environ.get("DOCKER_REGISTRY_URI", "localhost:5000")
DOCKER_USERNAME = os.environ.get("DOCKER_USERNAME", "")
DOCKER_PASSWORD_FILE = os.environ.get("DOCKER_PASSWORD_FILE", "")
DOCKER_REPOSITORY = os.environ.get("DOCKER_REPOSITORY", "simlab-systems")


@dataclass
class DockerRegistryMetadata:
    """Docker registry metadata."""

    registry_uri: str = DOCKER_REGISTRY_URI
    username: str = DOCKER_USERNAME
    password_file: str = DOCKER_PASSWORD_FILE
    repository: str = DOCKER_REPOSITORY


def get_remote_image_tag(
    image: str,
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
) -> Tuple[str, str]:
    """Gets the image tag for the remote Docker registry.

    Args:
        image: Image to get the tag for.
        docker_metadata: Docker registry metadata.

    Returns:
        Remote repository and tag.
    """
    registry_host = urlparse(docker_metadata.registry_uri).netloc

    if ":" not in image:
        return f"{registry_host}/{docker_metadata.repository}/{image}", None

    tag = image.split(":")[-1]
    name = image.split(":")[0]
    return f"{registry_host}/{docker_metadata.repository}/{name}", tag


def docker_login(
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
):
    """Logs in to the remote Docker registry.

    Args:
        docker_metadata: Docker registry metadata.
    """
    auth_command = (
        f"cat {docker_metadata.password_file} | docker login --username "
        f"{docker_metadata.username} --password-stdin "
        f"{docker_metadata.registry_uri}"
    )
    subprocess.run(auth_command, shell=True, check=True)


def load_image(image_path: str) -> Dict[str, Any]:
    """Loads an image to the local Docker registry.

    Args:
        image_path: Path to the image.

    Returns:
        Image information.
    """
    load_command = f"docker image load -i {image_path}"
    result = subprocess.run(
        load_command, shell=True, check=True, capture_output=True
    )
    image_name = result.stdout.decode().split()[2]

    inspect_command = f"docker image inspect -f json {image_name}"
    result = subprocess.run(
        inspect_command, shell=True, check=True, capture_output=True
    )
    image_info = json.loads(result.stdout.decode())[0]
    return image_info


def docker_pull_image(
    image_name: str,
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
) -> None:
    """Pulls an image from the remote Docker registry.

    Args:
        image_name: Image name.
        docker_metadata: Docker registry metadata.
    """
    docker_login(docker_metadata)
    remote_repo, tag = get_remote_image_tag(image_name, docker_metadata)

    if not tag:
        image_tag = remote_repo
    else:
        image_tag = f"{remote_repo}:{tag}"

    pull_command = f"docker pull {image_tag}"
    subprocess.run(pull_command, shell=True, check=True)


def docker_push_image(
    image_name: str,
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
) -> None:
    """Pushes an image to the remote Docker registry.

    Args:
        image_name: Image name.
        docker_metadata: Docker registry metadata.
    """
    docker_login(docker_metadata)
    remote_repo, tag = get_remote_image_tag(image_name, docker_metadata)

    if not tag:
        image_tag = remote_repo
    else:
        image_tag = f"{remote_repo}:{tag}"

    # Add new tag to the image
    tag_command = f"docker tag {image_name} {image_tag}"
    subprocess.run(tag_command, shell=True, check=True)

    push_command = f"docker push {image_tag}"
    subprocess.run(push_command, shell=True, check=True)


def image_exists(image_name: str) -> bool:
    """Checks if an image exists in the local Docker registry.

    Args:
        image_name: Image name.

    Returns:
        True if the image exists, False otherwise.
    """
    check_command = f"docker inspect {image_name}"
    result = subprocess.run(check_command, shell=True)
    return result.returncode == 0


def docker_run_container(
    image_name: str,
    run_args: str = "",
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
) -> None:
    """Runs a container from an image.

    Args:
        image_name: Image name.
        run_args: Arguments for the run command. Defaults to empty string.
        docker_metadata: Docker registry metadata.
    """
    docker_login(docker_metadata)
    remote_repo, tag = get_remote_image_tag(image_name, docker_metadata)

    if not tag:
        image_tag = remote_repo
    else:
        image_tag = f"{remote_repo}:{tag}"

    # Check if the image exists
    if not image_exists(image_tag):
        docker_pull_image(image_name, docker_metadata)

    run_command = f"docker run {run_args} {image_tag}"
    subprocess.run(run_command, shell=True, check=True)


def docker_stop_container(container_id: str) -> None:
    """Stops a container.

    Args:
        container_id: Container ID.
    """
    stop_command = f"docker stop {container_id}"
    subprocess.run(stop_command, shell=True, check=True)


def delete_image(image_id: str) -> None:
    """Deletes an image in local Docker registry.

    Args:
        image_id: Image ID.
    """
    delete_command = f"docker rmi {image_id}"
    subprocess.run(delete_command, shell=True, check=True)
