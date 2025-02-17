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
) -> None:
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


def inspect_image(image_name: str) -> Dict[str, Any]:
    """Inspects an image.

    Args:
        image_name: Image name.

    Returns:
        Image information.
    """
    inspect_command = f"docker image inspect -f json {image_name}"
    result = subprocess.run(
        inspect_command, shell=True, check=True, capture_output=True
    )
    return json.loads(result.stdout.decode())[0]


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

    image_info = inspect_image(image_name)
    return image_info


def stream_save_image(image_name: str):
    """Streams the image file.

    Args:
        image_name: Image name.

    Raises:
        subprocess.CalledProcessError: If the subprocess fails.

    Yields:
        Image file chunks.
    """
    save_command = f"docker save {image_name}"
    process = subprocess.Popen(
        save_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while True:
        chunk = process.stdout.read(4096)  # Read 4KB at a time
        if not chunk:
            break
        yield chunk

    process.wait()
    if process.returncode != 0:
        error_message = process.stderr.read().decode()
        raise subprocess.CalledProcessError(
            process.returncode, save_command, error_message
        )


def docker_pull_image(
    image_name: str,
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
) -> str:
    """Pulls an image from the remote Docker registry.

    Args:
        image_name: Image name.
        docker_metadata: Docker registry metadata.

    Returns:
        Image tag.
    """
    docker_login(docker_metadata)
    remote_repo, tag = get_remote_image_tag(image_name, docker_metadata)

    if not tag:
        image_tag = remote_repo
    else:
        image_tag = f"{remote_repo}:{tag}"

    pull_command = f"docker pull {image_tag}"
    subprocess.run(pull_command, shell=True, check=True)
    return image_tag


def docker_stream_push_image(
    image_name: str,
    docker_metadata: DockerRegistryMetadata = DockerRegistryMetadata(),
):
    """Pushes an image to the remote Docker registry using a stream.

    Args:
        image_name: Image name.
        docker_metadata: Docker registry metadata.

    Raises:
        subprocess.CalledProcessError: If the subprocess fails.

    Yields:
        Docker logs output.
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
    process = subprocess.Popen(
        push_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in iter(process.stdout.readline, ""):
        yield line.strip()

    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        error_message = process.stderr.read().decode()
        raise subprocess.CalledProcessError(
            process.returncode, push_command, error_message
        )


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
) -> str:
    """Runs a container from an image.

    Args:
        image_name: Image name.
        run_args: Arguments for the run command. Defaults to empty string.
        docker_metadata: Docker registry metadata.

    Returns:
        Container ID.
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

    run_command = f"docker run -d {run_args} {image_tag}"
    result = subprocess.run(
        run_command, shell=True, check=True, capture_output=True
    )
    container_id = result.stdout.decode().strip()
    return container_id


def docker_stop_container(container_id: str) -> None:
    """Stops and deletes a container.

    Args:
        container_id: Container ID.
    """
    stop_command = f"docker container stop {container_id}"
    subprocess.run(stop_command, shell=True, check=True)
    delete_command = f"docker container rm {container_id}"
    subprocess.run(delete_command, shell=True, check=True)


def delete_image(image_id: str) -> None:
    """Deletes an image in local Docker registry.

    Args:
        image_id: Image ID.
    """
    delete_command = f"docker rmi {image_id}"
    subprocess.run(delete_command, shell=True, check=True)


def clean_local_docker_registry() -> None:
    """Cleans the local Docker registry."""
    delete_containers_command = (
        "docker rm $(docker ps -aq -f status=exited) 2>/dev/null"
    )
    subprocess.run(delete_containers_command, shell=True, check=True)
    delete_images_command = (
        'docker rmi $(docker images -q --filter "dangling=true") -f '
        "2>/dev/null"
    )
    subprocess.run(delete_images_command, shell=True, check=True)
