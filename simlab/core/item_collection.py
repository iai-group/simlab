"""Represent a collection of items.

An item represents an unit of information that serves as a background
for the creation of information needs. An item can be a document, a
service, a product, etc. An item collection is used to access the items
MongoDB collection. Note that an item collection is read-only.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import find_records

DEFAULT_ITEM_DB = "datasets"


@dataclass
class Item:
    """Represents an item."""

    id: str
    properties: Dict[str, Any] = field(default_factory=dict)


class ItemCollection:
    def __init__(
        self,
        collection_name,
        db_name: str = DEFAULT_ITEM_DB,
    ) -> None:
        """Initializes the item collection.

        Args:
            collection_name: Name of the item collection in MongoDB.
            db_name: Name of the MongoDB database. Defaults to DEFAULT_ITEM_DB.
        """
        self._collection_name = collection_name
        try:
            self.mongo_connector = MongoDBConnector()
            self.mongo_connector.set_default_db(db_name)
        except Exception as e:
            raise RuntimeError(f"Error connecting to MongoDB: {e}")

    def __del__(self) -> None:
        """Closes the MongoDB connection when the object is deleted."""
        self.mongo_connector.close_connection()

    def get_random_item(self) -> Item:
        """Gets a random item from the collection.

        Returns:
            A random item.
        """
        db = self.mongo_connector.get_database()
        item = (
            db[self._collection_name]
            .aggregate([{"$sample": {"size": 1}}])
            .next()
        )
        id = item.pop("_id")
        return Item(id, item)

    def get_item_by_id(self, item_id: str) -> Item:
        """Gets an item by its ID.

        Args:
            item_id: ID of the item.

        Raises:
            ValueError: If the item is not found or multiple items are found.

        Returns:
            An item.
        """
        items = find_records(
            self.mongo_connector,
            self._collection_name,
            {"_id": ObjectId(item_id)},
        )

        if len(items) > 1:
            raise ValueError(f"Multiple items with ID {item_id} found")

        item = items[0]

        if not item:
            raise ValueError(f"Item with ID {item_id} not found")

        item.pop("_id")
        return Item(item_id, item)

    def get_items(self, query: Dict[str, Any]) -> List[Item]:
        """Gets items that match a query.

        Args:
            query: Query to filter items.

        Returns:
            A list of items.
        """
        items = find_records(self.mongo_connector, self._collection_name, query)
        return [Item(item.pop("_id"), item) for item in items]

    def get_possible_property_values(self, property_name: str) -> List[str]:
        """Gets the possible values for a given property.

        Args:
            property_name: Name of the property.

        Returns:
            A list of possible values.
        """
        db = self.mongo_connector.get_database()
        return db[self._collection_name].distinct(f"properties.{property_name}")

    def get_possible_properties(self) -> Set[str]:
        """Gets the list of properties defined in the collection.

        Returns:
            A set of properties.
        """
        properties: Set[str] = set()
        for item in self.get_items({}):
            properties.update(item.properties.keys())
        return properties
