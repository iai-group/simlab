"""Interface to represent an information need.

The information need comprises two elements: constraints and requests.
The constraints specify the slot-value pairs that the item of interest
must satisfy, while the requests specify the slots for which the user
wants information.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


class InformationNeed:
    def __init__(
        self, constraints: Dict[str, Any], requests: List[str]
    ) -> None:
        """Initializes an information need.

        Args:
            constraints: Slot-value pairs representing constraints on the item
              of interest.
            requests: Slots representing the desired information.
        """
        self.constraints = constraints
        self.requested_slots = defaultdict(
            None, {slot: None for slot in requests}
        )

    def get_constraint_value(self, slot: str) -> Any:
        """Returns the value of a constraint slot.

        Args:
            slot: Slot.

        Returns:
            Value of the slot.
        """
        return self.constraints.get(slot)

    def get_requestable_slots(self) -> List[str]:
        """Returns the list of requestable slots."""
        return [
            slot
            for slot in self.requested_slots
            if not self.requested_slots[slot]
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Returns the information need as a dictionary."""
        return {
            "constraints": self.constraints,
            "requested_slots": self.get_requestable_slots(),
            "fulfilled_slots": {
                slot: value
                for slot, value in self.requested_slots.items()
                if value
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InformationNeed:
        """Creates an information need from a dictionary.

        Args:
            data: Information need data as a dictionary.

        Raises:
            KeyError: If the dictionary does not contain the required keys.

        Returns:
            Information need instance.
        """
        if not all(key in data for key in ["constraints", "requested_slots"]):
            raise KeyError(
                "The dictionary must contain constraints and requested_slots."
            )

        return cls(
            constraints=data.get("constraints", {}),
            requests=data.get("requested_slots", []),
        )
