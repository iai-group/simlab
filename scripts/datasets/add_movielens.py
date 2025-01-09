"""Script to add MovieLens dataset to MongoDB.

Dataset website:
https://grouplens.org/datasets/movielens/

Citation:
F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History
and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5,
4: 19:1-19:19. https://doi.org/10.1145/2827872
"""

import argparse
import os
import re
import zipfile
from typing import Any, Dict, List

import pandas as pd
import wget

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records
from simlab.core.item_collection import DEFAULT_ITEM_DB

# By default, download the 32M version of the dataset
MOVIELENS_DATA_URL = (
    "https://files.grouplens.org/datasets/movielens/ml-32m.zip"
)


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(prog="add_movielens.py")
    parser.add_argument(
        "--ml_url",
        type=str,
        default=MOVIELENS_DATA_URL,
        help="URL to download the MovieLens dataset.",
    )
    parser.add_argument(
        "--mongo_uri",
        type=str,
        help="MongoDB URI to connect to the database.",
    )
    parser.add_argument(
        "--mongo_db",
        type=str,
        help="MongoDB database name.",
        default=DEFAULT_ITEM_DB,
    )

    return parser.parse_args()


def download_movielens(movielens_url: str) -> str:
    """Downloads the MovieLens dataset.

    Returns:
        Path to the extracted folder.
    """
    movies_zip = wget.download(movielens_url)
    with zipfile.ZipFile(movies_zip, "r") as zip_ref:
        zip_ref.extractall("temp")
    os.remove(movies_zip)

    folder_name = movies_zip.split(".zip")[0]
    return f"temp/{folder_name}"


def prepare_movie_records(folder_name: str) -> List[Dict[str, Any]]:
    """Prepares the movie records to be inserted into the database.

    Args:
        folder_name: Folder where the dataset is extracted

    Returns:
        List of movie records.
    """
    records = []

    movies_df = pd.read_csv(os.path.join(folder_name, "movies.csv"))
    tags_df = pd.read_csv(os.path.join(folder_name, "tags.csv"))

    for _, row in movies_df.iterrows():
        movie_id = row["movieId"]

        title = row["title"]

        # Extract year from the title
        year = None
        match = re.search(r"\(\d{4}\)", title)
        if match:
            year = match.group(0)
            year = year[1:-1].strip()
            title = re.sub(r"\(\d{4}\)", "", title).strip()

        genres = row["genres"].split("|")

        tags = tags_df[tags_df["movieId"] == movie_id]["tag"].tolist()
        # Remove duplicate tags
        tags = list(set(tags))

        record = {
            "movieId": row["movieId"],
            "title": title,
            "genres": genres,
            "keywords": tags,
            "year": year,
        }

        records.append(record)

    return records


if __name__ == "__main__":
    args = parse_args()

    mongo_connector = MongoDBConnector(args.mongo_uri, args.mongo_db)

    movies_folder = download_movielens(args.ml_url)

    movies = prepare_movie_records(movies_folder)
    ids = insert_records(mongo_connector, "movielens", movies)
    print(f"Inserted {len(ids)} movies.")

    os.system(f"rm -rf {movies_folder}")
