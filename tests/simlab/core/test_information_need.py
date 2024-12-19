"""Tests for information need."""

import pytest

from simlab.core.information_need import InformationNeed
from simlab.core.simulation_domain import SimulationDomain
from simlab.utils.utils_information_needs import (
    generate_random_information_needs,
    save_information_need_batch,
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


def test_to_dict(information_need: InformationNeed) -> None:
    """Tests to_dict.

    Args:
        information_need: Information need.
    """
    d = information_need.to_dict()
    assert d.get("constraints") == {"title": "title", "year": 2024}
    assert d.get("requested_slots") == ["rating"]
    assert d.get("fulfilled_slots") == {}


def test_from_dict(information_need: InformationNeed) -> None:
    """Tests from_dict.

    Args:
        information_need: Information need.
    """
    data = {
        "constraints": {"title": "title", "year": 2024},
        "requested_slots": {"rating": None},
    }
    loaded_information_need = InformationNeed.from_dict(data)

    assert loaded_information_need.constraints == information_need.constraints
    assert (
        loaded_information_need.requested_slots
        == information_need.requested_slots
    )


def test_from_dict_error() -> None:
    """Tests from_dict with an error."""
    with pytest.raises(KeyError):
        InformationNeed.from_dict(
            {
                "constraints": {"title": "title", "year": 2024},
            }
        )


def test_generate_random_information_needs(
    simulation_domain: SimulationDomain,
) -> None:
    """Tests generate_random_information_needs."""
    information_needs = generate_random_information_needs(simulation_domain, 10)
    assert len(information_needs) == 10


def test_save_information_need_batch(
    simulation_domain: SimulationDomain,
) -> None:
    """Tests save_information_need_batch."""
    information_needs = generate_random_information_needs(simulation_domain, 10)
    batch_id = save_information_need_batch(information_needs, "simlab_test")

    assert batch_id is not None
