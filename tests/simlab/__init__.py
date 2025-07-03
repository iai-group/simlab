"""Module level init for SimLab tests."""

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records
from simlab.core.information_need import InformationNeed

mongo_connector = MongoDBConnector()
mongo_connector.set_default_db("simlab_test")

# Insert dummy information needs into the database
dummy_information_needs = [
    InformationNeed(
        constraints={"genre": "action"},
        requests=["title", "year"],
    ).to_dict(),
    InformationNeed(
        constraints={"genre": "comedy"},
        requests=["title", "year"],
    ).to_dict(),
    InformationNeed(
        constraints={"year": 2023},
        requests=["title", "rating"],
    ).to_dict(),
    InformationNeed({"year": 2024}, ["title", "genre"]).to_dict(),
]
dummy_training_information_needs = [
    InformationNeed(
        constraints={"genre": "action"},
        requests=["title"],
    ).to_dict(),
    InformationNeed(
        constraints={"genre": "drama"},
        requests=["title", "rating"],
    ).to_dict(),
    InformationNeed(
        constraints={"year": 1999},
        requests=["title", "rating"],
    ).to_dict()
]

insert_records(
    mongo_connector,
    "information_needs",
    [
        {
            "_id": ObjectId("675380fa0f51790295720dac"),
            "information_needs": dummy_information_needs,
        },
        {
            "_id": ObjectId("675380fa0f51790295720edc"),
            "information_needs": dummy_training_information_needs,
        },
    ],
)

# Insert dummy item collections into the database
items = [
    {
        "_id": ObjectId("675380fa0f51790295721dac"),
        "title": "The Matrix",
        "year": 1999,
        "genre": "action",
        "rating": 4,
    },
    {
        "_id": ObjectId("675380fa0f51790295722dac"),
        "title": "Inception",
        "year": 2010,
        "genre": "action",
    },
    {
        "_id": ObjectId("675380fa0f51790295723dac"),
        "title": "The Titanic",
        "year": 1997,
        "genre": "romance",
    },
    {
        "_id": ObjectId("675380fa0f51790295724dac"),
        "title": "The Hangover",
        "year": 2009,
        "genre": "comedy",
        "rating": 3,
    },
]

mongo_connector.set_default_db("datasets")
insert_records(mongo_connector, "imdb_movies", items)
