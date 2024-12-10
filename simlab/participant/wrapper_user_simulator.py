"""Wrapper for user simulator served with an API."""

import requests

from dialoguekit.core import AnnotatedUtterance, Utterance
from dialoguekit.participant import User
from dialoguekit.participant.user import UserType
from simlab.utils.utils_response_parsing import parse_API_response


class WrapperUserSimulator(User):
    def __init__(
        self, id: str, uri: str, user_type: UserType = UserType.SIMULATOR
    ) -> None:
        """Initializes the user simulator.

        Args:
            id: User ID.
            uri: URI of the user simulator's API.
            user_type: User type. Defaults to SIMULATOR.
        """
        super().__init__(id, user_type)
        self._uri = uri

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        # TODO: Extract common code with WrapperAgent.receive_utterance to a
        # utility function.
        context = [
            utterance.text
            for utterance in self._dialogue_connector.dialogue_history.utterances  # noqa
        ]
        r = requests.post(
            f"{self._uri}/receive_utterance",
            json={
                "context": context,
                "message": utterance.text,
                "agent_id": self._dialogue_connector._agent.id,
            },
        )
        r = r.json()
        (
            utterance_text,
            utterance_dialogue_acts,
            utterance_annotations,
            metadata,
        ) = parse_API_response(r)

        response = AnnotatedUtterance(
            text=utterance_text,
            participant=self._type,
            dialogue_acts=utterance_dialogue_acts,
            annotations=utterance_annotations,
            metadata=metadata,
        )
        self._dialogue_connector.register_user_utterance(response)
