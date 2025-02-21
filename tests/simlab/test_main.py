"""Tests for the main module."""

from unittest.mock import MagicMock, patch

import pytest

from dialoguekit.core.dialogue import Dialogue
from simlab.core.information_need import InformationNeed
from simlab.core.run_configuration import RunConfiguration
from simlab.main import (
    filter_existing_participant_pairs,
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


def test_filter_existing_participant_pairs() -> None:
    """Tests the filter_existing_participant_pairs function."""
    mocked_agent = MagicMock(id="test_agent_1")
    mocker_simulator_1 = MagicMock(id="test_user_1")
    mocker_simulator_2 = MagicMock(id="test_user_2")
    participant_pairs = [
        (mocked_agent, mocker_simulator_1),
        (mocked_agent, mocker_simulator_2),
    ]

    # Mock os.path.exists to return True for the first pair and False for the
    # second.
    with patch("os.path.exists", side_effect=[True, False]):
        filtered_pairs = filter_existing_participant_pairs(
            "output_dir", participant_pairs
        )
        assert filtered_pairs == [(mocked_agent, mocker_simulator_2)]


def test_main(task: Task) -> None:
    """Tests the main function."""
    # Mock dependencies
    mocked_configuration = MagicMock(spec=RunConfiguration)
    mocked_configuration.task = task
    mocked_configuration.agents = [
        MagicMock(spec=WrapperAgent, id="test_agent")
    ]
    mocked_configuration.user_simulators = [
        MagicMock(spec=WrapperUserSimulator, id="test_user_simulator")
    ]

    with (
        patch("simlab.main.MongoDBConnector") as mocked_mongo_connector,
        patch("simlab.main.insert_record") as mocked_insert_record,
        patch("simlab.main.json_to_dialogues") as mocked_json_to_dialogues,
    ):

        mocked_json_to_dialogues.return_value = [MagicMock(spec=Dialogue)]

        main(
            mocked_configuration,
            "mongodb://localhost:27017",
            "simlab_test",
            "tests/simlab/data/dialogue_export",
        )

        mocked_mongo_connector.assert_called_once_with(
            "mongodb://localhost:27017", "simlab_test"
        )
        mocked_json_to_dialogues.assert_called_once_with(
            "tests/simlab/data/dialogue_export/task_testing/"
            "675380fa0f51790295720dac/test_agent_test_user_simulator.json"
        )
        mocked_insert_record.assert_called_once()
