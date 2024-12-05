"""Script to populate MongoDB with supported metrics in SimLab.

The supported metrics are automatically extracted from the metrics
module.
"""

import argparse
import importlib
import inspect
import logging
from typing import Dict, List

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records
from simlab.metrics.metric import Metric


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(prog="populate_mongodb.py")

    parser.add_argument(
        "--mongo-uri",
        type=str,
        help="MongoDB URI to connect to the database.",
    )
    parser.add_argument(
        "--mongo-db",
        type=str,
        help="MongoDB database name.",
    )

    return parser.parse_args()


def parse_module(module: str, base_class) -> List[Dict[str, str]]:
    """Parses a module to extract classes that inherit from a base class.

    Args:
        module: Module name.
        base_class: Base class to filter classes.

    Returns:
        List of names and descriptions of the extracted classes.
    """
    classes = []
    try:
        module = importlib.import_module(module)
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, base_class) and cls != base_class:
                description = (
                    cls.description
                    if hasattr(cls, "description")
                    else cls.__doc__
                )
                classes.append({"name": name, "description": description})
    except Exception as e:
        logging.error(f"Error parsing module {module}: {e}")

    return classes


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

    # Parse all metrics inheriting from Metric class
    metrics = parse_module("simlab.metrics", Metric)
    ids = insert_records(db_connector, "metrics", metrics)

    logging.info(f"Inserted {len(ids)} metrics")
    db_connector.close_connection()


if __name__ == "__main__":
    args = parse_args()
    main(args)
