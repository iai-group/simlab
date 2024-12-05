"""Documentation routes."""

from flask import Blueprint, Response, jsonify, request, send_file

from connectors.docker.utils import find_images
from connectors.mongo.utils import find_records
from webapp.backend.app import docker_registry_connector, mongo_connector

docs = Blueprint("documentation", __name__)


@docs.route("/template-agent-api", methods=["GET"])
def template_agent_api() -> Response:
    """Returns the Swagger UI for the template agent API."""
    assert request.method == "GET", "Invalid request method"
    return send_file("data/swagger/conv_agent_api.json"), 200


@docs.route("/template-simulator-api", methods=["GET"])
def template_simulator_api() -> Response:
    """Returns the Swagger UI for the template simulator API."""
    assert request.method == "GET", "Invalid request method"
    return send_file("data/swagger/user_simulator_api.json"), 200


@docs.route("/tasks", methods=["GET"])
def tasks() -> Response:
    """Returns a list of available tasks in SimLab."""
    assert request.method == "GET", "Invalid request method"

    tasks = find_records(mongo_connector, "tasks", {})

    if not tasks:
        return Response("No tasks found", 400)

    return jsonify(tasks), 200


@docs.route("/tasks/<task_id>", methods=["GET"])
def task(task_id: str) -> Response:
    """Returns the details of a task."""
    assert request.method == "GET", "Invalid request method"

    task = find_records(mongo_connector, "tasks", {"name": task_id})

    if len(task) > 1:
        return Response("Multiple tasks found", 500)

    if not task:
        return Response("Task not found", 404)
    return jsonify(task), 200


@docs.route("/metrics", methods=["GET"])
def metrics() -> Response:
    """Returns a list of available metrics in SimLab."""
    assert request.method == "GET", "Invalid request method"

    metrics = find_records(mongo_connector, "metrics", {})
    if not metrics:
        return Response("No metrics found", 404)

    return jsonify(metrics), 200


@docs.route("/metrics/<metric_id>", methods=["GET"])
def metric(metric_id: str) -> Response:
    """Returns the details of a metric in SimLab."""
    assert request.method == "GET", "Invalid request method"

    metric = find_records(mongo_connector, "metrics", {"name": metric_id})

    if len(metric) > 1:
        return Response("Multiple metrics found", 500)

    if not metric:
        return Response("Metric not found", 400)

    return jsonify(metric), 200


@docs.route("/agents", methods=["GET"])
def agents() -> Response:
    """Returns a list of available agents in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    agents = find_images(docker_registry_connector, {"label": "type=agent"})

    if not agents:
        return Response("No agents found", 400)

    agent_list = [
        {
            "id": agent.id,
            "tags": agent.tags,
            "labels": agent.labels,
        }
        for agent in agents
    ]
    return jsonify(agent_list), 200


@docs.route("/agents/<agent_id>", methods=["GET"])
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


@docs.route("/simulators", methods=["GET"])
def simulators() -> Response:
    """Returns a list of available simulators in Docker registry."""
    assert request.method == "GET", "Invalid request method"

    simulators = find_images(
        docker_registry_connector, {"label": "type=simulator"}
    )
    if not simulators:
        return Response("No simulators found", 400)

    simulator_list = [
        {
            "id": simulator.id,
            "tags": simulator.tags,
            "labels": simulator.labels,
        }
        for simulator in simulators
    ]
    return jsonify(simulator_list), 200


@docs.route("/simulators/<simulator_id>", methods=["GET"])
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
