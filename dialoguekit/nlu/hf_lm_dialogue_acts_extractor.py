"""Dialogue act extractor based on a language model hosted on Hugging Face."""

from __future__ import annotations

import re
import string
from typing import List

from transformers import pipeline

from dialoguekit.core.dialogue_act import DialogueAct
from dialoguekit.core.intent import Intent
from dialoguekit.core.slot_value_annotation import SlotValueAnnotation
from dialoguekit.core.utterance import Utterance
from dialoguekit.nlu.dialogue_acts_extractor import DialogueActsExtractor

DEFAULT_HF_MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"


class LMDialogueActsExtractor(DialogueActsExtractor):
    def __init__(
        self,
        extraction_prompt: str,
        intent_labels: List[str],
        slot_labels: List[str],
        model: str = DEFAULT_HF_MODEL,
    ) -> None:
        """Initializes the dialogue act extractor.

        Args:
            extraction_prompt: Extraction prompt.
            intent_labels: List of intent labels.
            slot_labels: List of slot labels.
            model: Hugging Face model name. Defaults to DEFAULT_HF_MODEL.
        """
        super().__init__()
        self.extraction_prompt = extraction_prompt
        self.intent_labels = intent_labels
        self.slot_labels = slot_labels
        self.model_name = model
        self.generator = pipeline(
            "text-generation", model=self.model_name, device_map="auto"
        )

    def filter_invalid_dialogue_acts(
        self,
        utterance: str,
        dialogue_acts: List[DialogueAct],
    ) -> List[DialogueAct]:
        """Filters out invalid dialogue acts.

        This method should be used after inference to filter out dialogue
        acts with invalid intents, slots, or values.

        Args:
            utterance: Input utterance.
            dialogue_acts: List of dialogue acts.

        Returns:
            List of valid dialogue acts.
        """
        filtered_dialogue_acts = []
        for dialogue_act in dialogue_acts:
            if dialogue_act.intent.label not in self.intent_labels:
                continue
            filtered_annotations = []
            for annotation in dialogue_act.annotations:
                if annotation.slot not in self.slot_labels:
                    continue
                if (
                    annotation.value is not None
                    and annotation.value not in utterance
                ):
                    continue
                filtered_annotations.append(annotation)
            filtered_dialogue_acts.append(
                DialogueAct(dialogue_act.intent, filtered_annotations)
            )
        return filtered_dialogue_acts

    def _parse_dialogue_acts(
        self, dialogue_acts: List[str]
    ) -> List[DialogueAct]:
        """Parses dialogue acts from a list of strings.

        Args:
            dialogue_acts: String representation of dialogue acts.

        Returns:
            List of dialogue acts.
        """
        parsed_dialogue_acts = []
        pattern = r"(\w+-?\w+)\((.*)\)\s*"
        for dialogue_act in dialogue_acts:
            match = re.match(pattern, dialogue_act.strip())
            if match:
                intent = Intent(match.group(1))
                slot_value_pairs = match.group(2).split(",")
                annotations = []
                for slot_value_pair in slot_value_pairs:
                    pair = slot_value_pair.split("=")
                    if len(pair) != 2:
                        continue
                    annotations.append(
                        SlotValueAnnotation(
                            pair[0].strip(), pair[1].strip().strip('"')
                        )
                    )
                parsed_dialogue_acts.append(
                    DialogueAct(intent=intent, annotations=annotations)
                )
        return parsed_dialogue_acts

    def _parse_model_output(self, model_output: str) -> List[DialogueAct]:
        """Parses model output.

        Assumes that the dialogue acts have the following format:
        intent1(slot1='value1', slot2='value2')|intent2(slot1='value3')

        Args:
            model_output: Model output.

        Returns:
            List of dialogue acts in string format.
        """
        model_output = model_output.strip()
        punctuation = (
            string.punctuation.replace('"', "")
            .replace("|", "")
            .replace(".", "")
        )
        pattern = (
            r"(\w+-?\w+\((\w+(=\"[\w\s"
            + punctuation
            + r"]+\")?,?\s?)*\)\s*\|?\s*)*"
        )
        match = re.fullmatch(pattern, model_output)
        if match:
            return self._parse_dialogue_acts(model_output.split("|"))
        return []

    def extract_dialogue_acts(self, utterance: Utterance) -> List[DialogueAct]:
        """Extracts dialogue acts from an utterance.

        Args:
            utterance: Utterance.

        Raises:
            AssertionError: If the model fails to generate dialogue acts.

        Returns:
            List of dialogue acts.
        """
        model_input = [
            {
                "role": "user",
                "content": self.extraction_prompt.format(
                    utterance=utterance.text
                ),
            }
        ]
        output = self.generator(model_input, do_sample=False, return_text=True)[
            0
        ].get("generated_text", [])
        assert "user" != output[-1].get(
            "role", ""
        ), "Model failed to generate dialogue acts."
        model_output = output[-1].get("content", "")
        dialogue_acts = self._parse_model_output(model_output)
        return self.filter_invalid_dialogue_acts(utterance.text, dialogue_acts)

    def save(self, path: str) -> None:
        """Saves the dialogue act extractor to a given path.

        This method is not implemented for this dialogue act extractor as the
        model is externally hosted.

        Args:
            path: Path to save the dialogue act extractor.
        """
        pass

    @classmethod
    def load(cls, path: str) -> LMDialogueActsExtractor:
        """Loads the dialogue act extractor from a path.

        This method is not implemented for this dialogue act extractor as the
        model is externally hosted.

        Args:
            path: Path to the dialogue act extractor.

        Returns:
            LMDialogueActsExtractor.
        """
        pass
