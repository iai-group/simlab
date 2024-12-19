"""Logic to perform the simulation-based evaluation of conversational agents.

Workflow:
1. Load simulation configuration and save it for future reference.
2. Instantiate all components required for the simulation.
For each agent-user simulator pair:
    3. Generate synthetic conversations.
    4. Evaluate the performance of the agent based on the synthetic
       conversations.
5. Aggregate and save the evaluation results.
"""

import argparse
import itertools
import os
from statistics import mean, median, stdev
from typing import List, Tuple

import numpy as np

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_record
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import Participant
from dialoguekit.utils.dialogue_reader import json_to_dialogues
from simlab.core.information_need import InformationNeed
from simlab.core.run_configuration import RunConfiguration
from simlab.simualtion_platform import SimulationPlatform
from simlab.utils.configuration_readers.base_configuration_reader import (
    BaseConfigurationReader,
)


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Execute the simulation.")
    parser.add_argument(
        "config_file",
        type=str,
        required=True,
        help="Path to the simulation configuration file.",
    )
    parser.add_argument(
        "mongo_uri",
        type=str,
        required=True,
        help="MongoDB URI.",
    )
    parser.add_argument(
        "mongo_db",
        type=str,
        required=True,
        help="MongoDB database name.",
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
    user_simulator: Participant,
    agent: Agent,
    information_needs: List[InformationNeed],
):
    """Generates synthetic dialogues for the given agent-user simulator pair.

    Args:
        simulation_platform: Simulation platform.
        user_simulator: User simulator.
        agent: Agent.
        information_needs: List of information needs.
    """
    for information_need in information_needs:
        user_simulator.set_information_need(information_need)
        simulation_platform.connect(user_simulator.id, user_simulator, agent)
        simulation_platform.disconnect(user_simulator.id, agent.id)


def filter_existing_participant_pairs(
    output_dir: str, participant_pairs: List[Tuple[Participant, Participant]]
) -> List[Tuple[Participant, Participant]]:
    """Filters the agent-user simulator pairs which have already been evaluated.

    Args:
        output_dir: Path to the output directory for the task.
        participant_pairs: List of agent-user simulator pairs.

    Returns:
        List of agent-user simulator pairs which have not been evaluated.
    """
    filtered_pairs = []

    for agent, user_simulator in participant_pairs:
        if not os.path.exists(
            os.path.join(output_dir, f"{agent.id}_{user_simulator.id}.json")
        ):
            filtered_pairs.append((agent, user_simulator))

    return filtered_pairs


def main(
    configuration: RunConfiguration, mongo_uri: str, mongo_db: str
) -> None:
    """Runs the simulation-based evaluation given a configuration.

    Args:
        configuration: Simulation configuration object.
        mongo_uri: MongoDB URI.
        mongo_db: MongoDB database name.
    """
    mongo_connector = MongoDBConnector(mongo_uri, mongo_db)
    output_dir = os.path.join(
        "data",
        f"dialogue_export_{configuration.task.name}",
        configuration.task.batch_id,
    )
    # Generate all possible agent-user simulator pairs
    participant_pairs = itertools.product(
        configuration.agents, configuration.user_simulators
    )

    simulation_platform = SimulationPlatform(Agent)

    # Remove pairs that have already been evaluated
    participant_pairs = filter_existing_participant_pairs(
        output_dir, participant_pairs
    )

    for agent, user_simulator in participant_pairs:
        # Generate synthetic dialogues
        generate_synthetic_dialogues(
            simulation_platform,
            user_simulator,
            agent,
            configuration.task.information_needs,
        )

        # Evaluate the performance of the agent
        synthetic_dialogues = json_to_dialogues(
            os.path.join(output_dir, f"{agent.id}_{user_simulator.id}.json")
        )
        agent_evaluation_results = configuration.task.evaluation(
            synthetic_dialogues
        )
        # Aggregate and save the evaluation results
        agent_evaluation_summary = {
            "agent_id": agent.id,
            "user_simulator_id": user_simulator.id,
            "task_id": configuration.task.name,
            "information_need_batch_id": configuration.task.batch_id,
            "metrics": {},
        }
        for metric, values in agent_evaluation_results.items():
            agent_evaluation_summary["metrics"][metric] = {
                "values": values,
                "mean": mean(values),
                "std": stdev(values),
                "median": median(values),
                "min": min(values),
                "max": max(values),
                "q1": np.quantile(values, 0.25),
                "q3": np.quantile(values, 0.75),
            }
        insert_record(
            mongo_connector,
            "evaluation_results",
            agent_evaluation_summary,
        )


if __name__ == "__main__":
    args = parse_args()
    configuration = load_configuration(args.config_file)
    main(configuration, args.mongo_uri, args.mongo_db)
