"""Simulation platform facilitating interaction between agent and simulator."""

import logging
from copy import deepcopy
from typing import Any, Dict, Type

from dialoguekit.connector import DialogueConnector
from dialoguekit.participant import Agent, User
from dialoguekit.platforms import Platform


class SimulationPlatform(Platform):
    def __init__(
        self, agent_class: Type[Agent], user_class: Type[User]
    ) -> None:
        """Initializes the simulation platform.

        Args:
            agent_class: Class of the agent.
            user_class: Class of the user.
        """
        super().__init__(agent_class)
        self._user_class = user_class

    def start(
        self,
        agent_config: Dict[str, Any],
        user_config: Dict[str, Any],
        agent_class: Type[Agent] = None,
        user_class: Type[User] = None,
    ) -> None:
        """Starts the simulation platform.

        Sets the configuration for the agent and the user. Optionally, changes
        the classes of the agent and the user.

        Args:
            agent_config: Configuration for the agent.
            user_config: Configuration for the user.
            agent_class: Class of the agent. Defaults to None.
            user_class: Class of the user. Defaults to None
        """
        self._agent_config = agent_config
        self._user_config = user_config

        if agent_class:
            self._agent_class = agent_class
        if user_class:
            self._user_class = user_class

    def get_new_agent(self) -> Agent:
        """Returns a new instance of the agent.

        Returns:
            Agent.
        """
        try:
            return self._agent_class(**self._agent_config)
        except AttributeError as e:
            logging.error(f"Error while creating agent: {e}")

    def get_new_user(self, config: Dict[str, Any]) -> User:
        """Returns a new instance of the user.

        Args:
            config: Configuration for the user.

        Returns:
            User.
        """
        try:
            return self._user_class(**config)
        except AttributeError as e:
            logging.error(f"Error while creating user: {e}")

    def connect(self, user_id: str) -> None:
        """Connects a user to an agent.

        Args:
            user_id: User ID.
        """
        user_config = deepcopy(self._user_config)
        user_config["id"] = user_id
        self._active_users[user_id] = self.get_new_user(user_config)
        dialogue_connector = DialogueConnector(
            agent=self.get_new_agent(),
            user=self._active_users[user_id],
            platform=self,
        )
        dialogue_connector.start()

    def display_agent_utterance(self, user_id: str, utterance: str) -> None:
        """Displays an agent utterance.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.
        """
        print(f"Agent: {utterance}")

    def display_user_utterance(self, user_id: str, utterance: str) -> None:
        """Displays a user utterance.

        Args:
            user_id: User ID.
            utterance: An instance of Utterance.
        """
        print(f"User: {utterance}")
