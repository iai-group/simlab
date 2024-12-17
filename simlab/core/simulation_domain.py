"""Simulation domain knowledge.

This domain knowledge allows the definition of requestable and
informable slots. If not specified, all the slots are considered
requestable and informable.
"""

# Taken from UserSimCRS

import logging
from collections import defaultdict
from typing import Dict, List

from dialoguekit.core.domain import Domain
from simlab.core.item_collection import ItemCollection


class SimulationDomain(Domain):
    def __init__(self, config_file: str) -> None:
        """Initializes the domain knowledge.

        Args:
            config_file: Path to the domain configuration file.
        """
        super().__init__(config_file)

    def get_requestable_slots(self) -> List[str]:
        """Returns the list of requestable slots."""
        if "requestable_slots" not in self._config:
            return self.get_slot_names()
        return self._config["requestable_slots"]

    def get_informable_slots(self) -> List[str]:
        """Returns the list of informable slots."""
        if "informable_slots" not in self._config:
            return self.get_slot_names()
        return self._config["informable_slots"]

    def get_item_collections(self) -> Dict[str, ItemCollection]:
        """Returns the list of item collections associated with the domain.

        Raises:
            KeyError: If the configuration does not have the field
              item_collections.

        Returns:
            List of item collections.
        """
        if "item_collections" not in self._config:
            raise KeyError(
                "The domain configuration should contain the field "
                "'item_collections'."
            )
        item_collections = defaultdict(ItemCollection)
        for collection in self._config["item_collections"]:
            try:
                name = collection.get("collection_name")
                item_collections[name] = ItemCollection(**collection)
            except RuntimeError as e:
                logging.error(
                    "Could not create item collection with configuration: "
                    f"{collection}\n{e}"
                )
        return dict(item_collections)
