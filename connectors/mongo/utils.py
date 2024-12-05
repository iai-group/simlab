"""Utility functions for database operations."""

import logging
from typing import Any, Dict, List

from webapp.backend.connectors.mongo.mongo_connector import MongoDBConnector


def find_records(
    connector: MongoDBConnector, collection: str, query: str
) -> List[Dict[str, Any]]:
    """Finds records in a collection that match a query.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        query: Query.

    Returns:
        List of records.
    """
    db = connector.get_database()
    try:
        return [record for record in db[collection].find(query)]
    except Exception as e:
        logging.error(f"Error finding records: {e}")
    return []


def insert_record(
    connector: MongoDBConnector, collection: str, record: Dict[str, Any]
) -> str:
    """Inserts a record into a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        record: Record to insert.

    Returns:
        ID of the inserted record.
    """
    db = connector.get_database()
    try:
        id = db[collection].insert_one(record).inserted_id
        return id
    except Exception as e:
        logging.error(f"Error inserting record: {e}")
    return None


def insert_records(
    connector: MongoDBConnector, collection: str, records: List[Dict[str, Any]]
) -> List[str]:
    """Inserts multiple records into a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        records: Records to insert.

    Returns:
        List of IDs of the inserted records.
    """
    db = connector.get_database()
    try:
        ids = db[collection].insert_many(records).inserted_ids
        return ids
    except Exception as e:
        logging.error(f"Error inserting records: {e}")
    return []


def delete_records(
    connector: MongoDBConnector, collection: str, query: Dict[str, Any]
) -> None:
    """Deletes a record from a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        query: Query to match the record to delete.
    """
    db = connector.get_database()
    try:
        nb_deleted = db[collection].delete_many(query).deleted_count
        logging.info(f"Deleted {nb_deleted} records")
    except Exception as e:
        logging.error(f"Error deleting record: {e}")
