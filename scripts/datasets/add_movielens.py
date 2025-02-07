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
from google.cloud import storage

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import insert_records
from simlab.core.item_collection import DEFAULT_ITEM_DB

# By default, download the 32M version of the dataset
MOVIELENS_DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-32m.zip"
DATASET_FOLDER = "data/datasets/"
GCP_BUCKET_NAME = "simlab_data"


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
    parser.add_argument(
        "--dataset_folder",
        type=str,
        help="Folder to store the dataset.",
        default=DATASET_FOLDER,
    )
    return parser.parse_args()


def download_movielens(movielens_url: str, dataset_folder: str) -> str:
    """Downloads the MovieLens dataset.

    Args:
        movielens_url: URL to download the MovieLens dataset.
        dataset_folder: Folder to store the dataset.

    Returns:
        Path to the extracted folder.
    """
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder, exist_ok=True)

    movies_zip = wget.download(movielens_url)
    with zipfile.ZipFile(movies_zip, "r") as zip_ref:
        zip_ref.extractall(dataset_folder)
    os.remove(movies_zip)

    folder_name = movies_zip.split(".zip")[0]
    return os.path.join(dataset_folder, folder_name)


def upload_to_gcp(bucket_name: str, source_folder: str):
    """Uploads files from the dataset folder to GCP bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    print("Started uploading files to GCP bucket...")
    for root, _, files in os.walk(source_folder):
        for file in files:
            local_path = os.path.join(root, file)
            blob_path = os.path.relpath(local_path, source_folder)
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_path)
            print(f"Uploaded {local_path} to gs://{bucket_name}/{blob_path}")
    print("Finished uploading files to GCP bucket.")


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

    movies_folder = download_movielens(args.ml_url, args.dataset_folder)

    # Upload dataset files to GCP
    upload_to_gcp(GCP_BUCKET_NAME, movies_folder)

    movies = prepare_movie_records(movies_folder)
    ids = insert_records(mongo_connector, "movielens", movies)
    print(f"Inserted {len(ids)} movies.")
