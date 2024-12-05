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


def test_tasks(flask_client: FlaskClient) -> None:
    """Tests the tasks route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/tasks")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert all(
        task.get("name") and task.get("description") for task in json_data
    )


def test_task(flask_client: FlaskClient) -> None:
    """Tests the task route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/tasks/crs")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0].get("name") == "crs"
    assert json_data[0].get("description") == "CRS Evaluation"


def test_task_not_found(flask_client: FlaskClient) -> None:
    """Tests the task route when the task is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/tasks/unknown")
    assert response.status_code == 400


def test_metrics(flask_client: FlaskClient) -> None:
    """Tests the metrics route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/metrics")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert all(
        metric.get("name") and metric.get("description")
        for metric in json_data
    )


def test_metric(flask_client: FlaskClient) -> None:
    """Tests the metric route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/metrics/success_rate")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0].get("name") == "success_rate"
    assert json_data[0].get("description") == "Success rate"


def test_metric_not_found(flask_client: FlaskClient) -> None:
    """Tests the metric route when the metric is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/metrics/unknown")
    assert response.status_code == 400


def test_agents(flask_client: FlaskClient) -> None:
    """Tests the agents route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/agents")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all(
        key in ["id", "tags", "labels"]
        for agent in data
        for key in agent.keys()
    )


def test_agent(flask_client: FlaskClient) -> None:
    """Tests the agent route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/agents/agent1")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("id") == "agent1"
    assert data.get("tags") == ["crs"]
    assert data.get("labels") == {
        "type": "agent",
        "agent_id": "agent1",
    }


def test_agent_not_found(flask_client: FlaskClient) -> None:
    """Tests the agent route when the agent is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/agents/unknown")
    assert response.status_code == 400


def test_simulators(flask_client: FlaskClient) -> None:
    """Tests the simulators route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/simulators")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all(
        key in ["id", "tags", "labels"]
        for simulator in data
        for key in simulator.keys()
    )


def test_simulator(flask_client: FlaskClient) -> None:
    """Tests the simulator route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/simulators/simulator1")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("id") == "simulator1"
    assert data.get("tags") == ["us"]
    assert data.get("labels") == {
        "type": "simulator",
        "simulator_id": "simulator1",
    }


def test_simulator_not_found(flask_client: FlaskClient) -> None:
    """Tests the simulator route when the simulator is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/simulators/unknown")
    assert response.status_code == 400
