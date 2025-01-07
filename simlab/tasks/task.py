"""Class to represent a task."""

from typing import Dict, List

from bson import ObjectId

from connectors.mongo.mongo_connector import MongoDBConnector
from connectors.mongo.utils import find_records
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
        batch_id: str,
    ) -> None:
        """Initializes a task.

        The number of simulation to run is equal to the number of information
        needs.

        Args:
            name: Name of the task.
            domain: Domain knowledge.
            metrics: Metrics to evaluate the dialogue.
            db_name: Name of the MongoDB database.
            batch_id: Information need batch identifier.
        """
        self.name = name
        self.domain = domain
        self.metrics = metrics
        self.db_name = db_name
        self.batch_id = batch_id
        self.information_needs = self.get_information_needs(batch_id)

    def get_information_needs(self, batch_id: str) -> List[InformationNeed]:
        """Gets the information needs used for the task.

        Args:
            batch_id: Information need batch identifier.

        Returns:
            List of information needs.
        """
        information_needs = self._retrieve_information_needs(batch_id)
        self.num_simulation = len(information_needs)

        return information_needs

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
