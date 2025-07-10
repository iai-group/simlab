"""Conversational agent API template for Flask framework.

This file contains methods with placeholders for the API endpoints described in
the documentation. Placeholders are indicated by TODO comments."""

from flask import Flask, request, jsonify, Response
from typing import List, Dict

app = Flask(__name__)


@app.route("/receive_utterance", methods=["POST"])
def receive_utterance() -> Response:
    """Receives an utterance from the user and sends a response.

    Returns:
        Response to user.
    """
    try:
        context = request.json.get("context")
        user_id = request.json.get("user_id")
        agent_id = request.json.get("agent_id")
        utterance = request.json.get("message")

        # TODO: implement logic to process an utterance and generate a response.
        # Check documentation for further details on the expected format of
        # the different elements of the response.
        response: str = None  # Placeholder for response, defaults to None
        dialogue_acts: List = (
            None  # Placeholder for dialogue acts, defaults to None. Optional.
        )
        annotations: List = (
            None  # Placeholder for annotations, defaults to None. Optional.
        )
        metadata: Dict = (
            None  # Placeholder for metadata, defaults to None. Optional.
        )

        return (
            jsonify(
                {
                    "message": response,
                    "dialogue_acts": dialogue_acts,
                    "annotations": annotations,
                    "metadata": metadata,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/configure", methods=["POST"])
def configure() -> Response:
    """Configures the agent with custom parameters.

    Returns:
        Whether the configuration was successful.
    """
    try:
        agent_id = request.json.get("id")
        parameters = request.json.get("parameters")

        # TODO: Validate agent_id and parameters
        b_valid_configuration = (
            False  # Placeholder for validation, defaults to False
        )

        if not b_valid_configuration:
            return jsonify({"message": "Invalid configuration"}), 400

        # TODO: Implement configuration logic

        b_success = False  # Placeholder for success status, defaults to False

        if b_success:
            return jsonify({"message": "Configuration successful"}), 201

        return (
            jsonify(
                {"message": "An issue occurred when configuring the agent"}
            ),
            400,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500
