"""Routes interacting with the registry."""

import subprocess
import tempfile

from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, request
from flask_login import login_required

from connectors.docker.commands import docker_pull_image, stream_save_image
from connectors.mongo.utils import find_records
from webapp.backend.app import mongo_connector
from webapp.backend.async_tasks.celery_worker import celery, upload_image_task

registry = Blueprint("registry", __name__)


@registry.route("/agents", methods=["GET"])
def agents() -> Response:
    """Returns a list of available agents in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    agents = find_records(mongo_connector, "system_images", {"type": "agent"})

    if not agents:
        return jsonify({"message": "No agents found"}), 200

    agent_list = [
        {
            "id": agent.get("name", None),
            "image_name": agent.get("image_name", None),
            "tag": agent.get("tag", None),
            "description": agent.get("description", None),
            "type": agent.get("type", None),
            "author": agent.get("author", None),
            "version": agent.get("version", None),
        }
        for agent in agents
    ]
    return jsonify(agent_list), 200


@registry.route("/agent", methods=["POST"])
def agent() -> Response:
    """Returns the details of an agent."""
    assert request.method == "POST", "Invalid request method"

    image_name = request.get_json().get("image_name")

    if not image_name:
        return jsonify({"error": "Image name not provided"}), 400

    agents = find_records(
        mongo_connector,
        "system_images",
        {"image_name": image_name, "type": "agent"},
    )

    if len(agents) > 1:
        return jsonify({"error": "Multiple agents found"}), 500

    if not agents:
        return jsonify({"error": "Agent not found"}), 400

    agent = agents[0]

    return (
        jsonify(
            {
                "id": agent.get("name", None),
                "image_name": agent.get("image_name", None),
                "tag": agent.get("tag", None),
                "description": agent.get("description", None),
                "type": agent.get("type", None),
                "author": agent.get("author", None),
                "version": agent.get("version", None),
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
        return jsonify({"message": "No simulators found"}), 200

    simulator_list = [
        {
            "id": simulator.get("name", None),
            "image_name": simulator.get("image_name", None),
            "tag": simulator.get("tag", None),
            "description": simulator.get("description", None),
            "type": simulator.get("type", None),
            "author": simulator.get("author", None),
            "version": simulator.get("version", None),
        }
        for simulator in simulators
    ]
    return jsonify(simulator_list), 200


@registry.route("/simulator", methods=["POST"])
def simulator() -> Response:
    """Returns the details of a simulator."""
    assert request.method == "POST", "Invalid request method"

    image_name = request.get_json().get("image_name")

    if not image_name:
        return jsonify({"error": "Image name not provided"}), 400

    simulators = find_records(
        mongo_connector,
        "system_images",
        {"image_name": image_name, "type": "simulator"},
    )

    if len(simulators) > 1:
        return jsonify({"error": "Multiple simulators found"}), 500

    if not simulators:
        return jsonify({"error": "Simulator not found"}), 400

    simulator = simulators[0]

    return (
        jsonify(
            {
                "id": simulator.get("name", None),
                "image_name": simulator.get("image_name", None),
                "tag": simulator.get("tag", None),
                "description": simulator.get("description", None),
                "type": simulator.get("type", None),
                "author": simulator.get("author", None),
                "version": simulator.get("version", None),
            }
        ),
        200,
    )


@registry.route("/image", methods=["POST"])
def find_image() -> Response:
    """Returns the details of an image given its name."""
    assert request.method == "POST", "Invalid request method"

    image_name = request.get_json().get("image")

    images_metadata = find_records(
        mongo_connector, "system_images", {"image_name": image_name}
    )

    if not images_metadata:
        return jsonify({"error": "Image not found"}), 400

    if len(images_metadata) > 1:
        return jsonify({"error": "Multiple images found"}), 500

    image_metadata = images_metadata[0]
    image = f"{image_metadata.get('repository')}:{image_metadata.get('tag')}"

    participant_id = image_metadata.get("name")
    participant_description = image_metadata.get("description", "")
    if image_metadata.get("type") == "agent":
        participant_class = image_metadata.get("class", "WrapperAgent")
    elif image_metadata.get("type") == "simulator":
        participant_class = image_metadata.get("class", "WrapperUserSimulator")

    if not participant_id:
        return jsonify({"error": "ID not found in image labels"}), 500

    participant_config = {
        "class_name": participant_class,
        "arguments": {"id": participant_id},
        "image": image,
        "description": participant_description,
    }

    return jsonify(participant_config), 200


@registry.route("/upload-image", methods=["POST"])
@login_required
def upload_image() -> Response:
    """Uploads an image to the Docker registry."""
    assert request.method == "POST", "Invalid request method"

    if "file" not in request.files:
        return jsonify({"error": "No file submitted"}), 400
    if "image_name" not in request.form:
        return jsonify({"error": "No image name submitted"}), 400

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
        return jsonify({"error": "Task ID not provided"}), 400

    task = AsyncResult(task_id, app=celery)
    if task.state == "PROGRESS":
        return (
            jsonify({"status": "PROGRESS", "log": task.info.get("log", "")}),
            202,
        )
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

    image_name = request.get_json().get("image_name")

    if not image_name:
        return jsonify({"error": "Image name not provided"}), 400

    try:
        # Pull the image first
        image_pulled = docker_pull_image(image_name)

        def generate():
            """Generates the image file."""
            yield from stream_save_image(image_pulled)

        response = Response(generate(), content_type="application/x-tar")
        response.headers[
            "Content-Disposition"
        ] = f"attachment; filename={image_name.replace(':', '_')}.tar"

        return response

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to download image: {str(e)}"}), 500
