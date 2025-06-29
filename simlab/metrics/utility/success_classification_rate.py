"""Zero-shot classifier to assess success of conversations"""

from dialoguekit.core.dialogue import Dialogue
from simlab.metrics.metric import Metric
from transformers import pipeline

DEFAULT_CLASSIFIER_MODEL = "facebook/bart-large-mnli"


class SuccessClassificationRate(Metric):
    def __init__(
        self,
        name: str = "success_rate",
        model_name: str = DEFAULT_CLASSIFIER_MODEL,
    ) -> None:
        """Initializes success classifier.

        Args:
            name: Name of the metric. Defaults to "success_rate".
            model_name: Name of the classifier model. Defaults to
              DEFAULT_CLASSIFIER_MODEL.
        """
        super().__init__(name)

        self.classifier = pipeline("zero-shot-classification", model=model_name)

        self.hypothesis_template = (
            "The AGENT's recommendations are {} with the USER's preferences."
        )
        self.labels = ["aligned", "misaligned"]

    def evaluate_dialogue(self, dialogue: Dialogue) -> float:
        """Evaluates a dialogue.

        Args:
            dialogue: Dialogue to evaluate.

        Returns:
            Whether the conversation is successful or not as 1 or 0
              respectively.
        """
        conv = "\n".join(
            [
                f"{utterance.participant.name}: {utterance.text}"
                for utterance in dialogue.utterances
            ]
        )

        result = self.classifier(
            conv, self.labels, hypothesis_template=self.hypothesis_template
        )

        return 1.0 if result["labels"][0] == "aligned" else 0.0
