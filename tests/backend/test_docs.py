"""Tests for documentation routes."""

from flask_login import FlaskLoginClient


def test_template_agent_api(flask_client: FlaskLoginClient) -> None:
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


def test_template_simulator_api(flask_client: FlaskLoginClient) -> None:
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


def test_tasks(flask_client: FlaskLoginClient) -> None:
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


def test_task(flask_client: FlaskLoginClient) -> None:
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


def test_task_not_found(flask_client: FlaskLoginClient) -> None:
    """Tests the task route when the task is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/tasks/unknown")
    assert response.status_code == 400


def test_metrics(flask_client: FlaskLoginClient) -> None:
    """Tests the metrics route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/metrics")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert all(
        metric.get("name") and metric.get("description") for metric in json_data
    )


def test_metric(flask_client: FlaskLoginClient) -> None:
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


def test_metric_not_found(flask_client: FlaskLoginClient) -> None:
    """Tests the metric route when the metric is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/metrics/unknown")
    assert response.status_code == 400


def test_agents(flask_client: FlaskLoginClient) -> None:
    """Tests the agents route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/agents")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all(
        key
        in [
            "id",
            "tag",
            "author",
            "version",
            "type",
            "image_name",
            "port",
            "description",
        ]
        for agent in data
        for key in agent.keys()
    )


def test_agent(flask_client: FlaskLoginClient) -> None:
    """Tests the agent route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.post(
        "/agent", json={"image_name": "dummy/agent1:1.0"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("id") == "agent1"
    assert data.get("author") == "Test Author"
    assert data.get("type") == "agent"


def test_agent_not_found(flask_client: FlaskLoginClient) -> None:
    """Tests the agent route when the agent is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.post(
        "/agent", json={"image_name": "unknown/agent:1.0"}
    )
    assert response.status_code == 400


def test_simulators(flask_client: FlaskLoginClient) -> None:
    """Tests the simulators route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.get("/simulators")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert all(
        key
        in [
            "id",
            "tag",
            "author",
            "version",
            "type",
            "image_name",
            "port",
            "description",
        ]
        for simulator in data
        for key in simulator.keys()
    )


def test_simulator(flask_client: FlaskLoginClient) -> None:
    """Tests the simulator route.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.post(
        "/simulator", json={"image_name": "dummy/simulator1:1.0"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("id") == "simulator1"
    assert data.get("author") == "Test Author"
    assert data.get("type") == "simulator"


def test_simulator_not_found(flask_client: FlaskLoginClient) -> None:
    """Tests the simulator route when the simulator is not found.

    Args:
        flask_client: A Flask test client.
    """
    response = flask_client.post(
        "/simulator", json={"image_name": "unknown/simulator:1.0"}
    )
    assert response.status_code == 400
