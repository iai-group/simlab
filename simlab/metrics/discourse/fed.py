"""Evaluate dialogues with regards to discourse features.

The supported features are:
- Coherent
- Error Recovery
- Consistent
- Diverse
- Topic Depth
- Likeable
- Understanding
- Flexible
- Informative
- Inquisitive
- Overall Impression

Reference:
Mehri S, Eskenazi M. Unsupervised evaluation of interactive dialog with
DialoGPT. arXiv preprint arXiv:2006.12719. 2020.

Adapted from original implementation: https://github.com/Shikib/fed
"""

from typing import Dict, List

import torch
from transformers import AutoModelWithLMHead, AutoTokenizer

from dialoguekit.core.dialogue import Dialogue
from simlab.metrics.metric import Metric


class FED(Metric):
    def __init__(self, feature: str, name: str = "fed") -> None:
        """Initializes the FED metric for a specific feature.

        Args:
            feature: The feature to evaluate.
            name: Name of the metric. Defaults to "fed".
        """
        super().__init__(f"{name}_{feature}")
        self.feature = feature

        self._model_name = "microsoft/DialoGPT-large"
        self._eou_token = " <|endoftext|> "  # End of utterance token
        self.tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        self.model = AutoModelWithLMHead.from_pretrained(self._model_name)

    @property
    def features(self) -> Dict[str, Dict[str, List[str]]]:
        """Returns the supported features and their corresponding examples."""
        return {
            "coherent": {
                "positive": [],
                "negative": [
                    "You're making no sense at all.",
                    "You're changing the topic so much!",
                    "You are so confusing.",
                ],
            },
            "error_recovery": {
                "positive": [],
                "negative": [
                    "I am so confused right now.",
                    "You're really confusing.",
                    "I don't understand what you're saying.",
                ],
            },
            "consistent": {
                "positive": [],
                "negative": [
                    "That's not what you said earlier!",
                    "Stop contradicting yourself!",
                ],
            },
            "diverse": {
                "positive": [],
                "negative": [
                    "Stop saying the same thing repeatedly.",
                    "Why are you repeating yourself?",
                    "Stop repeating yourself!",
                ],
            },
            "depth": {
                "positive": [],
                "negative": [
                    "Stop changing the topic so much.",
                    "Don't change the topic!",
                ],
            },
            "likeable": {
                "positive": [
                    "I like you!",
                    "You're super polite and fun to talk to",
                    "Great talking to you.",
                ],
                "negative": [
                    "You're not very nice.",
                    "You're not very fun to talk to.",
                    "I don't like you.",
                ],
            },
            "understand": {
                "positive": [],
                "negative": [
                    "You're not understanding me!",
                    "What are you trying to say?",
                    "I don't understand what you're saying.",
                ],
            },
            "flexible": {
                "positive": [
                    "You're very easy to talk to!",
                    "Wow you can talk about a lot of things!",
                ],
                "negative": [
                    "I don't want to talk about that!",
                    "Do you know how to talk about something else?",
                ],
            },
            "informative": {
                "positive": [
                    "Thanks for all the information!",
                    "Wow that's a lot of information.",
                    "You know a lot of facts!",
                ],
                "negative": [
                    "You're really boring.",
                    "You don't really know much.",
                ],
            },
            "inquisitive": {
                "positive": [
                    "You ask a lot of questions!",
                    "That's a lot of questions!",
                ],
                "negative": [
                    "You don't ask many questions.",
                    "You don't seem interested.",
                ],
            },
        }

    def _format_dialogue(self, dialogue: Dialogue) -> str:
        """Formats a dialogue as a single string.

        Args:
            dialogue: Dialogue to format.

        Returns:
            Formatted dialogue.
        """
        dialogue_text = ""
        for utterance in dialogue.utterances:
            dialogue_text += f"{self._eou_token}{utterance.text}"
        return dialogue_text

    def _score(self, dialogue: str, example: str) -> float:
        """Computes log-likelihood score of DialoGPT generating a response.

        Args:
            dialogue: Dialogue text.
            example: Example text.

        Returns:
            Log-likelihood score.
        """
        if not dialogue.startswith(self._eou_token):
            dialogue = f"{self._eou_token}{dialogue}"

        input_text = f"{dialogue}{self._eou_token}{example}"
        input_text = input_text.strip()

        tokenize_input = self.tokenizer.tokenize(input_text)
        if len(tokenize_input) >= 1024:
            tokenize_input = [self._eou_token] + tokenize_input[-1024:]
        tensor_input = torch.tensor(
            [self.tokenizer.convert_tokens_to_ids(tokenize_input)]
        )
        with torch.no_grad():
            output = self.model(tensor_input, labels=tensor_input)
            loss, _ = output[:2]
        return loss.item()

    def evaluate_dialogue(self, dialogue: Dialogue) -> float:
        """Evaluates a dialogue with respect to the specified feature.

        Args:
            dialogue: Dialogue to evaluate.

        Returns:
            Evaluation score.
        """
        examples = self.features.get(self.feature, {})
        positive_examples = examples.get("positive", [])
        negative_examples = examples.get("negative", [])

        dialogue_text = self._format_dialogue(dialogue)

        high_score = 0
        for example in positive_examples:
            hs = self._score(dialogue_text, example)
            high_score += hs
        high_score = high_score / max(len(positive_examples), 1)

        low_score = 0
        for example in negative_examples:
            ls = self._score(dialogue_text, example)
            low_score += ls
        low_score = low_score / max(len(negative_examples), 1)

        return low_score - high_score
