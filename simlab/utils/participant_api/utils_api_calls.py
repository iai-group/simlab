"""Utility functions for making API calls to the participant service."""

from typing import Any, Dict

import requests

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import DialogueParticipant
from simlab.utils.participant_api.utils_response_parsing import (
    parse_API_response,
)


def configure_participant(uri: str, parameters: Dict[str, Any]) -> None:
    """Configures the participant with parameters.

    Args:
        uri: URI of the participant's API.
        parameters: Configuration parameters.

    Raises:
        RuntimeError: If the agent fails to configure.
    """
    r = requests.post(f"{uri}/configure", json={"parameters": parameters})
    if r.status_code != 200:
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
