"""Fixtures to test backend."""

from typing import Dict

import pytest
from flask_login import FlaskLoginClient

from webapp.backend.app import create_app, mongo_connector


@pytest.fixture(scope="session")
def flask_app():
    """Creates a Flask app for testing."""
    app = create_app(testing=True)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    app.test_client_class = FlaskLoginClient

    yield app


@pytest.fixture(scope="session")
def flask_client(flask_app):
    """Creates a Flask test client.

    Args:
        flask_app: Flask app.
    """
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def flask_logged_client(flask_client: FlaskLoginClient):
    """Creates a Flask test client with a logged user.

    Args:
        flask_client: Flask test client.
    """
    response = flask_client.post(
        "/login", json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200

    yield flask_client

    flask_client.post("/logout")


@pytest.fixture(scope="session")
def test_database():
    """Returns the test database."""
    test_db = mongo_connector.get_database("simlab_test")
    yield test_db
    mongo_connector.client.drop_database("simlab_test")


@pytest.fixture(scope="session")
def user_data() -> Dict[str, str]:
    """Returns user data."""
    return {
        "email": "test_user@example.com",
        "username": "test_user",
        "password": "test_password",
    }
