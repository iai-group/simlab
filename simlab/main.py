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

from connectors.docker.commands import (
    DOCKER_PASSWORD_FILE,
    DOCKER_REGISTRY_URI,
    DOCKER_REPOSITORY,
    DOCKER_USERNAME,
    DockerRegistryMetadata,
    clean_local_docker_registry,
    docker_pull_image,
    docker_run_container,
    docker_stop_container,
    inspect_image,
)
from connectors.mongo.mongo_connector import (
    DEFAULT_DB,
    MONGO_URI,
    MongoDBConnector,
)
from connectors.mongo.utils import insert_record, update_record
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
from simlab.utils.participant_api.utils_api_calls import (
    configure_participant,
    wait_for_participant,
)

_NUM_ITER_PER_INFORMATION_NEED = 3


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
    # MongoDB arguments
    parser.add_argument(
        "--mongo_uri",
        type=str,
        help="MongoDB URI.",
        default=MONGO_URI,
    )
    parser.add_argument(
        "--mongo_db",
        type=str,
        help="MongoDB database name.",
        default=DEFAULT_DB,
    )
    # Docker registry arguments
    parser.add_argument(
        "--registry_uri",
        type=str,
        help="Docker registry URI.",
        default=DOCKER_REGISTRY_URI,
    )
    parser.add_argument(
        "--registry_username",
        type=str,
        help="Docker registry username.",
        default=DOCKER_USERNAME,
    )
    parser.add_argument(
        "--registry_password_file",
        type=str,
        help="File with Docker registry password.",
        default=DOCKER_PASSWORD_FILE,
    )
    parser.add_argument(
        "--registry_repository",
        type=str,
        help="Docker registry repository.",
        default=DOCKER_REPOSITORY,
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
) -> None:
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


def start_participant(
    registry_metadata: DockerRegistryMetadata,
    participant_configuration: ParticipantConfiguration,
    port: int,
) -> Tuple[str, List[int]]:
    """Starts a container for a participant.

    Args:
        registry_metadata: Docker registry metadata.
        participant_configuration: Participant configuration.
        port: Local port to bind the container to.

    Raises:
        RuntimeError: If the participant fails to start.

    Returns:
        Container id and the list of ports used by the container.
    """
    ports_used = []
    container_id = None
    try:
        image_tag = docker_pull_image(
            participant_configuration.image, registry_metadata
        )
        image_info = inspect_image(image_tag)
        flask_exposed_port = (
            image_info.get("Config", {}).get("Labels", {}).get("port", None)
        )
        exposed_ports = [
            port.split("/")[0]
            for port in image_info["Config"]["ExposedPorts"].keys()
        ]

        if not flask_exposed_port:
            # Use the first exposed port if the port label is not found
            flask_exposed_port = exposed_ports.pop(0)
        else:
            # Check if the port is in the list of exposed ports
            if flask_exposed_port not in exposed_ports:
                raise ValueError(
                    f"Port {flask_exposed_port} not in the list of exposed"
                    " ports"
                )
            exposed_ports.remove(flask_exposed_port)

        ports_used.append(port)
        run_args = f"-p {port}:{flask_exposed_port}"

        # Configure the participant
        participant_configuration.participant._uri = f"http://localhost:{port}"

        for exposed_port in exposed_ports:
            port += 1
            ports_used.append(port)
            run_args += f" -p {port}:{exposed_port}"

        container_id = docker_run_container(
            participant_configuration.image, run_args, registry_metadata
        )

        # Wait for participant to be ready
        wait_for_participant(participant_configuration.participant._uri)

        configure_participant(
            participant_configuration.participant._uri,
            participant_configuration.participant.id,
            participant_configuration.custom_parameters,
        )
    except Exception as e:
        raise RuntimeError(
            "Failed to start participant "
            f"{participant_configuration.participant.id}: {e}"
        )
    return container_id, ports_used


def evaluate_participant_pair(
    agent_configuration: ParticipantConfiguration,
    user_simulator_configuration: ParticipantConfiguration,
    simulation_platform: SimulationPlatform,
    configuration: RunConfiguration,
    output_dir: str,
    registry_metadata: DockerRegistryMetadata,
) -> Dict[str, Any]:
    """Evaluates the performance of an agent-user simulator pair.

    Args:
        agent_configuration: Agent configuration.
        user_simulator_configuration: User simulator configuration.
        simulation_platform: Simulation platform.
        configuration: Simulation configuration.
        output_dir: Path to the output directory for the task.
        registry_metadata: Docker registry metadata.

    Returns:
        Evaluation record.
    """
    # Pull images for the agent and user simulator and start the containers
    # TODO: This solution is suboptimal. See issue:
    #
    agent_port = 7000
    agent_container_id, agent_ports = start_participant(
        registry_metadata, agent_configuration, agent_port
    )

    simulator_port = max(agent_ports) + 1
    simulator_container_id, _ = start_participant(
        registry_metadata,
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
            user_simulator,  # type: ignore[arg-type]
            agent,  # type: ignore[arg-type]
            configuration.task.information_needs,
            output_dir,
        )

    # Stop the containers
    docker_stop_container(agent_container_id)
    docker_stop_container(simulator_container_id)

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
    mongo_connector: MongoDBConnector,
    registry_metadata: DockerRegistryMetadata,
    output_dir: str,
) -> None:
    """Runs the simulation-based evaluation given a configuration.

    Args:
        configuration: Simulation configuration object.
        mongo_connector: MongoDB connector.
        registry_metadata: Docker registry metadata.
        output_dir: Path to the output directory for the task.
    """
    # Generate all possible agent-user simulator pairs
    participant_pairs = list(
        itertools.product(
            configuration.agent_configurations,
            configuration.user_simulator_configurations,
        )
    )

    simulation_platform = SimulationPlatform(WrapperAgent)

    for agent, user_simulator in participant_pairs:
        agent_evaluation_summary = evaluate_participant_pair(
            agent,
            user_simulator,
            simulation_platform,
            configuration,
            output_dir,
            registry_metadata,
        )
        insert_record(
            mongo_connector,
            "evaluation_results",
            agent_evaluation_summary,
        )


if __name__ == "__main__":
    args = parse_args()

    try:
        # MongoDB connector
        mongo_connector = MongoDBConnector(args.mongo_uri, args.mongo_db)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)

    try:
        configuration = load_configuration(args.config_file)

        # Docker registry metadata
        registry_metadata = DockerRegistryMetadata(
            args.registry_uri,
            args.registry_username,
            args.registry_password_file,
            args.registry_repository,
        )

        output_dir = os.path.join(
            args.output_dir,
            configuration.task.name,
            configuration.task.batch_id,
        )

        main(configuration, mongo_connector, registry_metadata, output_dir)
        update_record(
            mongo_connector,
            "runs",
            {"name": configuration.name},
            {"status": "completed"},
        )
    except Exception as e:
        print(f"Error during simulation: {e}")
        update_record(
            mongo_connector,
            "runs",
            {"name": configuration.name},
            {"status": "failed", "error": str(e)},
        )
    finally:
        # Delete containers and images from the local Docker registry
        clean_local_docker_registry()
