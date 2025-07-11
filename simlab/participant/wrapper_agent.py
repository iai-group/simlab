"""Wrapper for conversational agent served with an API."""

from dialoguekit.core import AnnotatedUtterance, Intent, Utterance
from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.participant import Agent
from dialoguekit.participant.agent import AgentType
from simlab.utils.participant_api.utils_api_calls import get_utterance_response


class WrapperAgent(Agent):
    def __init__(
        self,
        id: str,
        uri: str = "http://localhost:7000",
        agent_type: AgentType = AgentType.BOT,
        stop_intent: Intent = Intent("EXIT"),
    ) -> None:
        """Initializes the conversational agent.

        Args:
            id: Agent ID.
            uri: URI of the agent's API.
            agent_type: Agent type. Defaults to BOT.
            stop_intent: Label of the exit intent. Defaults to "EXIT".
        """
        super().__init__(id=id, agent_type=agent_type, stop_intent=stop_intent)
        self._uri = uri

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        response = AnnotatedUtterance(
            text="Hello! How can I help you?",
            participant=self._type,
        )
        self._dialogue_connector.register_agent_utterance(response)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        response = AnnotatedUtterance(
            text="Goodbye!",
            participant=self._type,
            dialogue_acts=[DialogueAct(self.stop_intent)],
        )
        self._dialogue_connector.register_agent_utterance(response)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Responds to the other participant with an utterance.

        Args:
            utterance: The other participant's utterance.
        """
        context = [
            utterance.text
            for utterance in self._dialogue_connector.dialogue_history.utterances  # noqa
        ]
        request_data = {
            "context": context,
            "message": utterance.text,
            "user_id": self._dialogue_connector._user.id,
            "agent_id": self.id,
        }
        response = get_utterance_response(self._uri, request_data, self._type)
        self._dialogue_connector.register_agent_utterance(response)
