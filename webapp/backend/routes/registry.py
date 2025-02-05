"""Routes interacting with the registry."""

import os
import tempfile

from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, request, send_file
from flask_login import login_required

from connectors.docker.utils import get_image
from connectors.mongo.utils import find_records
from webapp.backend.app import docker_registry_connector, mongo_connector
from webapp.backend.async_tasks.celery_worker import celery, upload_image_task

registry = Blueprint("registry", __name__)


@registry.route("/agents", methods=["GET"])
def agents() -> Response:
    """Returns a list of available agents in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    agents = find_records(mongo_connector, "system_images", {"type": "agent"})

    if not agents:
        return Response("No agents found", 200)

    agent_list = [
        {
            "id": agent.name,
            "tag": agent.tag,
            "description": agent.get("description", None),
            "author": agent.get("author", None),
            "version": agent.get("version", None),
            "added": agent.get("added", None),
        }
        for agent in agents
    ]
    return jsonify(agent_list), 200


@registry.route("/agents/<agent_id>", methods=["GET"])
def agent(agent_id: str) -> Response:
    """Returns the details of an agent."""
    assert request.method == "GET", "Invalid request method"

    agent = find_records(
        mongo_connector,
        "system_images",
        {"$or": [{"_id": agent_id}, {"tag": agent_id}], "type": "agent"},
    )

    if len(agent) > 1:
        return Response("Multiple agents found", 500)

    if not agent:
        return Response("Agent not found", 400)

    return (
        jsonify(
            {
                "id": agent[0].name,
                "tag": agent[0].tag,
                "description": agent[0].get("description", None),
                "author": agent[0].get("author", None),
                "version": agent[0].get("version", None),
                "added": agent[0].get("added", None),
            }
        ),
        200,
    )


@registry.route("/simulators", methods=["GET"])
def simulators() -> Response:
    """Returns a list of available simulators in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    simulators = find_records(
        mongo_connector, "system_images", {"type": "simulator"}
    )
    if not simulators:
        return Response("No simulators found", 200)

    simulator_list = [
        {
            "id": simulator.name,
            "tag": simulator.tag,
            "description": simulator.get("description", None),
            "author": simulator.get("author", None),
            "version": simulator.get("version", None),
            "added": simulator.get("added", None),
        }
        for simulator in simulators
    ]
    return jsonify(simulator_list), 200


@registry.route("/simulators/<simulator_id>", methods=["GET"])
def simulator(simulator_id: str) -> Response:
    """Returns the details of a simulator."""
    assert request.method == "GET", "Invalid request method"

    simulator = find_records(
        mongo_connector,
        "system_images",
        {
            "$or": [{"_id": simulator_id}, {"tag": simulator_id}],
            "type": "simulator",
        },
    )

    if len(simulator) > 1:
        return Response("Multiple simulators found", 500)

    if not simulator:
        return Response("Simulator not found", 400)

    return (
        jsonify(
            {
                "id": simulator[0].name,
                "tag": simulator[0].tag,
                "description": simulator[0].get("description", None),
                "author": simulator[0].get("author", None),
                "version": simulator[0].get("version", None),
                "added": simulator[0].get("added", None),
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

    task = upload_image_task.apply_async(args=[image_name, file_path])
    return (
        jsonify({"message": "Image upload started", "task_id": task.id}),
        202,
    )


@registry.route("/upload-image-status", methods=["POST"])
@login_required
def upload_image_status() -> Response:
    """Returns the status of an image upload task."""
    assert request.method == "POST", "Invalid request method"

    task_id = request.get_json().get("task_id")
    if not task_id:
        return Response("Task ID not provided", 400)

    task = AsyncResult(task_id, app=celery)
    if task.state == "SUCCESS":
        return jsonify({"status": "SUCCESS", "message": "Image uploaded"}), 200
    if task.state == "FAILURE":
        return (
            jsonify(
                {
                    "status": "FAILURE",
                    "message": "Failed to upload image",
                    "error": str(task.info),
                }
            ),
            500,
        )

    return jsonify({"status": task.state}), 202


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
