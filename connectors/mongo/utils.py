"""Utility functions for database operations."""

import logging
from typing import Any, Dict, List, Union

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector


def find_records(
    connector: MongoDBConnector,
    collection: str,
    query: Dict[str, Union[str, bool, int, ObjectId, Dict]],
) -> List[Dict[str, Any]]:
    """Finds records in a collection that match a query.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        query: Query.

    Returns:
        List of records.
    """
    records = []
    db = connector.get_database()
    try:
        for record in db[collection].find(query):
            records.append(parse_object_id_to_str(record))
    except Exception as e:
        logging.error(f"Error finding records: {e}")
    return records  # type: ignore


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


def update_record(
    connector: MongoDBConnector,
    collection: str,
    query: Dict[str, Any],
    update: Dict[str, Any],
) -> bool:
    """Updates a record in a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        query: Query to match the record to update.
        update: Update to apply.

    Returns:
        True if the record was updated successfully, False otherwise.
    """
    db = connector.get_database()
    try:
        db[collection].update_one(query, {"$set": update})
    except Exception as e:
        logging.error(f"Error updating record: {e}")
        return False
    return True


def upsert_records(
    connector: MongoDBConnector, collection: str, records: List[Dict[str, Any]]
) -> List[str]:
    """Inserts or updates multiple records into a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        records: Records to insert or update.

    Returns:
        List of IDs of the inserted or updated records.
    """
    db = connector.get_database()
    ids = []
    try:
        for record in records:
            query = {key: record[key] for key in record if key != "_id"}
            r = db[collection].update_one(query, {"$set": record}, upsert=True)
            ids.append(r.upserted_id or record.get("_id"))
    except Exception as e:
        logging.error(f"Error upserting records: {e}")
    return ids


def delete_records(
    connector: MongoDBConnector, collection: str, query: Dict[str, Any]
) -> bool:
    """Deletes a record from a collection.

    Args:
        connector: MongoDB connector.
        collection: Collection name.
        query: Query to match the record to delete.

    Returns:
        True if the record was deleted successfully, False otherwise.
    """
    db = connector.get_database()
    nb_deleted = 0
    try:
        nb_deleted = db[collection].delete_many(query).deleted_count
        logging.info(f"Deleted {nb_deleted} records")
    except Exception as e:
        logging.error(f"Error deleting record: {e}")
        return False
    return nb_deleted > 0


def parse_object_id_to_str(
    data: Union[Dict[str, Any], List[Any], ObjectId]
) -> Union[Dict[str, Any], List[Any], str]:
    """Parses ObjectId to string recursively.

    Args:
        data: Data to parse.

    Returns:
        Data with ObjectId parsed to string.
    """
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, list):
        return [parse_object_id_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {
            key: parse_object_id_to_str(value) for key, value in data.items()
        }
    return data
