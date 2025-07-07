"""Utility functions for parsing the response from a participant's API."""

import logging
from typing import Any, Dict, List, Tuple

from dialoguekit.core import Annotation, Intent, SlotValueAnnotation
from dialoguekit.core.dialogue_act import DialogueAct

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_API_response(
    api_response: Dict[str, Any],
) -> Tuple[str, List[DialogueAct], List[Annotation], Dict[str, Any]]:
    """Parses the response from the API.

    Args:
        api_response: Response from the API.

    Returns:
        Utterance text, dialogue acts, annotations, and metadata.
    """
    utterance_text = api_response.get("message", "")
    if not utterance_text:
        logger.warning(
            f"Empty response from the agent. See response: {api_response}"
        )

    dialogue_acts = [
        DialogueAct(
            Intent(dialogue_act.get("intent", "")),
            annotations=[
                SlotValueAnnotation(
                    annotation.get("slot", ""), annotation.get("value", "")
                )
                for annotation in dialogue_act.get("annotations", [])
            ],
        )
        for dialogue_act in api_response.get("dialogue_acts", [])
    ]

    annotations = [
        Annotation(
            annotation.get("key", ""),
            annotation.get("value", ""),
        )
        for annotation in api_response.get("annotations", [])
    ]

    metadata = api_response.get("metadata", {})

    return utterance_text, dialogue_acts, annotations, metadata
