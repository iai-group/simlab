"""Documentation routes."""

from flask import Blueprint, Response, jsonify, request, send_file

from connectors.mongo.utils import find_records
from webapp.backend.app import mongo_connector

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
        return Response("Task not found", 400)
    return jsonify(task), 200


@docs.route("/metrics", methods=["GET"])
def metrics() -> Response:
    """Returns a list of available metrics in SimLab."""
    assert request.method == "GET", "Invalid request method"

    metrics = find_records(mongo_connector, "metrics", {})
    if not metrics:
        return Response("No metrics found", 400)

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
