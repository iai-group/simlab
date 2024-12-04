"""Fixtures for SimLab tests."""

import pytest

from simlab.core.simulation_domain import SimulationDomain


@pytest.fixture(scope="session")
def simulation_domain() -> SimulationDomain:
    """Returns the simulation domain for testing."""
    domain = SimulationDomain("tests/simlab/data/domain.yaml")
    assert domain.get_name() == "movies_testing"
    return domain
