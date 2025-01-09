"""Tests for run related routes."""

from flask_login import FlaskLoginClient

from connectors.mongo.utils import find_records
from tests.backend.conftest import mongo_connector


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
        "/run-request", json={"name": "invalid_test_run"}
    )
    assert response.status_code == 400
    assert response.json["message"] == "Run name not provided."


def test_run_request_duplicate_name(
    flask_logged_client: FlaskLoginClient,
) -> None:
    """Tests run_request route with duplicate run name."""
    response = flask_logged_client.post(
        "/run-request",
        json={
            "run_name": "test_run",
        },
    )
    assert response.status_code == 400
    assert response.json["message"] == "Run name already exists."


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
