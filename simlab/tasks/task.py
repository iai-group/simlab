"""Class to represent a task."""

from typing import Dict, List, Optional

from dialoguekit.core.dialogue import Dialogue
from simlab.core.information_need import InformationNeed
from simlab.core.simulation_domain import SimulationDomain
from simlab.metrics.metric import Metric


class Task:
    def __init__(
        self, name: str, domain: SimulationDomain, metrics: List[Metric]
    ) -> None:
        """Initializes a task.

        Args:
            name: Name of the task.
            domain: Domain knowledge.
            metrics: Metrics to evaluate the dialogue.
        """
        self.name = name
        self.domain = domain
        self.metrics = metrics

    def get_information_needs(
        self, n: int, batch_id: Optional[str] = None
    ) -> List[InformationNeed]:
        """Gets the information needs used for the task.

        If batch_id is provided, n is ignored and the information needs are
        retrieved from a previous batch.

        Args:
            n: Number of information needs to generate.
            batch_id: Information need batch identifier. Defaults to None.

        Returns:
            List of information needs.
        """
        if batch_id:
            return self._retrieve_information_needs(batch_id)

        # Generate new batch of information needs
        information_needs: List[InformationNeed] = []
        # TODO: Implement a function to generate random information needs
        # new_batch_id = None
        # Save new batch of information needs to MongoDB

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
