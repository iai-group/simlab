"""Fixtures for SimLab tests."""

from typing import List

import pytest

from dialoguekit.core.dialogue import Dialogue
from dialoguekit.utils.dialogue_reader import json_to_dialogues
from simlab.core.simulation_domain import SimulationDomain


@pytest.fixture(scope="session")
def simulation_domain() -> SimulationDomain:
    """Returns the simulation domain for testing."""
    domain = SimulationDomain("tests/simlab/data/domain.yaml")
    assert domain.get_name() == "movies_testing"
    return domain


@pytest.fixture(scope="session")
def dialogues() -> List[Dialogue]:
    """Returns a list of dialogues for testing."""
    dialogues = json_to_dialogues("tests/simlab/data/dialogues.json")
    assert len(dialogues) == 2
    return dialogues
