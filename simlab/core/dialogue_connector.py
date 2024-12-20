"""Adapted dialogue connector from DialogueKit."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from dialoguekit.connector.dialogue_connector import DialogueConnector
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.user import User

if TYPE_CHECKING:
    from simlab.simulation_platform import SimulationPlatform


class SimulationDialogueConnector(DialogueConnector):
    def __init__(
        self,
        agent: Agent,
        user: User,
        platform: SimulationPlatform,
        output_dir: str,
        conversation_id: str = None,
    ) -> None:
        """Represents a dialogue connector.

        Args:
            agent: An instance of Agent.
            user: An instance of User.
            platform: An instance of SimulationPlatform.
            output_dir: Output directory to save the dialogue.
            conversation_id: Conversation ID. Defaults to None.
        """
        super().__init__(
            agent, user, platform, conversation_id, save_dialogue_history=True
        )
        self._output_dir = output_dir

    def _dump_dialogue_history(self) -> None:
        """Exports the dialogue history.

        The exported files will be named as 'AgentID_UserID.json'

        If the two participants have had a conversation previously, the new
        conversation will be appended to the same export document.

        Per dialogue, the dialogue metadata will be added. Also per utterance
        the utterance metadata, will be added to the same level as the utterance
        text. Intent will also be exported if provided.
        """
        # If conversation is empty we do not save it.
        if len(self._dialogue_history.utterances) == 0:
            return

        history = self._dialogue_history
        file_name = os.path.join(
            self._output_dir, f"{self._agent.id}_{self._user.id}.json"
        )
        json_file = []

        # Check directory and read if exists.
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
        if os.path.exists(file_name):
            with open(file_name, encoding="utf-8") as json_file_out:
                json_file = json.load(json_file_out)

        dialogue_as_dict = history.to_dict()
        dialogue_as_dict["agent"] = self._agent.to_dict()
        dialogue_as_dict["user"] = self._user.to_dict()

        json_file.append(dialogue_as_dict)

        with open(file_name, "w", encoding="utf-8") as outfile:
            json.dump(json_file, outfile)

        # Empty dialogue history to avoid duplicate save
        for _ in range(len(self._dialogue_history.utterances)):
            self._dialogue_history.utterances.pop()
