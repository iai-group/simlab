"""Fixtures for SimLab tests."""

from typing import List
from unittest.mock import Mock

import pytest

from dialoguekit.core.dialogue import Dialogue
from dialoguekit.utils.dialogue_reader import json_to_dialogues
from simlab.core.information_need import InformationNeed
from simlab.core.simulation_domain import SimulationDomain
from simlab.metrics.metric import Metric
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.simulation_platform import SimulationPlatform
from simlab.tasks.task import Task


@pytest.fixture(scope="session")
def simulation_domain() -> SimulationDomain:
    """Returns the simulation domain for testing."""
    domain = SimulationDomain("tests/simlab/data/domain.yaml")
    assert domain.get_name() == "movies_testing"
    assert len(domain.get_item_collections()) == 1
    return domain


@pytest.fixture(scope="session")
def dialogues() -> List[Dialogue]:
    """Returns a list of dialogues for testing."""
    dialogues = json_to_dialogues("tests/simlab/data/dialogues.json")
    assert len(dialogues) == 2
    return dialogues


@pytest.fixture
def information_need() -> InformationNeed:
    """Fixture for information need."""
    return InformationNeed(
        constraints={"title": "title", "year": 2024},
        requests=["rating"],
    )


@pytest.fixture
def metric(dialogues: List[Dialogue]) -> Mock:
    """Returns a mocked metric."""
    mocked_metric = Mock(spec=Metric)
    mocked_metric.name = "mocked_metric"
    mocked_metric.evaluate_dialogue.return_value = 1
    mocked_metric.evaluate_dialogues.return_value = [1 for _ in dialogues]
    return mocked_metric


@pytest.fixture
def task(simulation_domain: SimulationDomain, metric) -> Task:
    """Returns a task instance for testing.

    Args:
        simulation_domain: Simulation domain.
        metric: Mocked metric.
    """
    t = Task(
        name="task_testing",
        domain=simulation_domain,
        metrics=[metric],
        db_name="simlab_test",
        batch_id="675380fa0f51790295720dac",
        training_batch_id="675380fa0f51790295720edc",
    )

    assert t.name == "task_testing"
    assert t.domain.get_name() == "movies_testing"
    assert len(t.metrics) == 1

    return t


@pytest.fixture
def sim_platform() -> SimulationPlatform:
    """Returns a simulation platform instance for testing."""
    agent_class = WrapperAgent

    platform = SimulationPlatform(agent_class)
    assert platform._agent_class == agent_class

    return platform
