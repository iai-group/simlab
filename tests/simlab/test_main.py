"""Tests for the main module."""

from unittest.mock import MagicMock, patch

import pytest

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
        "--mongo_uri=mongodb://localhost:27017",
        "--mongo_db=simlab_test",
        "--registry_uri=http://localhost:5000",
        "--registry_username=user",
        "--registry_password_file=tests/simlab/data/registry_password.txt",
        "--registry_repository=simlab-test-registry",
        "-o=tests/simlab/data/dialogue_export",
    ]

    monkeypatch.setattr("sys.argv", args)

    parsed_args = parse_args()
    assert parsed_args.config_file == "run_configuration.json"
    assert parsed_args.mongo_uri == "mongodb://localhost:27017"
    assert parsed_args.mongo_db == "simlab_test"
    assert parsed_args.registry_uri == "http://localhost:5000"
    assert parsed_args.registry_username == "user"
    assert (
        parsed_args.registry_password_file
        == "tests/simlab/data/registry_password.txt"
    )
    assert parsed_args.registry_repository == "simlab-test-registry"
    assert parsed_args.output_dir == "tests/simlab/data/dialogue_export"


def test_parse_args_missing_configuration(monkeypatch) -> None:
    """Tests the argument parser with missing configuration."""
    args = ["test_script"]

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
        patch("simlab.main.DockerRegistryMetadata") as mocked_docker_metadata,
        patch("simlab.main.MongoDBConnector") as mocked_mongo_connector,
        patch("simlab.main.insert_record") as mocked_insert_record,
        patch("simlab.main.json_to_dialogues") as mocked_json_to_dialogues,
        patch("simlab.main.start_participant") as mocked_start_participant,
        patch(
            "simlab.main.docker_stop_container"
        ) as mocked_docker_stop_container,
        patch(
            "simlab.main.clean_local_docker_registry"
        ) as mocked_clean_local_docker_registry,
    ):

        mocked_json_to_dialogues.return_value = [MagicMock(spec=Dialogue)]
        mocked_start_participant.return_value = (
            MagicMock(spec=str),
            [7000],
        )
        mocked_docker_stop_container.return_value = None
        mocked_clean_local_docker_registry.return_value = None

        main(
            mocked_configuration,
            mocked_mongo_connector,
            mocked_docker_metadata,
            "tests/simlab/data/dialogue_export/",
        )

        mocked_json_to_dialogues.assert_called_once_with(
            "tests/simlab/data/dialogue_export/"
            "test_agent_test_user_simulator.json"
        )
        mocked_insert_record.assert_called_once()
