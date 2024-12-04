"""Tests for routes related to authentication."""

from typing import Dict

import bcrypt
from flask.testing import FlaskClient
from pymongo.database import Database


def test_register(
    test_client: FlaskClient,
    test_database: Database,
    user_data: Dict[str, str],
) -> None:
    """Tests registering a new user.

    Args:
        test_client: Flask test client.
        test_database: Test database.
        user_data: User data.
    """
    response = test_client.post("/register", json=user_data)
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully."}

    # Check if user was added to the database
    user = test_database.users.find_one({"email": user_data["email"]})
    assert user is not None
    assert user.get("username") == user_data["username"]


def test_register_existing_user(
    test_client: FlaskClient, user_data: Dict[str, str]
) -> None:
    """Tests registering an existing user.

    Args:
        test_client: Flask test client.
        user_data: User data already in the database.
    """
    response = test_client.post(
        "/register",
        json=user_data,
    )
    assert response.status_code == 400
    assert response.json == {"message": "User already exists."}


def test_register_invalid_form(test_client: FlaskClient) -> None:
    """Tests registering a user with an invalid form.

    Args:
        test_client: Flask test client.
    """
    response = test_client.post(
        "/register",
        json={"username": "test_user", "password": "test_password"},
    )
    assert response.status_code == 400
    assert response.json == {"message": "Invalid form."}


def test_login_no_user(test_client: FlaskClient) -> None:
    """Tests logging in with a non-existing user.

    Args:
        test_client: Flask test client.
    """
    response = test_client.post(
        "/login",
        json={"username": "non_existing_user", "password": "test_password"},
    )
    assert response.status_code == 400
    assert response.json == {"message": "User not found."}


def test_login_wrong_password(
    test_client: FlaskClient, user_data: Dict[str, str]
) -> None:
    """Tests logging in with the wrong password.

    Args:
        test_client: Flask test client.
        user_data: User data.
    """
    response = test_client.post(
        "/login",
        json={"username": user_data["username"], "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json == {
        "message": "Login failed. Please check your credentials."
    }


def test_login_success(
    test_client: FlaskClient, user_data: Dict[str, str]
) -> None:
    """Tests logging in successfully.

    Args:
        test_client: Flask test client.
        user_data: User data.
    """
    response = test_client.post(
        "/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Login successful"}


def test_logout(test_client: FlaskClient) -> None:
    """Tests logging out a user.

    Args:
        test_client: Flask test client.
    """
    response = test_client.post("/logout")
    assert response.status_code == 200
    assert response.json == {"message": "Logout successful"}


def test_logout_not_logged_in(test_client: FlaskClient) -> None:
    """Tests logging out a user who is not logged in.

    Args:
        test_client: Flask test client.
    """
    response = test_client.post("/logout")
    assert response.status_code == 401
    assert response.json == {"message": "User not logged in."}


def test_reset_password(
    test_client: FlaskClient,
    test_database: Database,
    user_data: Dict[str, str],
) -> None:
    """Tests resetting a user's password.

    Args:
        test_client: Flask test client.
        user_data: User data.
    """
    response = test_client.post(
        "/reset-password",
        json={
            "username": user_data["username"],
            "password": "new_password",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Password reset successfully."}

    # Check if password was updated in the database
    user = test_database.users.find_one({"username": user_data["username"]})
    assert user is not None
    assert bcrypt.checkpw("new_password".encode("utf-8"), user.get("password"))

    # Reset password back to original
    test_database.users.update_one(
        {"username": user_data["username"]},
        {
            "$set": {
                "password": bcrypt.hashpw(
                    user_data["password"].encode("utf-8"), bcrypt.gensalt()
                )
            }
        },
    )


def test_reset_password_invalid_form(test_client: FlaskClient) -> None:
    """Tests resetting a user's password with an invalid form.

    Args:
        test_client: Flask test client.
    """
    response = test_client.post(
        "/reset-password",
        json={"username": "test_user"},
    )
    assert response.status_code == 400
    assert response.json == {"message": "Invalid form."}
