"""Logic to perform the simulation-based evaluation of conversational agents.

Workflow:
1. Load simulation configuration and save it for future reference.
2. Instantiate all components required for the simulation.
For each agent-user simulator pair:
    3. Start containers for the agent and user simulator.
    4. Generate synthetic conversations.
    5. Evaluate the performance of the agent based on the synthetic
       conversations.
6. Aggregate and save the evaluation results.
"""

import argparse
import itertools
import os
from statistics import mean, median, stdev
from typing import Any, Dict, List, Tuple

import numpy as np
from docker.models.containers import Container

from connectors.docker.docker_registry_connector import DockerRegistryConnector
from connectors.docker.utils import get_image, run_image
from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_record
from dialoguekit.utils.dialogue_reader import json_to_dialogues
from simlab.core.information_need import InformationNeed
from simlab.core.run_configuration import (
    ParticipantConfiguration,
    RunConfiguration,
)
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.simulation_platform import SimulationPlatform
from simlab.tasks.task import Task
from simlab.utils.configuration_readers.base_configuration_reader import (
    BaseConfigurationReader,
)
from simlab.utils.participant_api.utils_api_calls import configure_participant

_NUM_ITER_PER_INFORMATION_NEED = 10


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Execute the simulation.")
    parser.add_argument(
        "config_file",
        type=str,
        help="Path to the simulation configuration file.",
    )
    parser.add_argument(
        "mongo_uri",
        type=str,
        help="MongoDB URI.",
    )
    parser.add_argument(
        "mongo_db",
        type=str,
        help="MongoDB database name.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="data/dialogue_export",
        help="Path to the output directory for the task.",
    )
    return parser.parse_args()


def load_configuration(config_file: str) -> RunConfiguration:
    """Loads the simulation configuration.

    Args:
        config_file: Path to the simulation configuration file.

    Returns:
        RunConfiguration: Simulation configuration object.
    """
    return BaseConfigurationReader(config_file).configuration


def generate_synthetic_dialogues(
    simulation_platform: SimulationPlatform,
    user_simulator: WrapperUserSimulator,
    agent: WrapperAgent,
    information_needs: List[InformationNeed],
    output_dir: str,
):
    """Generates synthetic dialogues for the given agent-user simulator pair.

    Args:
        simulation_platform: Simulation platform.
        user_simulator: User simulator.
        agent: Agent.
        information_needs: List of information needs.
        output_dir: Path to the output directory for the task.
    """
    for information_need in information_needs:
        user_simulator.set_information_need(information_need)
        simulation_platform.connect(
            user_simulator.id, user_simulator, agent, output_dir
        )
        simulation_platform.disconnect(user_simulator.id, agent.id)


def filter_existing_participant_pairs(
    output_dir: str,
    participant_pairs: List[
        Tuple[ParticipantConfiguration, ParticipantConfiguration]
    ],
) -> List[Tuple[ParticipantConfiguration, ParticipantConfiguration]]:
    """Filters out the agent-user simulator pairs which have been evaluated.

    Args:
        output_dir: Path to the output directory for the task.
        participant_pairs: List of agent-user simulator pairs.

    Returns:
        List of agent-user simulator pairs which have not been evaluated.
    """
    # TODO: Refactor to check run configuration and evaluation results in MongoDB
    filtered_pairs = []

    for agent_configuration, user_simulator_configuration in participant_pairs:
        agent_id = agent_configuration.participant.id
        user_simulator_id = user_simulator_configuration.participant.id
        if not os.path.exists(
            os.path.join(
                output_dir,
                f"{agent_id}_{user_simulator_id}.json",
            )
        ):
            filtered_pairs.append(
                (agent_configuration, user_simulator_configuration)
            )

    return filtered_pairs


def start_participant(
    registry_connector: DockerRegistryConnector,
    participant_configuration: ParticipantConfiguration,
    port: int,
) -> Container:
    """Starts a container for a participant.

    Args:
        registry_connector: Docker registry connector.
        participant_configuration: Participant configuration.
        port: Port to expose.

    Returns:
        Container running the participant.
    """
    try:
        image = get_image(
            registry_connector, participant_configuration.image_name
        )
        exposed_port = image.labels.get("exposed_port")
        run_args = {"ports": {port: exposed_port}}
        container = run_image(
            registry_connector,
            participant_configuration.image_name,
            run_args=run_args,
        )

        # Configure the participant
        participant_configuration.participant._uri = f"http://localhost:{port}"
        configure_participant(
            participant_configuration.participant._uri,
            participant_configuration.custom_parameters,
        )
        return container
    except Exception as e:
        raise RuntimeError(
            "Failed to start participant "
            f"{participant_configuration.participant.id}: {e}"
        )


def evaluate_participant_pair(
    agent_configuration: ParticipantConfiguration,
    user_simulator_configuration: ParticipantConfiguration,
    simulation_platform: SimulationPlatform,
    configuration: RunConfiguration,
    output_dir: str,
    registry_connector: DockerRegistryConnector,
) -> Dict[str, Any]:
    """Evaluates the performance of an agent-user simulator pair.

    Args:
        agent_configuration: Agent configuration.
        user_simulator_configuration: User simulator configuration.
        simulation_platform: Simulation platform.
        configuration: Simulation configuration.
        output_dir: Path to the output directory for the task.
        registry_connector: Docker registry connector

    Returns:
        Evaluation record.
    """
    # Pull images for the agent and user simulator and start the containers
    # TODO: This solution is suboptimal. See issue:
    #
    agent_port = 7000
    agent_container = start_participant(
        registry_connector, agent_configuration, agent_port
    )

    simulator_port = 7001
    simulator_container = start_participant(
        registry_connector,
        user_simulator_configuration,
        simulator_port,
    )

    agent = agent_configuration.participant
    user_simulator = user_simulator_configuration.participant

    # Generate synthetic dialogues
    # For each information need, generate N synthetic dialogues to account for
    # non-determinism of dialogue participants
    for _ in range(_NUM_ITER_PER_INFORMATION_NEED):
        generate_synthetic_dialogues(
            simulation_platform,
            user_simulator,
            agent,
            configuration.task.information_needs,
            output_dir,
        )

    # Stop the containers
    agent_container.stop()
    simulator_container.stop()

    # Evaluate the performance of the agent
    dialogues_dir = os.path.join(
        output_dir, f"{agent.id}_{user_simulator.id}.json"
    )
    results = _dialogues_evaluation(dialogues_dir, configuration.task)

    evaluation_summary = {
        "run_name": configuration.name,
        "public": configuration.public,
        "agent_id": agent.id,
        "user_simulator_id": user_simulator.id,
        "task_id": configuration.task.name,
        "information_need_batch_id": configuration.task.batch_id,
        "metrics": results,
    }
    return evaluation_summary


def _dialogues_evaluation(dialogues_dir: str, task: Task) -> Dict[str, Any]:
    """Evaluates the dialogues in the given directory.

    Args:
        dialogues_dir: Path to the directory containing the dialogues.
        task: Evaluation task.

    Returns:
       Evaluation results.
    """
    synthetic_dialogues = json_to_dialogues(dialogues_dir)
    agent_evaluation_results = task.evaluation(synthetic_dialogues)

    results = {}
    # Aggregate the evaluation results
    for metric, values in agent_evaluation_results.items():
        results[metric] = {
            "values": values,
            "mean": mean(values),
            "std": stdev(values),
            "median": median(values),
            "min": min(values),
            "max": max(values),
            "q1": np.quantile(values, 0.25),
            "q3": np.quantile(values, 0.75),
        }
    return results


def main(
    configuration: RunConfiguration,
    mongo_uri: str,
    mongo_db: str,
    output_dir: str,
) -> None:
    """Runs the simulation-based evaluation given a configuration.

    Args:
        configuration: Simulation configuration object.
        mongo_uri: MongoDB URI.
        mongo_db: MongoDB database name.
        output_dir: Path to the output directory for the task.
    """
    # Docker registry connector
    registry_connector = DockerRegistryConnector()

    # MongoDB connector
    mongo_connector = MongoDBConnector(mongo_uri, mongo_db)
    output_dir = os.path.join(
        output_dir,
        configuration.task.name,
        configuration.task.batch_id,
    )

    # Generate all possible agent-user simulator pairs
    participant_pairs = list(
        itertools.product(configuration.agents, configuration.user_simulators)
    )

    simulation_platform = SimulationPlatform(WrapperAgent)

    # Remove pairs that have already been evaluated
    participant_pairs = filter_existing_participant_pairs(
        output_dir, participant_pairs
    )

    for agent, user_simulator in participant_pairs:
        agent_evaluation_summary = evaluate_participant_pair(
            agent,
            user_simulator,
            simulation_platform,
            configuration,
            output_dir,
            registry_connector,
        )
        insert_record(
            mongo_connector,
            "evaluation_results",
            agent_evaluation_summary,
        )


if __name__ == "__main__":
    args = parse_args()
    configuration = load_configuration(args.config_file)
    main(configuration, args.mongo_uri, args.mongo_db, args.output_dir)
