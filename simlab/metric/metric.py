"""Base class for metrics to evaluate a dialogue."""

from abc import ABC, abstractmethod
from typing import List

from dialoguekit.core.dialogue import Dialogue


class Metric(ABC):
    def __init__(self, name: str) -> None:
        """Initializes a metric.

        Args:
            name: Name of the metric.
        """
        self.name = name

    @abstractmethod
    def evaluate_dialogue(self, dialogue: Dialogue) -> float:
        """Evaluates a dialogue.

        Args:
            dialogue: Dialogue to evaluate.

        Raises:
            NotImplementedError: Subclasses must implement this method.

        Returns:
            Evaluation score.
        """
        raise NotImplementedError

    def evaluate_dialogues(self, dialogues: List[Dialogue]) -> List[float]:
        """Evaluates multiple dialogues.

        Args:
            dialogues: Dialogues to evaluate.

        Returns:
            List of evaluation scores.
        """
        return [self.evaluate_dialogue(dialogue) for dialogue in dialogues]
