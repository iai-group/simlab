"""Tests for base configuration reader."""

import os

import pytest

from simlab.core.simulation_domain import SimulationDomain
from simlab.metrics.task_performance.success_rate import SuccessRate
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.tasks.task import Task
from simlab.utils.configuration_readers.base_configuration_reader import (
    BaseConfigurationReader,
)
from simlab.utils.configuration_readers.component_generators.base_component_generator import (  # noqa: E501
    BaseComponentGenerator,
)


@pytest.fixture
def base_configuration_reader() -> BaseConfigurationReader:
    """Returns a base configuration reader."""
    return BaseConfigurationReader(
        "tests/simlab/data/test_run_configuration.json"
    )


def test_base_configuration_reader_file_not_found() -> None:
    """Tests base configuration reader file not found."""
    with pytest.raises(FileNotFoundError):
        BaseConfigurationReader("non_existent_file.json")


def test_base_configuration_reader_invalid_file() -> None:
    """Tests base configuration reader invalid file."""
    # Create temporary file for this test
    with open("temp.txt", "w") as file:
        file.write("Test file")

    with pytest.raises(RuntimeError):
        BaseConfigurationReader("temp.txt")

    # Remove temporary file
    os.remove("temp.txt")


def test_get_component_generator(
    base_configuration_reader: BaseConfigurationReader,
) -> None:
    """Tests get component generator."""
    component_generator = base_configuration_reader._get_component_generator()

    assert isinstance(component_generator, BaseComponentGenerator)


def test_parse_task(
    base_configuration_reader: BaseConfigurationReader,
) -> None:
    """Tests parse task."""
    task = base_configuration_reader._parse_task()

    assert isinstance(task, Task)
    assert task.name == "Template Task"
    assert len(task.metrics) == 1
    assert isinstance(task.metrics[0], SuccessRate)
    assert isinstance(task.domain, SimulationDomain)


def test_parse_agents(
    base_configuration_reader: BaseConfigurationReader,
) -> None:
    """Tests parse agents."""
    agents = base_configuration_reader._parse_agent_configurations()

    assert len(agents) == 1
    assert agents[0].participant.id == "template_wrapper_agent"
    assert agents[0].custom_parameters == {}
    assert isinstance(agents[0].participant, WrapperAgent)


def test_parse_user_simulators(
    base_configuration_reader: BaseConfigurationReader,
) -> None:
    """Tests parse user simulators."""
    user_simulators = (
        base_configuration_reader._parse_user_simulator_configurations()
    )

    assert len(user_simulators) == 1
    assert user_simulators[0].image_name == "template_user_simulator"
    assert user_simulators[0].custom_parameters == {"language": "en"}
    assert (
        user_simulators[0].participant.id == "template_wrapper_user_simulator"
    )
    assert user_simulators[0].participant._uri == "http://localhost:6001"
    assert isinstance(user_simulators[0].participant, WrapperUserSimulator)
