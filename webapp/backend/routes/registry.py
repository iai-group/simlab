"""Routes interacting with the registry."""

import os
import tempfile

from flask import Blueprint, Response, jsonify, request, send_file
from flask_login import login_required

from connectors.docker.utils import find_images, get_image
from webapp.backend.app import docker_registry_connector

registry = Blueprint("registry", __name__)


@registry.route("/agents", methods=["GET"])
def agents() -> Response:
    """Returns a list of available agents in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    agents = find_images(docker_registry_connector, {"label": "type=agent"})

    if not agents:
        return Response("No agents found", 200)

    agent_list = [
        {
            "id": agent.id,
            "tags": agent.tags,
            "labels": agent.labels,
        }
        for agent in agents
    ]
    return jsonify(agent_list), 200


@registry.route("/agents/<agent_id>", methods=["GET"])
def agent(agent_id: str) -> Response:
    """Returns the details of an agent."""
    assert request.method == "GET", "Invalid request method"

    agent = find_images(
        docker_registry_connector,
        {"label": [f"agent_id={agent_id}", "type=agent"]},
    )

    if len(agent) > 1:
        return Response("Multiple agents found", 500)

    if not agent:
        return Response("Agent not found", 400)

    return (
        jsonify(
            {
                "id": agent[0].id,
                "tags": agent[0].tags,
                "labels": agent[0].labels,
            }
        ),
        200,
    )


@registry.route("/simulators", methods=["GET"])
def simulators() -> Response:
    """Returns a list of available simulators in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    simulators = find_images(
        docker_registry_connector, {"label": "type=simulator"}
    )
    if not simulators:
        return Response("No simulators found", 200)

    simulator_list = [
        {
            "id": simulator.id,
            "tags": simulator.tags,
            "labels": simulator.labels,
        }
        for simulator in simulators
    ]
    return jsonify(simulator_list), 200


@registry.route("/simulators/<simulator_id>", methods=["GET"])
def simulator(simulator_id: str) -> Response:
    """Returns the details of a simulator."""
    assert request.method == "GET", "Invalid request method"

    simulator = find_images(
        docker_registry_connector,
        {"label": [f"simulator_id={simulator_id}", "type=simulator"]},
    )

    if len(simulator) > 1:
        return Response("Multiple simulators found", 500)

    if not simulator:
        return Response("Simulator not found", 400)

    return (
        jsonify(
            {
                "id": simulator[0].id,
                "tags": simulator[0].tags,
                "labels": simulator[0].labels,
            }
        ),
        200,
    )


@registry.route("/image", methods=["POST"])
def find_image() -> Response:
    """Returns the details of an image given its name."""
    assert request.method == "POST", "Invalid request method"

    image_name = request.get_json().get("image")
    image = get_image(docker_registry_connector, image_name)

    if not image:
        return Response("Image not found", 400)

    participant_id = image.labels.get("name")
    participant_description = image.labels.get("description", "")
    if image.labels.get("type") == "agent":
        participant_class = image.labels.get("class", "WrapperAgent")
    elif image.labels.get("type") == "simulator":
        participant_class = image.labels.get("class", "WrapperSimulator")

    if not participant_id:
        return Response("ID not found in image labels", 500)

    participant_config = {
        "class_name": participant_class,
        "arguments": {"id": participant_id},
        "image": image_name,
        "description": participant_description,
    }

    return jsonify(participant_config), 200


@registry.route("/upload-image", methods=["POST"])
@login_required
def upload_image() -> Response:
    """Uploads an image to the Docker registry."""
    assert request.method == "POST", "Invalid request method"

    if "file" not in request.files:
        return Response("No file submitted", 400)
    if "image_name" not in request.form:
        return Response("No image name submitted", 400)

    file = request.files.get("file")
    image_name = request.form.get("image_name")

    # Temporary save the file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tar") as temp_file:
        file.save(temp_file.name)
        temp_file.close()
        file_path = temp_file.name

    try:
        docker_registry_connector.client.images.load(open(file_path, "rb"))
        docker_registry_connector.push_image(image_name)
    except Exception as e:
        return (
            jsonify({"error": str(e), "message": "Failed to push image"}),
            500,
        )
    finally:
        # Remove the temporary file
        os.remove(file_path)

    return Response("Image uploaded", 201)


@registry.route("/download-image", methods=["POST"])
@login_required
def download_image() -> Response:
    """Downloads an image from the Docker registry."""
    assert request.method == "POST", "Invalid request method"

    image_name = request.get_json().get("image")

    if not image_name:
        return Response("Image name not provided.", 400)

    try:
        image = docker_registry_connector.pull_image(image_name)

        # Save the image to a temp file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in image:
                temp_file.write(chunk)
            temp_file.close()
    except Exception as e:
        return (
            jsonify({"error": str(e), "message": "Failed to pull image"}),
            500,
        )

    response = send_file(
        temp_file.name, as_attachment=True, download_name=f"{image_name}.tar"
    )

    os.remove(temp_file.name)
    return response
