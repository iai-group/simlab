"""Flask API for SimLab backend."""

import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")
mongo = PyMongo()
session = Session()


def create_app() -> Flask:
    """Creates a Flask app."""
    app = Flask(__name__)
    app.secret_key = "hUoOv1vgi0pQVgxETY4/K2f7lXL90gtJunFXzwj/g0w="

    CORS(
        app,
        resources={r"*": {"origins": "https://127.0.0.1"}},
        supports_credentials=True,
    )

    app.config["MONGO_URI"] = f"{MONGO_URI}/simlab"
    mongo.init_app(app)

    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB"] = MongoClient(MONGO_URI)
    app.config["SESSION_MONGODB_DB"] = "flask_session"
    app.config["SESSION_COOKIE_NAME"] = "flask_session"
    app.config["SESSION_COOKIE_SECURE"] = (
        False  # TODO: Change to True in production
    )
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_PERMANENT"] = False
    session.init_app(app)

    # Register blueprints
    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app
