"""Tests for simulation platform."""

from unittest.mock import MagicMock

from simlab.core.dialogue_connector import SimulationDialogueConnector
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.simulation_platform import SimulationPlatform


def test_connect(sim_platform: SimulationPlatform, monkeypatch) -> None:
    """Tests connect method."""
    # Mock DialogueConnector
    MockDialogueConnector = MagicMock(spec=SimulationDialogueConnector)
    dialogue_connector = MagicMock()
    dialogue_connector.start.return_value = None
    MockDialogueConnector.return_value = dialogue_connector

    monkeypatch.setattr(
        "simlab.simulation_platform.SimulationDialogueConnector",
        MockDialogueConnector,
    )

    agent = MagicMock(spec=WrapperAgent)
    agent.id = "test_agent"
    user_simulator = MagicMock(spec=WrapperUserSimulator)
    user_simulator.id = "test_user_simulator"

    user_id = "test_user_simulator"
    sim_platform.connect(user_id, user_simulator, agent, "tests/simlab/data")

    assert (
        "test_agent",
        "test_user_simulator",
    ) in sim_platform._active_agent_user_pairs.keys()

    MockDialogueConnector.assert_called_once()
    dialogue_connector.start.assert_called_once()


def test_disconnect(sim_platform: SimulationPlatform) -> None:
    """Tests disconnect method."""
    agent = MagicMock(spec=WrapperAgent)
    agent.id = "test_agent"
    user_simulator = MagicMock(spec=WrapperUserSimulator)
    user_simulator.id = "test_user_simulator"

    user_id = "test_user_simulator"
    sim_platform.connect(user_id, user_simulator, agent, "tests/simlab/data")

    sim_platform.disconnect("test_user_simulator", "test_agent")

    assert (
        "test_agent",
        "test_user_simulator",
    ) not in sim_platform._active_agent_user_pairs.keys()
