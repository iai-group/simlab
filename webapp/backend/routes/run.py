"""Routes related to runs."""

import datetime
import os
from typing import Any, Dict, List

from bson import ObjectId
from flask import Blueprint, Response, json, jsonify, request
from flask_login import current_user, login_required

from connectors.mongo.utils import delete_records, find_records, insert_record
from webapp.backend.app import DATA_FOLDER, jenkins_job_manager, mongo_connector

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


def _submit_experiment(
    username: str,
    experiment_name: str,
    task_id: str,
    configuration_path: str,
    job_name="run_execution",
) -> None:
    """Submits an experiment to the Jenkins server.

    Args:
        username: Username of the user.
        experiment_name: Name of the experiment.
        task_id: Task ID.
        configuration_path: Path to the configuration file.
        job_name: Name of the Jenkins job.
    """
    # Link run configuration file to run in MongoDB
    insert_record(
        connector=mongo_connector,
        collection="runs",
        record={
            "username": username,
            "run_name": experiment_name,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",
            "task_id": task_id,
            "run_configuration_file": configuration_path,
        },
    )

    jenkins_job_manager.submit_job(configuration_path, job_name=job_name)


def _save_configuration(username: str, configuration: Dict[str, Any]) -> str:
    """Saves the configuration to a file.

    Args:
        username: Username of the user.
        configuration: Configuration to save.

    Returns:
        Path to the saved configuration file.
    """
    configuration_path = os.path.join(
        "simlab",
        "configs",
        configuration["task"]["_id"],
        f"{username}_{configuration['name']}.json",
    )
    full_path = os.path.join(DATA_FOLDER, configuration_path)
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path))
    with open(full_path, "w") as f:
        json.dump(configuration, f)
    return configuration_path


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

    run_name = data.get("run_name")
    if not run_name:
        return jsonify({"message": "Run name not provided."}), 400
    run_name = run_name.strip().replace(" ", "_")
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

    # Save run configuration
    run_configuration_path = _save_configuration(username, run_configuration)

    try:
        # Send run request to Jenkins server with run configuration file
        _submit_experiment(
            username,
            run_configuration["name"],
            run_configuration["task"]["_id"],
            run_configuration_path,
            job_name="run_execution",
        )
    except Exception as e:
        return (
            jsonify({"message": f"Error while submitting job: {str(e)}"}),
            500,
        )

    return jsonify({"message": "Run request created."}), 201


@run.route("/run-baseline", methods=["POST"])
@login_required
def run_baseline() -> Response:
    """Submits a baseline run request."""
    assert request.method == "POST", "Invalid request method"

    username = current_user.username

    # Parse and load baseline configuration file from the request
    try:
        if "configuration" not in request.files:
            return (
                jsonify({"message": "Configuration file not provided."}),
                400,
            )

        file = request.files["configuration"]
        if file.filename == "":
            return jsonify({"message": "No file selected."}), 400

        # Read the file and parse JSON
        baseline_configuration = json.load(file)
    except Exception as e:
        return (
            jsonify({"message": f"Invalid configuration file: {str(e)}"}),
            400,
        )

    # Check that run name is unique for user
    run_name = baseline_configuration.get("name")
    if not run_name:
        return jsonify({"message": "Run name not provided."}), 400

    run_name = run_name.strip().replace(" ", "_")

    if not all(
        key in baseline_configuration.keys()
        for key in ["task", "agents", "user_simulators"]
    ):
        return (
            jsonify(
                {
                    "message": "Configuration file is missing required fields "
                    "(task, agents, user_simulators)."
                }
            ),
            400,
        )

    # Save baseline configuration to file
    baseline_configuration_path = _save_configuration(
        username, baseline_configuration
    )

    try:
        # Submit baseline run request
        _submit_experiment(
            username,
            run_name,
            baseline_configuration.get("task", {}).get("_id"),
            baseline_configuration_path,
        )
    except Exception as e:
        return (
            jsonify({"message": f"Error while submitting job: {str(e)}"}),
            500,
        )

    return jsonify({"message": "Baseline run request created."}), 201


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
