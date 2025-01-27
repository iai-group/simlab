"""Flask API for SimLab backend."""

from bson import ObjectId
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from connectors.docker.docker_registry_connector import DockerRegistryConnector
from connectors.jenkins.jenkins_job_manager import JenkinsJobManager
from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.user import User

DATA_FOLDER = "data/simlab"

login_manager = LoginManager()
mongo_connector = MongoDBConnector()
docker_registry_connector = DockerRegistryConnector()
jenkins_job_manager = JenkinsJobManager()


@login_manager.user_loader
def load_user(user_id: str) -> User:
    """Loads a user.

    Args:
        user_id: User ID.

    Raises:
        ValueError: If the user id is not found in the database.

    Returns:
        User.
    """
    database = mongo_connector.get_database()
    user_data = database.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise ValueError(f"User not found: {user_id}")

    return User.from_mongo_document(user_data)


def create_app(testing: bool = False) -> Flask:
    """Creates a Flask app.

    Args:
        testing: Whether the app is for testing. Defaults to False.
    """
    app = Flask(__name__)
    app.secret_key = "hUoOv1vgi0pQVgxETY4/K2f7lXL90gtJunFXzwj/g0w="

    CORS(
        app,
        resources={
            r"*": {
                "origins": [
                    "http://127.0.0.1",
                    "http://localhost:3001",
                    "https://localhost",
                ]
            }
        },
        supports_credentials=True,
    )

    login_manager.init_app(app)

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = (
        "None"  # Allow cross-site cookies (needed for cross-origin requests)
    )
    app.config["REMEMBER_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SECURE"] = True
    app.config["REMEMBER_COOKIE_SAMESITE"] = (
        "None"  # Allow cross-site remember cookies
    )

    app.config["UPLOAD_FOLDER"] = "data/uploads"
    app.config["ALLOWED_EXTENSIONS"] = {"json"}

    if testing:
        mongo_connector.set_default_db("simlab_test")

    jenkins_job_manager.check_jenkins_connection()

    # Register blueprints
    from webapp.backend.routes.auth import auth as auth_blueprint
    from webapp.backend.routes.docs import docs as docs_blueprint
    from webapp.backend.routes.results import results as results_blueprint
    from webapp.backend.routes.run import run as run_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(docs_blueprint)
    app.register_blueprint(run_blueprint)
    app.register_blueprint(results_blueprint)

    return app
