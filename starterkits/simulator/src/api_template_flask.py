"""User simulator API template for Flask framework.

This file contains methods with placeholders for the API endpoints described in
the documentation. Placeholders are indicated by TODO comments."""

from flask import Flask, request, jsonify, Response
from typing import List, Dict, Union

app = Flask(__name__)


@app.route("/receive_utterance", methods=["POST"])
def receive_utterance() -> Response:
    """Receives an utterance from the agent and sends a response.

    Returns:
        Response to conversational agent.
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
    """Configures the simulator with custom parameters.

    Returns:
        Whether the configuration was successful.
    """
    try:
        simulator_id = request.json.get("id")
        parameters = request.json.get("parameters")

        # TODO: Validate simulator_id and parameters.
        b_valid_configuration = (
            False  # Placeholder for validation, defaults to False.
        )

        if not b_valid_configuration:
            return jsonify({"message": "Invalid configuration"}), 400

        # TODO: Implement configuration logic.

        b_success = False  # Placeholder for success status, defaults to False.

        if b_success:
            return jsonify({"message": "Configuration successful"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/set_information_need", methods=["POST"])
def set_information_need() -> Response:
    """Sets the information need for the user.

    This endpoint is used before starting a conversation.

    Return:
        Whether the operation was successful.
    """
    try:
        user_id = request.json.get("user_id")
        information_need = request.json.get(
            "information_need"
        )  # Check documentation for further details on information need format.

        # TODO: Implement logic to set the information need.
        b_success = False  # Placeholder for success status, defaults to False.

        if b_success:
            return (
                jsonify({"message": "Information need set successfully"}),
                201,
            )

        return (
            jsonify(
                {
                    "message": "An issue occurred when setting the information "
                    "need."
                }
            ),
            400,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/get_information_need", methods=["POST"])
def get_information_need() -> Response:
    """Returns the current information need of the simulator."""
    try:
        user_id = request.json.get("user_id")

        # TODO: Implement the logic to retrieve the simulator's information need.
        information_need: Dict[
            str, Union[Dict, List]
        ] = None  # Placeholder for information need, defaults to None.
    except Exception as e:
        return jsonify({"message": str(e)}), 500
