"""Evaluate dialogues with regards to recommendation success ratio.

The success ratio of a dialogue corresponds to ratio of successful rounds of
recommendation. A round is considered successful if the user accepts a
recommended item. This ratio is computed automatically based on dialogue acts
recognized by a NLU module.

Adapted from UserSimCRS: https://github.com/iai-group/UserSimCRS
"""

from typing import List

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.dialogue import Dialogue
from dialoguekit.core.intent import Intent
from dialoguekit.nlu.nlu import NLU
from dialoguekit.participant.participant import DialogueParticipant
from simlab.metrics.metric import Metric


class RecommendationSuccessRatio(Metric):
    def __init__(
        self,
        user_nlu: NLU,
        agent_nlu: NLU,
        reject_intent_labels: List[str],
        accept_intent_labels: List[str],
        recommendation_intent_labels: List[str],
        name: str = "recommendation_success_ratio",
    ) -> None:
        """Initializes the success ratio metric.

        Args:
            user_nlu: NLU module for user utterances.
            agent_nlu: NLU module for agent utterances.
            reject_intent_labels: List of intent labels indicating rejection.
            accept_intent_labels: List of intent labels indicating acceptance.
            recommendation_intent_labels: List of intent labels indicating
              recommendation.
            name: Name of the metric. Defaults to "success_ratio".
        """
        super().__init__(name)
        self.user_nlu = user_nlu
        self.agent_nlu = agent_nlu
        self.reject_intents = [Intent(label) for label in reject_intent_labels]
        self.accept_intents = [Intent(label) for label in accept_intent_labels]
        self.recommendation_intents = [
            Intent(label) for label in recommendation_intent_labels
        ]

    def annotate_dialogue(self, dialogue: Dialogue) -> Dialogue:
        """Annotates utterances with dialogue acts.

        Args:
            dialogue: Dialogue to be annotated.

        Raises:
            ValueError: If the participant is unknown.

        Returns:
            Annotated dialogue.
        """
        for i, utterance in enumerate(dialogue.utterances):
            if not isinstance(utterance, AnnotatedUtterance):
                dialogue.utterances[i] = AnnotatedUtterance.from_utterance(
                    utterance
                )

            if len(utterance.dialogue_acts) > 0:
                continue

            if utterance.participant == DialogueParticipant.USER:
                dialogue.utterances[
                    i
                ].dialogue_acts = self.user_nlu.extract_dialogue_acts(utterance)
            elif utterance.participant == DialogueParticipant.AGENT:
                dialogue.utterances[
                    i
                ].dialogue_acts = self.agent_nlu.extract_dialogue_acts(
                    utterance
                )
            else:
                raise ValueError(
                    f"Unknown participant: {utterance.participant}"
                )
        return dialogue

    def get_recommendation_rounds(
        self, dialogue: Dialogue
    ) -> List[List[AnnotatedUtterance]]:
        """Gets utterances per recommendation round.

        Args:
            dialogue: Dialogue.

        Returns:
            Utterances per recommendation round.
        """
        rounds = []
        current_round = []
        for utterance in dialogue.utterances:
            if any(
                intent in utterance.get_intents()
                for intent in self.recommendation_intents
            ):
                if current_round:
                    rounds.append(current_round)
                current_round = [utterance]
            else:
                current_round.append(utterance)
        return rounds

    def is_recommendation_accepted(
        self, round: List[AnnotatedUtterance]
    ) -> bool:
        """Assesses whether the recommendation was accepted.

        Args:
            round: Utterances in recommendation round.

        Returns:
            True if the recommendation was accepted, False otherwise.
        """
        b_accepted = False
        for utterance in round:
            if utterance.participant == DialogueParticipant.USER:
                intents = utterance.get_intents()
                if any(intent in self.accept_intents for intent in intents):
                    b_accepted = True
                elif any(intent in self.reject_intents for intent in intents):
                    return False
        return b_accepted

    def evaluate_dialogue(self, dialogue: Dialogue) -> float:
        """Evaluates the ratio of successful rounds of recommendation.

        Args:
            dialogue: Dialogue to evaluate.

        Returns:
            Ratio of successful rounds of recommendation, or 0 if no
            recommendation rounds are found.
        """
        rounds = self.get_recommendation_rounds(dialogue)
        successful_rounds = 0
        for round in rounds:
            if self.is_recommendation_accepted(round):
                successful_rounds += 1
        return successful_rounds / len(rounds) if rounds else 0.0
