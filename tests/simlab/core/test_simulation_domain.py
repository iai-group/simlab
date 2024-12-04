"""Tests for simulation domain."""

from simlab.core.simulation_domain import SimulationDomain


def test_get_requestable_slots(simulation_domain: SimulationDomain) -> None:
    """Tests get_requestable_slots.

    Args:
        simulation_domain: Simulation domain.
    """
    assert all(
        slot in simulation_domain.get_requestable_slots()
        for slot in ["year", "title", "genre", "rating"]
    )


def test_get_informable_slots(simulation_domain: SimulationDomain) -> None:
    """Tests get_informable_slots.

    Args:
        simulation_domain: Simulation domain.
    """
    assert all(
        slot in simulation_domain.get_informable_slots()
        for slot in ["year", "genre"]
    )
