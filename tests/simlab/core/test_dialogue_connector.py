"""Tests for dialogue connector."""

import os
from unittest.mock import MagicMock

import pytest

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.participant.participant import DialogueParticipant
from simlab.core.dialogue_connector import SimulationDialogueConnector
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator


@pytest.fixture
def dialogue_connector() -> SimulationDialogueConnector:
    """Returns a dialogue connector."""
    agent = MagicMock(spec=WrapperAgent)
    agent.id = "test_agent"
    agent.to_dict.return_value = {"id": agent.id}
    user_simulator = MagicMock(spec=WrapperUserSimulator)
    user_simulator.id = "test_user_simulator"
    user_simulator.to_dict.return_value = {"id": user_simulator.id}

    platform = MagicMock()

    dialogue_connector = SimulationDialogueConnector(
        agent=agent,
        user=user_simulator,
        platform=platform,
        output_dir="tests/simlab/data/dialogue_export",
    )

    assert (
        dialogue_connector._output_dir == "tests/simlab/data/dialogue_export"
    )
    return dialogue_connector


def test_dump_dialogue_history_empty(
    dialogue_connector: SimulationDialogueConnector,
) -> None:
    """Tests dialogue saving with empty conversation."""
    assert dialogue_connector._dump_dialogue_history() is None


def test_dump_dialogue_history(
    dialogue_connector: SimulationDialogueConnector,
) -> None:
    """Tests dialogue saving."""
    dialogue_connector.register_agent_utterance(
        AnnotatedUtterance("Hello", DialogueParticipant.AGENT)
    )
    dialogue_connector.register_user_utterance(
        AnnotatedUtterance("Hi", DialogueParticipant.USER)
    )

    assert not os.path.exists("tests/simlab/data/dialogue_export/")
    dialogue_connector._dump_dialogue_history()
    assert os.path.exists(
        "tests/simlab/data/dialogue_export/test_agent_test_user_simulator.json"
    )

    # Clean up
    os.remove(
        "tests/simlab/data/dialogue_export/test_agent_test_user_simulator.json"
    )
    os.rmdir("tests/simlab/data/dialogue_export/")
