"""Routes related to a run."""

import ast
import os

from bson import ObjectId
from flask import Blueprint, Response, json, jsonify, request
from flask_login import current_user, login_required

from connectors.mongo.utils import delete_records, find_records, insert_record
from webapp.backend.app import DATA_FOLDER, mongo_connector

run = Blueprint("run", __name__)


@run.route("/run-request", methods=["POST"])
@login_required
def run_request() -> Response:
    """Submits a run request."""
    assert request.method == "POST", "Invalid request method"

    username = current_user.username
    data = request.get_json()

    run_configuration = {}

    # Check that run name is unique for user
    run_name = data.get("run_name")
    if not run_name:
        return jsonify({"message": "Run name not provided."}), 400
    run_name = run_name.strip().replace(" ", "_")

    runs = find_records(
        mongo_connector, "runs", {"username": username, "run_name": run_name}
    )
    if runs:
        return jsonify({"message": "Run name already exists."}), 400

    run_configuration["name"] = run_name

    # Get task configuration
    task = find_records(
        mongo_connector, "tasks", {"_id": ObjectId(data.get("task_id"))}
    )
    if not task or len(task) != 1:
        return jsonify({"message": "Error while retrieving task."}), 500

    run_configuration["task"] = task[0]

    # Get metrics configuration and update it with metrics arguments
    metrics = []
    for metric in data.get("metrics", []):
        metric_configs = find_records(
            mongo_connector, "metrics", {"_id": ObjectId(metric.get("id"))}
        )
        if not metric_configs or len(metric_configs) != 1:
            return jsonify({"message": "Error while retrieving metrics."}), 500

        metric_config = metric_configs[0]
        metric_config.update(
            {"name": metric.get("name", metric_config.get("name"))}
        )
        for arg in metric.get("arguments", []):
            arg_name = arg.get("name")
            # It is assume that arguments with custom types are not supported
            # in the web interface.
            metric_config.get("arguments", {}).update(
                {arg_name: ast.literal_eval(arg.get("value"))}
            )

        metrics.append(metric_config)

    run_configuration["metrics"] = metrics

    run_configuration["agents"] = data.get("agents", [])
    run_configuration["user_simulators"] = data.get("user_simulators", [])

    # Save run configuration to file
    run_configuration_path = os.path.join(
        DATA_FOLDER,
        "configs",
        f"{username}_{run_configuration['name']}.json",
    )
    if not os.path.exists(os.path.dirname(run_configuration_path)):
        os.makedirs(os.path.dirname(run_configuration_path))
    with open(run_configuration_path, "w") as f:
        json.dump(run_configuration, f)

    # Link run configuration file to run in MongoDB
    insert_record(
        connector=mongo_connector,
        collection="runs",
        record={
            "username": username,
            "run_name": run_configuration["name"],
            "run_configuration_file": run_configuration_path,
        },
    )

    # Send run request to Jenkins server with run configuration file
    # TODO: Implement Jenkins server integration
    # See: https://github.com/iai-group/simlab/issues/5

    return jsonify({"message": "Run request created."}), 201


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
