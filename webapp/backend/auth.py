"""Authentication module."""

import bcrypt
from app import mongo_connector
from flask import Blueprint, Response, jsonify, request
from flask_login import login_required, login_user, logout_user
from user import User

auth = Blueprint("authentication", __name__)


@auth.route("/login", methods=["POST"])
def login() -> Response:
    """Logs in a user."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    database = mongo_connector.get_database()

    user = database.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found."}), 400

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return (
            jsonify(
                {"message": "Login failed. Please check your credentials."}
            ),
            401,
        )

    user = User.from_mongo_document(user)
    login_user(user, remember=True)

    return jsonify({"message": "Login successful"}), 200


@auth.route("/logout", methods=["POST", "GET"])
@login_required
def logout() -> Response:
    """Logs out a user."""
    assert request.method in ["POST", "GET"], "Invalid request method"

    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth.route("/register", methods=["POST"])
def register() -> Response:
    """Registers a new user."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    database = mongo_connector.get_database()

    # Check if user already exists
    if database.users.find_one({"email": email}):
        return jsonify({"message": "User already exists."}), 400

    # Register user in MongoDB
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "email": email,
        "username": username,
        "password": hashed_password,
    }
    database.users.insert_one(user)

    return jsonify({"message": "User registered successfully."}), 201


@auth.route("/reset-password", methods=["POST"])
def reset_password() -> Response:
    """Resets a user's password."""
    assert request.method == "POST", "Invalid request method"

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Check if user exists
    database = mongo_connector.get_database()
    user = database.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found."}), 400

    # Reset user's password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    database.users.update_one(
        {"username": username}, {"$set": {"password": hashed_password}}
    )

    return jsonify({"message": "Password reset successfully."}), 200
