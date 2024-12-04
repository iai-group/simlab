"""Tests for documentation routes."""

from flask.testing import FlaskClient


def test_template_agent_api(flask_client: FlaskClient) -> None:
    """Tests the template_agent_api route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/template-agent-api")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data.get("info", {}).get("title") == "Template Agent API"
    assert all(
        route in ["/receive_utterance", "/configure"]
        for route in json_data.get("paths", {}).keys()
    )


def test_template_simulator_api(flask_client: FlaskClient) -> None:
    """Tests the template_simulator_api route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/template-simulator-api")
    assert response.status_code == 200
    json_data = response.get_json()
    assert (
        json_data.get("info", {}).get("title") == "Template User Simulator API"
    )
    assert all(
        route in ["/receive_utterance", "/configure"]
        for route in json_data.get("paths", {}).keys()
    )
