"""MongoDB connector module.

Establishes a connection to the MongoDB database.
"""

import os

from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DEFAULT_DB = os.environ.get("MONGO_DB", "simlab")


class MongoDBConnector:
    def __init__(
        self, uri: str = MONGO_URI, default_db: str = DEFAULT_DB
    ) -> None:
        """Initializes the MongoDB connector.

        Args:
            uri: MongoDB URI. Defaults to MONGO_URI.
            default_db: Default database name. Defaults to DEFAULT_DB.
        """
        super().__init__()
        self.uri = uri
        self.default_db = default_db
        self.client = self._connect()

    def set_default_db(self, default_db: str) -> None:
        """Sets the default database.

        Args:
            default_db: Default database name.
        """
        self.default_db = default_db

    def _connect(self) -> MongoClient:
        """Connects to the MongoDB database.

        Returns:
            A MongoClient instance.
        """
        return MongoClient(self.uri)

    def close_connection(self) -> None:
        """Closes the connection to the MongoDB database."""
        self.client.close()

    def get_database(self, database_name: str = None) -> Database:
        """Gets a specific database.

        Args:
            database_name: Database name. Defaults to None.

        Returns:
            Database.
        """
        if not database_name:
            return self.client.get_database(self.default_db)
        return self.client.get_database(database_name)
