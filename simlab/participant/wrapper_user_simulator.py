"""Wrapper for user simulator served with an API."""

import requests

from dialoguekit.core import Utterance
from dialoguekit.participant import User
from dialoguekit.participant.user import UserType
from simlab.core.information_need import InformationNeed
from simlab.utils.participant_api.utils_api_calls import get_utterance_response


class WrapperUserSimulator(User):
    def __init__(
        self,
        id: str,
        uri: str = "http://localhost:7001",
        user_type: UserType = UserType.SIMULATOR,
    ) -> None:
        """Initializes the user simulator.

        Args:
            id: User ID.
            uri: URI of the user simulator's API.
            user_type: User type. Defaults to SIMULATOR.
        """
        super().__init__(id, user_type)
        self._uri = uri

    def set_information_need(self, information_need: InformationNeed) -> None:
        """Sets the information need for the user simulator.

        Args:
            information_need: Information need.

        Raises:
            RuntimeError: If the request fails.
        """
        r = requests.post(
            f"{self._uri}/set_information_need",
            json={
                "information_need": information_need.to_dict(),
                "user_id": self.id,
            },
        )
        status_code = r.status_code
        if status_code != 200:
            raise RuntimeError(
                f"Failed to set information need. Status code: {status_code}\n"
                f"Response: {r.text}"
            )

        # Add information need as dialogue metadata.
        self._dialogue_connector.dialogue_history.metadata.update(
            {"information_need": information_need.to_dict()}
        )

    def update_information_need(self) -> None:
        """Updates information need metadata in the dialogue.

        Raises:
            RuntimeError: If the request fails.
        """
        r = requests.get(
            f"{self._uri}/get_information_need",
            params={"user_id": self.id},
        )
        status_code = r.status_code
        if status_code != 200:
            raise RuntimeError(
                f"Failed to get information need. Status code: {status_code}\n"
                f"Response: {r.text}"
            )
        data = r.json()
        if data.get("information_need"):
            self._dialogue_connector.dialogue_history.metadata.update(
                {"information_need": data.get("information_need")}
            )

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        context = [
            utterance.text
            for utterance in self._dialogue_connector.dialogue_history.utterances  # noqa
        ]
        request_data = {
            "context": context,
            "message": utterance.text,
            "agent_id": self._dialogue_connector._agent.id,
        }
        response = get_utterance_response(self._uri, request_data, self._type)
        self._dialogue_connector.register_user_utterance(response)
