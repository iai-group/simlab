"""Success rate metric."""

from simlab.metrics.metric import Metric


class SuccessRate(Metric):

    description = "Success rate metric."

    def __init__(self, name: str = "success_rate") -> None:
        """Initializes the success rate metric.

        Args:
            name: Name of the metric. Defaults to "success_rate".
        """
        super().__init__(name)

    def evaluate_dialogue(self, dialogue) -> float:
        """Evaluates if the dialogue is successful.

        Args:
            dialogue: Dialogue to evaluate.

        Returns:
            1 if the dialogue is successful, 0 otherwise.
        """
        # TODO: Implement this method
        pass
