"""MongoDB connector module.

Establishes a connection to the MongoDB database.
"""

import os

from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DEFAULT_DB = os.environ.get("MONGO_DB", "simlab")


class MongoDBConnector:
    def __init__(self) -> None:
        """Initializes the MongoDB connector."""
        super().__init__()
        self.uri = MONGO_URI
        self.client = self._connect()

    def _connect(self) -> MongoClient:
        """Connects to the MongoDB database.

        Returns:
            A MongoClient instance.
        """
        return MongoClient(self.uri)

    def close_connection(self) -> None:
        """Closes the connection to the MongoDB database."""
        self.client.close()

    def get_database(self, database_name: str = DEFAULT_DB) -> Database:
        """Gets a specific database.

        Args:
            database_name: Database name. Defaults to DEFAULT_DB.

        Returns:
            Database.
        """
        return self.client.get_database(database_name)
