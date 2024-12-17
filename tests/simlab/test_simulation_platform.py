"""Tests for simulation platform."""

from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from dialoguekit.connector.dialogue_connector import DialogueConnector
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant
from dialoguekit.participant.user import User
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.simualtion_platform import SimulationPlatform


@pytest.fixture
def agent_config() -> Dict[str, str]:
    """Returns an agent configuration."""
    return {"id": "test_wrapper_agent", "uri": "http://localhost:6000"}


@pytest.fixture
def user_config() -> Dict[str, str]:
    """Returns a user configuration."""
    return {"id": "test_wrapper_user", "uri": "http://localhost:6001"}


@pytest.fixture
def sim_platform(
    agent_config: Dict[str, str],
    user_config: Dict[str, str],
) -> SimulationPlatform:
    """Returns a simulation platform instance for testing."""
    agent_class = WrapperAgent
    user_class = WrapperUserSimulator

    platform = SimulationPlatform(agent_class, user_class)
    assert platform._agent_class == agent_class
    assert platform._user_class == user_class

    platform.start(agent_config, user_config)
    assert platform._agent_config == agent_config
    assert platform._user_config == user_config

    return platform


def test_start(
    agent_config: Dict[str, str], user_config: Dict[str, str]
) -> None:
    """Tests start method."""
    agent_class = WrapperAgent
    user_class = WrapperUserSimulator

    platform = SimulationPlatform(Agent, User)

    platform.start(agent_config, user_config, agent_class, user_class)

    assert platform._agent_class == agent_class
    assert platform._user_class == user_class


def test_get_new_agent(
    sim_platform: SimulationPlatform,
) -> None:
    """Tests get_new_agent method."""
    agent = sim_platform.get_new_agent()
    assert isinstance(agent, WrapperAgent)


def test_get_new_user(
    sim_platform: SimulationPlatform,
    user_config: Dict[str, str],
) -> None:
    """Tests get_new_user method."""
    user = sim_platform.get_new_user(user_config)
    assert isinstance(user, WrapperUserSimulator)


def test_connect(sim_platform: SimulationPlatform, monkeypatch) -> None:
    """Tests connect method."""
    # Mock DialogueConnector
    MockDialogueConnector = MagicMock(spec=DialogueConnector)
    dialogue_connector = MagicMock()
    dialogue_connector.start.return_value = None
    MockDialogueConnector.return_value = dialogue_connector

    monkeypatch.setattr(
        "simlab.simualtion_platform.DialogueConnector",
        MockDialogueConnector,
    )

    user_id = "test_user"
    sim_platform.connect(user_id)

    assert "test_user" in sim_platform._active_users

    MockDialogueConnector.assert_called_once()
    dialogue_connector.start.assert_called_once()


def test_display_agent_utterance(
    sim_platform: SimulationPlatform, capsys
) -> None:
    """Tests display_agent_utterance method."""
    sim_platform.display_agent_utterance(
        Utterance("Hello!", DialogueParticipant.AGENT), "test_agent"
    )
    captured = capsys.readouterr()
    assert "test_agent: Hello!" == captured.out.strip()


def test_display_user_utterance(
    sim_platform: SimulationPlatform, capsys
) -> None:
    """Tests display_user_utterance method."""
    sim_platform.display_user_utterance(
        Utterance("Hello!", DialogueParticipant.USER), "test_user"
    )
    captured = capsys.readouterr()
    assert "test_user: Hello!" == captured.out.strip()


def test_get_new_agent_config_error(user_config: Dict[str, str]) -> None:
    """Tests get_new_agent method with error."""
    platform = SimulationPlatform(WrapperAgent, WrapperUserSimulator)

    agent_config = {"id": "test_wrapper_agent", "attr": "value"}
    platform.start(agent_config, user_config)

    with patch("logging.error") as mock_logging_error:
        agent = platform.get_new_agent()
        assert agent is None

        mock_logging_error.assert_called_once_with(
            "Error while creating agent: __init__() got an unexpected keyword "
            "argument 'attr'"
        )


def test_get_new_user_config_error(sim_platform: SimulationPlatform) -> None:
    """Tests get_new_user method with error."""
    user_config = {"id": "test_wrapper_user", "attr": "value"}

    with patch("logging.error") as mock_logging_error:
        user = sim_platform.get_new_user(user_config)
        assert user is None

        mock_logging_error.assert_called_once_with(
            "Error while creating user: __init__() got an unexpected keyword "
            "argument 'attr'"
        )
