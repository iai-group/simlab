"""Tests for run related routes."""

import pytest
from bson import ObjectId
from flask_login import FlaskLoginClient

from connectors.mongo.utils import find_records
from tests.backend.conftest import mongo_connector
from webapp.backend.routes.run import (
    parse_metrics,
    parse_task,
    validate_configuration_file_extension,
)


def test_validate_configuration_file_extension():
    """Tests validate_configuration_file_extension."""
    assert validate_configuration_file_extension("file.json")
    assert not validate_configuration_file_extension("file.txt")
    assert not validate_configuration_file_extension("file")
    assert not validate_configuration_file_extension("file.json.txt")


def test_parse_task() -> None:
    """Tests parse_task."""
    configuration = {
        "task": {
            "name": "crs",
        }
    }

    task_id = parse_task(configuration)
    assert task_id is not None

    mongo_task_id = find_records(mongo_connector, "tasks", {"name": "crs"})[
        0
    ].get("_id")
    assert task_id == ObjectId(mongo_task_id)


def test_parse_task_no_task_name() -> None:
    """Tests parse_task with no task name."""
    configuration = {}

    with pytest.raises(KeyError):
        parse_task(configuration)


def test_parse_task_task_not_found() -> None:
    """Tests parse_task with task not found."""
    configuration = {
        "task": {
            "name": "unknown",
        }
    }

    with pytest.raises(ValueError):
        parse_task(configuration)


def test_parse_metrics() -> None:
    """Tests parse_metrics."""
    configuration = {
        "metrics": [
            {
                "name": "success_rate",
            }
        ]
    }

    metrics = parse_metrics(configuration)
    assert metrics is not None

    mongo_metric_id = find_records(
        mongo_connector, "metrics", {"name": "success_rate"}
    )[0].get("_id")

    assert metrics["success_rate"] == mongo_metric_id


def test_parse_metrics_no_metrics() -> None:
    """Tests parse_metrics with no metrics."""
    configuration = {}

    with pytest.raises(KeyError):
        parse_metrics(configuration)


def test_parse_metrics_metric_not_found() -> None:
    """Tests parse_metrics with metric not found."""
    configuration = {
        "metrics": [
            {
                "name": "unknown",
            }
        ]
    }

    with pytest.raises(ValueError):
        parse_metrics(configuration)


def test_run_request_unauthorized(flask_client: FlaskLoginClient) -> None:
    """Tests run_request route with unauthorized user."""
    response = flask_client.post("/run-request")
    assert response.status_code == 401


def test_run_request_invalid_method(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_request route with invalid request method."""
    response = flask_logged_client.get("/run-request")
    assert response.status_code == 405


def test_run_request_invalid_form(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_request route with invalid form."""
    response = flask_logged_client.post(
        "/run-request", data={"run_name": "test_run"}
    )
    assert response.status_code == 400
    assert (
        response.json["message"]
        == "Invalid request. Please provide run name and configuration file."
    )


def test_run_request(flask_logged_client: FlaskLoginClient) -> None:
    """Tests run_request route."""
    # TODO: Implement test_run_request
    pass


def test_run_info_unauthorized(flask_client: FlaskLoginClient) -> None:
    """Tests run_info route with unauthorized user."""
    response = flask_client.get("/run-info/675728398dd85617189bd026")
    assert response.status_code == 401


def test_run_info_invalid_method(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_info route with invalid request method."""
    response = flask_logged_client.post("/run-info/675728398dd85617189bd026")
    assert response.status_code == 405


def test_run_info_unknown_run(flask_logged_client: FlaskLoginClient) -> None:
    """Tests run_info route with unknown run."""
    response = flask_logged_client.get("/run-info/675728398dd85617189bd026")
    assert response.status_code == 400
    assert response.json == {"message": "Run not found."}


def test_run_info(flask_logged_client: FlaskLoginClient) -> None:
    """Tests run_info route."""
    run_id = find_records(
        mongo_connector,
        "runs",
        {"username": "test_user", "run_name": "test_run"},
    )[0].get("_id")
    response = flask_logged_client.get(f"/run-info/{str(run_id)}")
    assert response.status_code == 200
    run_info = response.json.get("run_info", {})
    assert run_info["run_name"] == "test_run"
    assert run_info["username"] == "test_user"
    assert all(
        config_key in ["task", "metrics", "agents", "user_simulators"]
        for config_key in run_info["run_configuration"].keys()
    )


def test_run_delete_unauthorized(flask_client: FlaskLoginClient) -> None:
    """Tests run_delete route with unauthorized user."""
    flask_client.post("/logout")
    response = flask_client.delete("/delete-run/675728308dd85617189bd025")
    assert response.status_code == 401


def test_run_delete_invalid_method(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_delete route with invalid request method."""
    response = flask_logged_client.post("/delete-run/675728308dd85617189bd025")
    assert response.status_code == 405


def test_run_delete_unknown_run(flask_logged_client: FlaskLoginClient) -> None:
    """Tests run_delete route with unknown run."""
    response = flask_logged_client.delete(
        "/delete-run/675728308dd85617189bd025"
    )
    assert response.status_code == 500
    assert response.json == {"message": "Failed to delete run."}


def test_run_delete(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_delete route."""
    run_id = find_records(
        mongo_connector,
        "runs",
        {"username": "test_user", "run_name": "test_run2"},
    )[0].get("_id")
    response = flask_logged_client.delete(f"/delete-run/{str(run_id)}")
    assert response.status_code == 200
    assert response.json == {"message": "Run deleted successfully."}
