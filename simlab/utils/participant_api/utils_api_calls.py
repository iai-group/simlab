"""Utility functions for making API calls to the participant service."""

import time
from typing import Any, Dict

import requests

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import DialogueParticipant
from simlab.utils.participant_api.utils_response_parsing import (
    parse_API_response,
)


def configure_participant(
    uri: str, id: str, parameters: Dict[str, Any]
) -> None:
    """Configures the participant with parameters.

    Args:
        uri: URI of the participant's API.
        id: Participant's ID.
        parameters: Configuration parameters.

    Raises:
        RuntimeError: If the agent fails to configure.
    """
    r = requests.post(
        f"{uri}/configure", json={"id": id, "parameters": parameters}
    )
    if r.status_code != 201:
        raise RuntimeError("Failed to configure the agent.")


def get_utterance_response(
    uri: str, request_data: Dict[str, Any], participant: DialogueParticipant
) -> AnnotatedUtterance:
    """Gets participant's response to an utterance.

    Args:
        uri: URI of the participant's API.
        request_data: Data to send to the API.
        participant: Dialogue participant.

    Returns:
        Annotated utterance.
    """
    r = requests.post(
        f"{uri}/receive_utterance",
        json=request_data,
    )
    data = r.json()
    (
        utterance_text,
        utterance_dialogue_acts,
        utterance_annotations,
        metadata,
    ) = parse_API_response(data)

    response = AnnotatedUtterance(
        text=utterance_text,
        participant=participant,
        dialogue_acts=utterance_dialogue_acts,
        annotations=utterance_annotations,
        metadata=metadata,
    )
    return response


def wait_for_participant(
    uri: str, max_retries: int = 10, delay: int = 5
) -> bool:
    """Waits for the participant to be ready.

    Args:
        uri: URI of the participant's API.
        max_retries: Maximum number of retries.
        delay: Delay between retries.

    Raises:
        RuntimeError: If the participant is not ready.
    """
    for _ in range(max_retries):
        try:
            requests.get(f"{uri}/")
            return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(delay)
    raise RuntimeError("Participant is not ready.")
