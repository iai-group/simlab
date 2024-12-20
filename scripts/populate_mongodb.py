"""Script to populate MongoDB with supported metrics in SimLab.

The supported metrics are automatically extracted from the metrics
module.
"""

import argparse
import logging
import os
from typing import Any, Dict, List

import yaml

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records, upsert_records
from simlab.utils.configuration_readers.component_generators.base_component_generator import (  # noqa: E501
    BaseComponentGenerator,
)
from simlab.utils.utils_information_needs import (
    generate_random_information_needs,
    save_information_need_batch,
)

DEFAULT_NUM_INFORMATION_NEEDS = 1000


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(prog="populate_mongodb.py")

    parser.add_argument(
        "resource_dir",
        type=str,
        help=(
            "Path to the resource directory. It should include the folders "
            "'metrics' and 'tasks'."
        ),
    )
    parser.add_argument(
        "--mongo_uri",
        type=str,
        help="MongoDB URI to connect to the database.",
    )
    parser.add_argument(
        "--mongo_db",
        type=str,
        help="MongoDB database name.",
    )

    return parser.parse_args()


def load_new_tasks(
    tasks_dir: str, mongo_connector: MongoDBConnector
) -> List[Dict[str, Any]]:
    """Loads new task descriptions from the tasks directory.

    The task descriptions are stored in YAML files. For each new task, a batch
    of information needs is created.

    Args:
        tasks_dir: Path to the tasks directory.
        mongo_connector: MongoDB connector.

    Raises:
        FileNotFoundError: If the tasks directory does not exist.

    Returns:
        List of task descriptions that are not already in the database.
    """
    if not os.path.exists(tasks_dir):
        raise FileNotFoundError(f"Tasks directory not found: {tasks_dir}")

    task_descriptions = []
    for file in os.listdir(tasks_dir):
        if file.endswith(".yaml") or file.endswith(".yml"):
            description = yaml.safe_load(open(os.path.join(tasks_dir, file)))

            if not description.get("arguments", {}).get("batch_id"):
                # Generate information needs for the new task
                batch_id = create_information_needs_batch(
                    description, mongo_connector
                )
                description.get("arguments", {})["batch_id"] = {
                    "type": "str",
                    "value": batch_id,
                }
                # Save the updated task description
                yaml.safe_dump(
                    description, open(os.path.join(tasks_dir, file), "w")
                )

                task_descriptions.append(description)
    return task_descriptions


def load_metrics_descriptions(metrics_dir: str) -> List[Dict[str, Any]]:
    """Loads metrics descriptions from the metrics directory.

    The metrics descriptions are stored in YAML files.

    Args:
        metrics_dir: Path to the metrics directory.

    Raises:
        FileNotFoundError: If the metrics directory does not exist.

    Returns:
        List of metrics descriptions.
    """
    if not os.path.exists(metrics_dir):
        raise FileNotFoundError(f"Metrics directory not found: {metrics_dir}")

    metrics_descriptions = []
    for file in os.listdir(metrics_dir):
        if file.endswith(".yaml") or file.endswith(".yml"):
            description = yaml.safe_load(open(os.path.join(metrics_dir, file)))
            metrics_descriptions.append(description)

    return metrics_descriptions


def create_information_needs_batch(
    task_description: Dict[str, Any], mongo_connector: MongoDBConnector
) -> str:
    """Creates an information need batch for a task.

    Args:
        task_description: Task description.
        mongo_connector: MongoDB connector.

    Raises:
        ValueError: If the simulation domain is not provided in the task
          description.

    Returns:
        Batch identifier.
    """
    simulation_domain_description = task_description.get("arguments", {}).get(
        "domain", {}
    )

    if not simulation_domain_description:
        raise ValueError(
            "Simulation domain is required to create an information need batch."
        )

    component_generator = BaseComponentGenerator()
    simulation_domain = component_generator.generate_component(
        "domain",
        simulation_domain_description.get("class_name"),
        simulation_domain_description,
    )
    information_needs = generate_random_information_needs(
        simulation_domain, DEFAULT_NUM_INFORMATION_NEEDS
    )
    batch_id = save_information_need_batch(information_needs, mongo_connector)
    return batch_id


def main(args: argparse.Namespace) -> None:
    """Populates MongoDB with supported tasks and metrics in SimLab.

    Args:
        args: Command line arguments.
    """
    db_connector = (
        MongoDBConnector(args.mongo_uri)
        if args.mongo_uri
        else MongoDBConnector()
    )
    if args.mongo_db:
        db_connector.set_default_db(args.mongo_db)

    # Populate tasks
    tasks = load_new_tasks(
        os.path.join(args.resource_dir, "tasks"), db_connector
    )
    if len(tasks) > 0:
        ids = insert_records(db_connector, "tasks", tasks)
        logging.info(f"Inserted {len(ids)} new tasks in MongoDB.")
    else:
        logging.info("No new tasks to insert in MongoDB.")

    # Populate metrics
    metrics = load_metrics_descriptions(
        os.path.join(args.resource_dir, "metrics")
    )
    ids = upsert_records(db_connector, "metrics", metrics)
    logging.info(f"Inserted {len(ids)} metrics in MongoDB.")


if __name__ == "__main__":
    args = parse_args()
    main(args)
