"""Module level init for backend tests."""

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records

mongo_connector = MongoDBConnector()
mongo_connector.set_default_db("simlab_test")

# Insert dummy data into the database
dummy_metrics = [
    {"name": "success_rate", "description": "Success rate"},
    {"name": "bleu", "description": "BLEU score"},
]
metrics_ids = insert_records(mongo_connector, "metrics", dummy_metrics)

dummy_tasks = [
    {
        "_id": ObjectId("675728398dd85617189bd025"),
        "name": "crs",
        "description": "CRS Evaluation",
    },
    {
        "_id": ObjectId("675728398dd85634189bd025"),
        "name": "css",
        "description": "CSS Evaluation",
    },
]
insert_records(mongo_connector, "tasks", dummy_tasks)


dummy_runs = [
    {
        "username": "test_user",
        "run_name": "test_run",
        "public": True,
        "task_id": "675728398dd85617189bd025",
        "system": {
            "type": "agent",
            "image": "dummy/agent:1.0",
            "arguments": [{"id": "TestAgent"}],
            "parameters": {},
            "class_name": "WrapperAgent",
        },
        "run_configuration_file": "dummy/config/path.json",
    },
    {
        "username": "test_user",
        "run_name": "test_run2",
        "public": True,
        "task_id": "675728398dd85634189bd025",
        "system": {
            "type": "simulator",
            "image": "dummy/simulator:1.0",
            "arguments": [{"id": "TestSimulator"}],
            "parameters": {},
            "class_name": "WrapperUserSimulator",
        },
        "run_configuration_file": "dummy/config/path2.json",
    },
]
insert_records(mongo_connector, "runs", dummy_runs)

dummy_agents = [
    {
        "name": "agent1",
        "image_name": "dummy/agent1:1.0",
        "tag": "1.0",
        "description": "Test agent 1",
        "type": "agent",
        "author": "Test Author",
        "port": 5005,
        "version": "1.0",
    },
    {
        "name": "agent2",
        "image_name": "dummy/agent2:1.0",
        "tag": "1.0",
        "description": "Test agent 2",
        "type": "agent",
        "author": "Test Author",
        "port": 5005,
        "version": "1.0",
    },
]
insert_records(mongo_connector, "system_images", dummy_agents)

dummy_simulators = [
    {
        "name": "simulator1",
        "image_name": "dummy/simulator1:1.0",
        "tag": "1.0",
        "description": "Test simulator 1",
        "type": "simulator",
        "author": "Test Author",
        "port": 5006,
        "version": "1.0",
    },
]
insert_records(mongo_connector, "system_images", dummy_simulators)
