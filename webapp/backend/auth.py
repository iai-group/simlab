"""Authentication module."""

import base64
from typing import Dict

import bcrypt
from app import mongo
from flask import Blueprint, Response, jsonify, request, session

auth = Blueprint("authentication", __name__)


def check_authorization(headers: Dict[str, str]) -> bool:
    """Checks if a user is authorized.

    Args:
        headers: Request headers.

    Returns:
        True if the Authorization header is present else False.
    """
    auth_header = headers.get("Authorization")
    return auth_header is not None


@auth.route("/login", methods=["POST"])
def login() -> Response:
    """Logs in a user."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found."}), 400

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return (
            jsonify(
                {"message": "Login failed. Please check your credentials."}
            ),
            401,
        )

    session["user"] = username
    session["logged_in"] = True
    return jsonify({"message": "Login successful"}), 200


@auth.route("/logout", methods=["POST"])
def logout() -> Response:
    """Logs out a user."""
    assert request.method == "POST", "Invalid request method"

    if not check_authorization(request.headers):
        return jsonify({"message": "Forbidden. You are not logged in."}), 403

    session.clear()
    return jsonify({"message": "Logout successful"}), 200


@auth.route("/register", methods=["POST"])
def register() -> Response:
    """Registers a new user."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Check if user already exists
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"message": "User already exists."}), 400

    # Register user in MongoDB
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "email": email,
        "username": username,
        "password": hashed_password,
    }
    mongo.db.users.insert_one(user)

    return jsonify({"message": "User registered successfully."}), 201


@auth.route("/reset-password", methods=["POST"])
def reset_password() -> Response:
    """Resets a user's password."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if user exists
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found."}), 400

    # Reset user's password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    mongo.db.users.update_one(
        {"email": email}, {"$set": {"password": hashed_password}}
    )

    return jsonify({"message": "Password reset successfully."}), 200


@auth.route("/auth/verify", methods=["GET", "POST"])
def verify_authentication() -> Response:
    """Verifies user authentication.

    It uses for authentication for private Docker registry. It assumes that
    the Authorization header contains the credentials in the form of
    "Basic base64(username:password)". It decodes the credentials and checks
    if the user exists in the database.
    """
    # Get the Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Basic "):
        return (
            jsonify({"message": "Missing or invalid Authorization header"}),
            401,
        )

    # Decode the Base64-encoded credentials
    auth_token = auth_header.split(" ")[1]
    try:
        decoded_credentials = base64.b64decode(auth_token).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)
    except Exception:
        return jsonify({"message": "Invalid credentials format"}), 401

    # Find the user in the database
    user = mongo.db.users.find_one({"username": username})
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user["password"]
    ):
        return jsonify({"message": "Authentication failed"}), 401

    # Successful authentication
    return jsonify({"message": "Authentication successful"}), 200
