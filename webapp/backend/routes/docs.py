"""Documentation routes."""

from flask import Blueprint, Response, request, send_file

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
    """Returns a list of available tasks."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/tasks/<task_id>", methods=["GET"])
def task(task_id: str) -> Response:
    """Returns the details of a task."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/agents", methods=["GET"])
def agents() -> Response:
    """Returns a list of available agents."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/agents/<agent_id>", methods=["GET"])
def agent(agent_id: str) -> Response:
    """Returns the details of an agent."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/simulators", methods=["GET"])
def simulators() -> Response:
    """Returns a list of available simulators."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/simulators/<simulator_id>", methods=["GET"])
def simulator(simulator_id: str) -> Response:
    """Returns the details of a simulator."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/metrics", methods=["GET"])
def metrics() -> Response:
    """Returns a list of available metrics."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)


@docs.route("/metrics/<metric_id>", methods=["GET"])
def metric(metric_id: str) -> Response:
    """Returns the details of a metric."""
    assert request.method == "GET", "Invalid request method"
    return Response("Not implemented", 501)
