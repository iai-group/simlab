"""Routes related to runs."""

import os
from typing import Any, Dict, List

from bson import ObjectId
from flask import Blueprint, Response, json, jsonify, request
from flask_login import current_user, login_required

from connectors.mongo.utils import delete_records, find_records, insert_record
from webapp.backend.app import DATA_FOLDER, mongo_connector
from connectors.jenkins.jenkins_job_manager import submit_job 

run = Blueprint("run", __name__)


def _get_previous_task_participants(
    task_id: str, participant_type: str
) -> List[Dict[str, Any]]:
    """Gets configuration task participants of a specific type.

    Args:
        task_id: Task ID.
        participant_type: Participant type.

    Returns:
        List of participants configuration.
    """
    participants = []
    previous_runs = find_records(
        mongo_connector, "runs", {"task_id": ObjectId(task_id)}
    )

    for run in previous_runs:
        if run.get("status") == "successful":
            run_configuration = json.load(open(run["run_configuration_file"]))
            run_participants = (
                run_configuration.get("agents", [])
                if participant_type == "agent"
                else run_configuration.get("user_simulators", [])
            )
            for participant in run_participants:
                if participant not in participants:
                    participants.append(participant)

    return participants


@run.route("/run-request", methods=["POST"])
@login_required
def run_request() -> Response:
    """Submits a run request."""
    assert request.method == "POST", "Invalid request method"

    username = current_user.username
    data = request.get_json()

    run_configuration = {
        "public": data.get("public", True),
    }

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

    system = data.get("system", {})
    system_type = system.pop("type")
    if system_type == "agent":
        run_configuration["agents"] = [system]
        run_configuration["user_simulators"] = _get_previous_task_participants(
            task[0]["_id"], "user_simulator"
        )
    elif system_type == "user_simulator":
        run_configuration["user_simulators"] = [system]
        run_configuration["agents"] = _get_previous_task_participants(
            task[0]["_id"], "agent"
        )

    # Save run configuration to file
    run_configuration_path = os.path.join(
        DATA_FOLDER,
        "configs",
        run_configuration["task"]["_id"],
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
            "status": "pending",
            "task_id": run_configuration["task"]["_id"],
            "run_configuration_file": run_configuration_path,
        },
    )

    # Send run request to Jenkins server with run configuration file
    # TODO: Implement Jenkins server integration
    # See: https://github.com/iai-group/simlab/issues/5
    try:
        submit_job(run_name,run_configuration_path)
    except Exception as e:
        error_message = f"Error submitting job: {str(e)}"
        print(error_message)
        return jsonify({"message": "Job submission failed. : {error_message}"}), 500

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


@run.route("/list-runs/<task_id>", methods=["GET"])
def list_runs(task_id: str) -> Response:
    """Lists runs for a task.

    Args:
        task_id: Task ID.

    Returns:
        All runs associated with the task.
    """
    assert request.method == "GET", "Invalid request method"

    records = find_records(
        mongo_connector, "runs", {"task_id": ObjectId(task_id)}
    )

    return jsonify({"runs": records}), 200


@run.route("/list-runs-user", methods=["GET"])
@login_required
def list_runs_user() -> Response:
    """Lists runs for the current user.

    Returns:
        All runs associated with the current user.
    """
    assert request.method == "GET", "Invalid request method"

    username = current_user.username

    records = find_records(mongo_connector, "runs", {"username": username})

    return jsonify({"runs": records}), 200
