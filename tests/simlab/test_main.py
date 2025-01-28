"""Tests for the main module."""

from unittest.mock import MagicMock, patch

import pytest
from docker.models.containers import Container

from dialoguekit.core.dialogue import Dialogue
from simlab.core.information_need import InformationNeed
from simlab.core.run_configuration import (
    ParticipantConfiguration,
    RunConfiguration,
)
from simlab.main import (
    generate_synthetic_dialogues,
    load_configuration,
    main,
    parse_args,
)
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.simulation_platform import SimulationPlatform
from simlab.tasks import Task
from simlab.utils.configuration_readers.base_configuration_reader import (
    BaseConfigurationReader,
)


def test_parse_args(monkeypatch) -> None:
    """Tests the argument parser."""
    args = [
        "test_script",
        "run_configuration.json",
        "mongodb://localhost:27017",
        "simlab_test",
        "http://localhost:5000",
        "user",
        "pwd",
        "-o=tests/simlab/data/dialogue_export",
    ]

    monkeypatch.setattr("sys.argv", args)

    parsed_args = parse_args()
    assert parsed_args.config_file == "run_configuration.json"
    assert parsed_args.mongo_uri == "mongodb://localhost:27017"
    assert parsed_args.mongo_db == "simlab_test"
    assert parsed_args.output_dir == "tests/simlab/data/dialogue_export"


def test_parse_args_missing_args(monkeypatch) -> None:
    """Tests the argument parser with missing arguments."""
    args = ["test_script", "run_configuration.json"]

    monkeypatch.setattr("sys.argv", args)

    with pytest.raises(SystemExit):
        parse_args()


def test_load_configuration() -> None:
    """Tests the load_configuration function."""
    mock_configuration = MagicMock(spec=RunConfiguration)
    mock_configuration_reader = MagicMock(spec=BaseConfigurationReader)
    mock_configuration_reader.configuration = mock_configuration

    with patch(
        "simlab.main.BaseConfigurationReader",
        return_value=mock_configuration_reader,
    ) as mock_reader_class:
        configuration = load_configuration("run_configuration.json")
        assert configuration == mock_configuration
        mock_reader_class.assert_called_once_with("run_configuration.json")


def test_generate_synthetic_dialogues(
    information_need: InformationNeed,
) -> None:
    """Tests the generate_synthetic_dialogues function."""
    mocked_simulation_platform = MagicMock(spec=SimulationPlatform)
    mocked_user_simulator = MagicMock(
        spec=WrapperUserSimulator, id="test_simulator"
    )
    mocked_agent = MagicMock(spec=WrapperAgent, id="test_agent")

    generate_synthetic_dialogues(
        mocked_simulation_platform,
        mocked_user_simulator,
        mocked_agent,
        [information_need],
        "tests/simlab/data/dialogue_export",
    )

    mocked_user_simulator.set_information_need.assert_called_once_with(
        information_need
    )
    mocked_simulation_platform.connect.assert_called_once_with(
        "test_simulator",
        mocked_user_simulator,
        mocked_agent,
        "tests/simlab/data/dialogue_export",
    )
    mocked_simulation_platform.disconnect.assert_called_once_with(
        "test_simulator", "test_agent"
    )


def test_main(task: Task) -> None:
    """Tests the main function."""
    # Mock dependencies
    mocked_configuration = MagicMock(spec=RunConfiguration)
    mocked_configuration.name = "test_run"
    mocked_configuration.public = True
    mocked_configuration.task = task
    mocked_configuration.agent_configurations = [
        MagicMock(
            spec=ParticipantConfiguration,
            image="template_agent",
            participant=MagicMock(spec=WrapperAgent, id="test_agent"),
        )
    ]
    mocked_configuration.user_simulator_configurations = [
        MagicMock(
            spec=ParticipantConfiguration,
            image="template_user_simulator",
            participant=MagicMock(
                spec=WrapperUserSimulator, id="test_user_simulator"
            ),
        )
    ]
    with (
        patch(
            "simlab.main.DockerRegistryConnector"
        ) as mocked_docker_connector,
        patch("simlab.main.MongoDBConnector") as mocked_mongo_connector,
        patch("simlab.main.insert_record") as mocked_insert_record,
        patch("simlab.main.json_to_dialogues") as mocked_json_to_dialogues,
        patch("simlab.main.start_participant") as mocked_start_participant,
    ):

        mocked_json_to_dialogues.return_value = [MagicMock(spec=Dialogue)]
        mocked_start_participant.return_value = MagicMock(spec=Container)

        main(
            mocked_configuration,
            mocked_mongo_connector,
            mocked_docker_connector,
            "tests/simlab/data/dialogue_export/",
        )

        mocked_json_to_dialogues.assert_called_once_with(
            "tests/simlab/data/dialogue_export/"
            "test_agent_test_user_simulator.json"
        )
        mocked_insert_record.assert_called_once()
