"""Routes to interact with the experiment results."""

from bson import ObjectId
from flask import Blueprint, Response, jsonify, request
from flask_login import current_user, login_required

from connectors.mongo.utils import find_records
from webapp.backend.app import mongo_connector

results = Blueprint("results", __name__)


@results.route("/results/<task_id>", methods=["GET"])
def get_results(task_id: str) -> Response:
    """Returns the results of a task.

    Args:
        task_id: Task ID.

    Returns:
        Public results of the task.
    """
    assert request.method == "GET", "Invalid request method"

    result_records = find_records(
        mongo_connector,
        "evaluation_results",
        {"task_id": ObjectId(task_id), "public": True},
    )

    if not result_records or len(result_records) == 0:
        return jsonify({"message": "No results found for this task."}), 404

    return jsonify({"results": result_records}), 200


@results.route("/results-user", methods=["GET"])
@login_required
def get_results_user() -> Response:
    """Returns the results of the current user.

    Returns:
        Results of the current user.
    """
    assert request.method == "GET", "Invalid request method"

    username = current_user.username

    result_records = []

    # Find user runs in MongoDB
    user_run_names = find_records(
        mongo_connector, "runs", {"username": username}
    )

    if user_run_names:
        result_records = find_records(
            mongo_connector,
            "evaluation_results",
            {"run_name": {"$in": [run["name"] for run in user_run_names]}},
        )

    if not result_records or len(result_records) == 0:
        return jsonify({"message": "No results found for this user."}), 404

    return jsonify({"results": result_records}), 200
