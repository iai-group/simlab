"""Module level init for backend tests."""

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records

mongo_connector = MongoDBConnector()
mongo_connector.set_default_db("simlab_test")

# Insert dummy data into the database
dummy_metrics = [
    {"name": "success_rate", "description": "Success rate"},
    {"name": "bleu", "description": "BLEU score"},
]
insert_records(mongo_connector, "metrics", dummy_metrics)

dummy_tasks = [
    {"name": "crs", "description": "CRS Evaluation"},
    {"name": "css", "description": "CSS Evaluation"},
]
insert_records(mongo_connector, "tasks", dummy_tasks)
