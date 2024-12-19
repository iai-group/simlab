"""Tests for task module."""

from typing import List

from dialoguekit.core.dialogue import Dialogue
from simlab.tasks import Task


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
