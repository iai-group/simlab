"""Base class to generate components from configuration."""

import importlib
import inspect
import pkgutil
from typing import Any, Dict

_DEFAULT_MAP_TYPE_TO_MODULE_NAME = {
    "agent": "simlab.participant.wrapper_agent",
    "user_simulator": "simlab.participant.wrapper_user_simulator",
    "task": "simlab.tasks",
    "metric": "simlab.metrics",
    "domain": "simlab.core.simulation_domain",
    "information_need": "simlab.core.information_need",
    # DialogueKit components
    "nlu": "dialoguekit.nlu",
}


class BaseComponentGenerator:
    def __init__(
        self,
        map_type_to_module_name: Dict[
            str, str
        ] = _DEFAULT_MAP_TYPE_TO_MODULE_NAME,
    ) -> None:
        """Initializes a component generator.

        Args:
            map_type_to_module_name: Mapping of component types to module names.
              Defaults to _DEFAULT_MAP_TYPE_TO_MODULE_NAME.
        """
        self.map_type_to_module_name = map_type_to_module_name

    def get_available_classes(self, module_name: str) -> Dict[str, Any]:
        """Returns available classes from a module and its submodules.

        Caution: This method does not handle cyclic dependencies.

        Args:
            module_name: Module name.

        Returns:
            Dictionary of available classes.
        """
        available_classes: Dict[str, Any] = {}

        try:
            root_module = importlib.import_module(module_name)
            available_classes.update(self._inspect_module(module_name))

            if hasattr(root_module, "__path__"):
                for _, sub_module_name, _ in pkgutil.walk_packages(
                    root_module.__path__, f"{module_name}."
                ):
                    available_classes.update(
                        self._inspect_module(sub_module_name)
                    )
        except ModuleNotFoundError:
            raise ValueError(f"Module {module_name} not found.")
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while inspecting the module {module_name}:"
                f"\n{e}"
            )

        return available_classes

    def _inspect_module(self, module_name: str) -> Dict[str, Any]:
        """Inspects a module and extracts its classes.

        This method assumes that classes are not reused across modules.

        Args:
            module_name: Module name.

        Returns:
            Dictionary of classes in the module.
        """
        module = importlib.import_module(module_name)
        classes = {
            name: obj
            for name, obj in inspect.getmembers(module, inspect.isclass)
            if obj.__module__.startswith(module_name)
        }
        return classes

    def generate_component(
        self, type: str, class_name: str, component_config: Dict[str, Any]
    ) -> Any:
        """Generates a component from a configuration.

        It recursively generates components if the arguments contain components.

        Args:
            type: Component type.
            class_name: Component class name.
            component_config: Component configuration.

        Raises:
            ValueError: If the component name is not in the configuration.

        Returns:
            Component object.
        """
        # TODO: Optimize by caching the available classes per type
        component_class = self.get_available_classes(
            self.map_type_to_module_name[type]
        ).get(class_name, None)

        if not component_class:
            raise ValueError(f"Class {class_name} not found in {type}.")

        component_arguments = component_config.get("arguments", {})
        component_arguments = {
            key: (
                self.generate_component(
                    value.pop("type"), value.pop("class_name"), value
                )
                if isinstance(value, dict)
                else value
            )
            for key, value in component_arguments.items()
        }

        return component_class(**component_arguments)
