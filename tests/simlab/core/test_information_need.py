"""Tests for information need."""

import pytest

from simlab.core.information_need import InformationNeed


@pytest.fixture
def information_need() -> InformationNeed:
    """Fixture for information need."""
    return InformationNeed(
        constraints={"title": "title", "year": 2024},
        requests=["rating"],
    )


def test_get_constraint_value(information_need: InformationNeed) -> None:
    """Tests get_constraint_value.

    Args:
        information_need: Information need.
    """
    assert information_need.get_constraint_value("title") == "title"
    assert information_need.get_constraint_value("year") == 2024

    assert information_need.get_constraint_value("unknown") is None


def test_get_requestable_slots(information_need: InformationNeed) -> None:
    """Tests get_requestable_slots.

    Args:
        information_need: Information need.
    """
    assert information_need.get_requestable_slots() == ["rating"]
