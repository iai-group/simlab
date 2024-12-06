"""Class to represent a task."""

from typing import Dict, List, Optional, Tuple

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import find_records, insert_records
from dialoguekit.core.dialogue import Dialogue
from simlab.core.information_need import InformationNeed
from simlab.core.simulation_domain import SimulationDomain
from simlab.metrics.metric import Metric


class Task:
    def __init__(
        self,
        name: str,
        domain: SimulationDomain,
        metrics: List[Metric],
        db_name: str,
    ) -> None:
        """Initializes a task.

        Args:
            name: Name of the task.
            domain: Domain knowledge.
            metrics: Metrics to evaluate the dialogue.
            db_name: Name of the MongoDB database.
        """
        self.name = name
        self.domain = domain
        self.metrics = metrics
        self.db_name = db_name

    def get_information_needs(
        self, n: Optional[int] = None, batch_id: Optional[str] = None
    ) -> Tuple[str, List[InformationNeed]]:
        """Gets the information needs used for the task.

        If batch_id is provided, n is ignored and the information needs are
        retrieved from a previous batch.

        Args:
            n: Number of information needs to generate. Defaults to None.
            batch_id: Information need batch identifier. Defaults to None.

        Raises:
            ValueError: If both parameters are None.

        Returns:
            Batch identifier and list of information needs.
        """
        if not n and not batch_id:
            raise ValueError("Either n or batch_id must be provided.")

        if batch_id:
            return batch_id, self._retrieve_information_needs(batch_id)

        # Generate new batch of information needs
        information_needs: List[InformationNeed] = []
        # TODO: Implement a function to generate random information needs
        # Save new batch of information needs to MongoDB
        batch_id = self.save_information_need_batch(information_needs)

        return batch_id, information_needs

    def _retrieve_information_needs(
        self, batch_id: str
    ) -> List[InformationNeed]:
        """Retrieves information needs from a previous batch.

        Args:
            batch_id: Information need batch identifier.

        Raises:
            ValueError: If the batch_id is not found.

        Returns:
            List of information needs.
        """
        # Retrieve information needs from MongoDB
        information_needs: List[InformationNeed] = []
        mongo_connector = MongoDBConnector()
        mongo_connector.set_default_db(self.db_name)

        batch = find_records(
            mongo_connector, "information_needs", {"_id": ObjectId(batch_id)}
        )

        if not batch:
            raise ValueError(f"Batch with id {batch_id} not found.")

        for record in batch[0].get("information_needs", []):
            information_needs.append(InformationNeed.from_dict(record))

        mongo_connector.close_connection()

        return information_needs

    def evaluation(self, dialogues: List[Dialogue]) -> Dict[str, List[float]]:
        """Evaluates the dialogues using the metrics.

        Args:
            dialogues: Dialogues to evaluate.

        Returns:
            Evaluation scores for each metric.
        """
        return {
            metric.name: metric.evaluate_dialogues(dialogues)
            for metric in self.metrics
        }

    def save_information_need_batch(
        self, information_needs: List[InformationNeed]
    ) -> str:
        """Saves a batch of information needs to the database.

        Args:
            information_needs: List of information needs.

        Returns:
            Batch identifier.
        """
        mongo_connector = MongoDBConnector()
        mongo_connector.set_default_db(self.db_name)

        records = []
        for information_need in information_needs:
            record = information_need.to_dict()
            records.append(record)

        ids = insert_records(
            mongo_connector,
            "information_needs",
            [{"information_needs": records}],
        )

        assert (
            len(ids) == 1
        ), "Error saving information needs. More than one batch id is saved."

        mongo_connector.close_connection()

        return str(ids[0])
