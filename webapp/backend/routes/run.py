"""Routes related to a run."""

from typing import Any, Dict

from bson import ObjectId
from flask import Blueprint, Response, json, jsonify, request
from flask_login import current_user, login_required

from connectors.mongo.utils import delete_records, find_records, insert_record
from webapp.backend.app import mongo_connector

run = Blueprint("run", __name__)


def validate_configuration_file_extension(filename: str) -> bool:
    """Validates that the file extension is JSON."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "json"


def parse_task(configuration: Dict[str, Any]) -> ObjectId:
    """Parses task from configuration.

    Args:
        configuration: Configuration.

    Raises:
        KeyError: If task is not defined in configuration.
        ValueError: If task or task ID is not found.
        RuntimeError: If multiple tasks are found.

    Returns:
        Task ID from MongoDB.
    """
    task_name = configuration.get("task", {}).get("name", None)

    if not task_name:
        raise KeyError("Task name not found in configuration.")

    tasks = find_records(mongo_connector, "tasks", {"name": task_name})

    if not tasks:
        raise ValueError(f"Task {task_name} not found.")
    elif len(tasks) > 1:
        raise RuntimeError(f"Multiple tasks found for {task_name}.")

    task_id = tasks[0].get("_id")

    if not task_id:
        raise ValueError(f"Task ID not found for {task_name}.")

    return task_id


def parse_metrics(configuration: Dict[str, Any]) -> Dict[str, ObjectId]:
    """Parses metrics from configuration.

    Args:
        configuration: Configuration.

    Raises:
        KeyError: If metrics are not defined in configuration.
        ValueError: If metric or metric ID is not found.
        RuntimeError: If multiple metrics are found.

    Returns:
        Dictionary of metric names and IDs from MongoDB.
    """
    metrics = configuration.get("metrics", [])

    if not metrics:
        raise KeyError("Metrics not found in configuration.")

    metrics_dict = {}

    metrics_records = find_records(
        mongo_connector,
        "metrics",
        {"name": {"$in": [metric["name"] for metric in metrics]}},
    )

    if not metrics_records:
        raise ValueError("Metrics not found.")
    elif len(metrics_records) != len(metrics):
        raise RuntimeError("Multiple metrics found.")

    for metric in metrics_records:
        id = metric.get("_id")
        if not id:
            raise ValueError(f"Metric ID not found for {metric['name']}.")
        metrics_dict[metric["name"]] = metric["_id"]

    return metrics_dict


@run.route("/run-request", methods=["POST"])
@login_required
def run_request() -> Response:
    """Submits a run request."""
    assert request.method == "POST", "Invalid request method"

    username = current_user.username
    run_name = request.form.get("run_name")
    run_configuration_file = request.files.get("run_configuration_file", None)

    if (
        not run_name
        or not run_configuration_file
        or not validate_configuration_file_extension(
            run_configuration_file.filename
        )
    ):
        return (
            jsonify(
                {
                    "message": (
                        "Invalid request. Please provide run name and "
                        "configuration file."
                    )
                }
            ),
            400,
        )

    # Load run configuration from file
    try:
        run_configuration = json.load(run_configuration_file)
    except json.JSONDecodeError:
        return (
            jsonify(
                {
                    "message": (
                        "Invalid run configuration. Please check documentation "
                        "for correct format."
                    )
                }
            ),
            400,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    # Retrieve task and metrics ids from MongoDB
    try:
        run_configuration["task"]["_id"] = parse_task(run_configuration)
        metric_ids = parse_metrics(run_configuration)
        for metric in run_configuration["metrics"]:
            metric["_id"] = metric_ids[metric["name"]]
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    # Save run configuration to MongoDB
    run_id = insert_record(
        connector=mongo_connector,
        collection="runs",
        record={
            "username": username,
            "run_name": run_name,
            "run_configuration": run_configuration,
        },
    )

    # Send run request to Jenkins server
    # TODO: Implement Jenkins server integration
    # See: https://github.com/iai-group/simlab/issues/5

    return (
        jsonify(
            {
                "message": f"Run {run_name} submitted successfully.",
                "run_id": run_id,
            }
        ),
        200,
    )


@run.route("/run-info/<run_id>", methods=["GET"])
@login_required
def run_info(run_id: str) -> Response:
    """Returns information about a run."""
    assert request.method == "GET", "Invalid request method"

    username = current_user.username

    # Find run in MongoDB
    records = find_records(
        mongo_connector,
        "runs",
        {"_id": ObjectId(run_id), "username": username},
    )

    if not records:
        return jsonify({"message": "Run not found."}), 400
    elif len(records) > 1:
        return jsonify({"message": "Multiple runs found."}), 500

    run_info = records[0]
    return jsonify({"run_info": run_info}), 200


@run.route("/delete-run/<run_id>", methods=["DELETE"])
@login_required
def delete_run(run_id: str) -> Response:
    """Deletes a run."""
    assert request.method == "DELETE", "Invalid request method"

    username = current_user.username

    b_success = delete_records(
        mongo_connector,
        "runs",
        {"_id": ObjectId(run_id), "username": username},
    )

    if not b_success:
        return jsonify({"message": "Failed to delete run."}), 500

    return jsonify({"message": "Run deleted successfully."}), 200
