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
metrics_ids = insert_records(mongo_connector, "metrics", dummy_metrics)

dummy_tasks = [
    {"name": "crs", "description": "CRS Evaluation"},
    {"name": "css", "description": "CSS Evaluation"},
]
task_ids = insert_records(mongo_connector, "tasks", dummy_tasks)

dummy_runs = [
    {
        "username": "test_user",
        "run_name": "test_run",
        "run_configuration": {
            "task": {
                "_id": task_ids[0],
                "name": "crs",
                "arguments": {
                    "n_simulations": 100,
                    "metrics": [
                        {
                            "_id": metrics_ids[0],
                            "name": "success_rate",
                        }
                    ],
                },
            },
            "agents": [
                {
                    "name": "agent",
                }
            ],
            "user_simulators": [
                {
                    "name": "user_simulator",
                }
            ],
        },
    },
    {
        "username": "test_user",
        "run_name": "test_run2",
        "run_configuration": {
            "task": {
                "_id": task_ids[1],
                "name": "css",
                "arguments": {
                    "n_simulations": 100,
                    "metrics": [
                        {
                            "_id": metrics_ids[0],
                            "name": "success_rate",
                        }
                    ],
                },
            },
            "agents": [
                {
                    "name": "agent",
                }
            ],
            "user_simulators": [
                {
                    "name": "user_simulator",
                }
            ],
        },
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
