"""Simulation platform facilitating interaction between agent and simulator."""

from typing import Dict, Tuple, Type

from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.user import User
from dialoguekit.platforms import Platform
from simlab.core.dialogue_connector import SimulationDialogueConnector


class SimulationPlatform(Platform):
    def __init__(self, agent_class: Type[Agent]) -> None:
        """Initializes the simulation platform.

        Args:
            agent_class: Class of the agent.
        """
        super().__init__(agent_class)
        self._active_agent_user_pairs: Dict[
            Tuple[str, str], Tuple[Agent, User]
        ] = {}

    def start(self) -> None:
        """Starts the simulation platform.

        This method is not required for the simulation platform.
        """
        pass

    def connect(
        self, user_id: str, user_simulator: User, agent: Agent, output_dir: str
    ) -> None:
        """Connects a user simulator and an agent.

        Args:
            user_id: User simulator ID.
            user_simulator: User simulator.
            agent: Agent.
            output_dir: Output directory to save the dialogues.

        Raises:
            ValueError: If the agent is already connected to the user.
        """
        if (agent.id, user_id) in self._active_agent_user_pairs:
            raise ValueError(
                f"Agent {agent.id} is already connected to user {user_id}"
            )

        self._active_agent_user_pairs[(agent.id, user_id)] = (
            agent,
            user_simulator,
        )
        dialogue_connector = SimulationDialogueConnector(
            agent=agent,
            user=user_simulator,
            platform=self,
            output_dir=output_dir,
        )
        dialogue_connector.start()

    def display_agent_utterance(
        self, utterance: Utterance, agent_id: str, user_id: str = None
    ) -> None:
        """Displays an agent utterance.

        This is method is not required for the simulation platform.
        """
        pass

    def display_user_utterance(
        self, utterance: Utterance, user_id: str
    ) -> None:
        """Displays a user utterance.

        This is method is not required for the simulation platform.
        """
        pass

    def disconnect(self, user_id: str, agent_id: str) -> None:
        """Disconnects a user simulator from an agent.

        Args:
            user_id: User simulator ID.
            agent_id: Agent ID.
        """
        self._active_agent_user_pairs.pop((agent_id, user_id))
