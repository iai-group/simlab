"""Tests for task module."""

from typing import List
from unittest.mock import Mock

import pytest

from dialoguekit.core.dialogue import Dialogue
from simlab.core.simulation_domain import SimulationDomain
from simlab.metrics.metric import Metric
from simlab.tasks import Task


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
    )

    assert t.name == "task_testing"
    assert t.domain.get_name() == "movies_testing"
    assert len(t.metrics) == 1

    return t


def test_get_information_needs_retrieve_batch(task: Task) -> None:
    """Tests get_information_needs method with a retrieved batch."""
    batch_id = "675380fa0f51790295720dac"
    information_needs = task.get_information_needs(batch_id=batch_id)
    assert len(information_needs) == 4


def test_retrieve_information_needs(task: Task) -> None:
    """Tests _retrieve_information_needs method."""
    batch_id = "675380fa0f51790295720dac"
    information_needs = task._retrieve_information_needs(batch_id)
    assert len(information_needs) == 4


def test_evaluation(task: Task, dialogues: List[Dialogue]) -> None:
    """Tests evaluate method."""
    results = task.evaluation(dialogues)

    assert len(results) == 1
    assert len(results["mocked_metric"]) == 2
    assert all([result == 1 for result in results["mocked_metric"]])
