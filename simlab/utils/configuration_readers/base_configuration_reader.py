"""Base class for configuration readers."""

import json
import os
from copy import deepcopy
from typing import Any, Dict, List

from simlab.core.run_configuration import (
    ParticipantConfiguration,
    RunConfiguration,
)
from simlab.tasks.task import Task
from simlab.utils.configuration_readers.component_generators.base_component_generator import (  # noqa: E501
    BaseComponentGenerator,
)


class BaseConfigurationReader:
    def __init__(self, configuration_path: str = None) -> None:
        """Initializes a configuration reader.

        Args:
            configuration_path: Path to the configuration file. Defaults to
              None.
        """
        self.configuration_dict: Dict[str, Any] = dict()
        self._component_generator: BaseComponentGenerator = None

        if configuration_path:
            self.load_configuration_dict(configuration_path)
            self.configuration = self.configuration_parser()
        else:
            self.configuration = None

    def load_configuration_dict(self, configuration_path: str) -> None:
        """Loads the configuration dictionary from a file.

        Args:
            configuration_path: Path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            RuntimeError: If the configuration file is not a JSON file.
        """
        if not os.path.exists(configuration_path):
            raise FileNotFoundError(
                f"Configuration file {configuration_path} does not exist."
            )

        if not configuration_path.endswith(".json"):
            raise RuntimeError("Configuration file must be a JSON file.")

        self.configuration_dict = json.load(open(configuration_path, "r"))
        self._component_generator = self._get_component_generator()

    def configuration_parser(
        self, configuration_path: str = None
    ) -> RunConfiguration:
        """Parses the configuration dictionary.

        Args:
            configuration_path: Path to the configuration file. Defaults to
              None.

        Raises:
            ValueError: If the configuration dictionary is invalid.

        Returns:
            RunConfiguration object.
        """
        if configuration_path:
            self.load_configuration_dict(configuration_path)

        if "name" not in self.configuration_dict:
            raise ValueError("Configuration must have a name.")
        name = self.configuration_dict.pop("name")
        public = self.configuration_dict.pop("public", False)
        task = self._parse_task()
        agent_configurations = self._parse_agent_configurations()
        user_simulator_configurations = (
            self._parse_user_simulator_configurations()
        )

        self.configuration = RunConfiguration(
            name,
            public,
            task,
            agent_configurations,
            user_simulator_configurations,
        )
        return self.configuration

    def _parse_task(self) -> Task:
        """Parses the task configuration.

        Returns:
            Task object.
        """
        task_config_dict = deepcopy(self.configuration_dict.get("task", {}))
        task_class_name = task_config_dict.get("class_name", "Task")

        # Parse metrics
        metrics = [
            self._component_generator.generate_component(
                "metric", metric.get("class_name"), metric
            )
            for metric in task_config_dict.get("arguments", {}).get(
                "metrics", []
            )
        ]

        # Include parsed metrics in the task configuration
        task_config_dict.get("arguments", {})["metrics"] = metrics

        task = self._component_generator.generate_component(
            "task",
            task_class_name,
            task_config_dict,
        )
        return task

    def _parse_agent_configurations(
        self,
    ) -> List[ParticipantConfiguration]:
        """Parses the agents configuration.

        Returns:
            List of agents with their associated image and custom parameters.
        """
        agents = []
        for agent_config_dict in self.configuration_dict.get("agents", []):
            agent_class_name = agent_config_dict.get(
                "class_name", "WrapperAgent"
            )
            agent = self._component_generator.generate_component(
                "agent",
                agent_class_name,
                agent_config_dict,
            )

            agent_image_name = agent_config_dict.get("image", None)
            agent_custom_parameters = agent_config_dict.get("parameters", {})
            agents.append(
                ParticipantConfiguration(
                    agent_image_name, agent, agent_custom_parameters
                )
            )
        return agents

    def _parse_user_simulator_configurations(
        self,
    ) -> List[ParticipantConfiguration]:
        """Parses the user simulators configuration.

        Returns:
            List of user simulators with their associated image and custom
              parameters.
        """
        user_simulators = []
        for user_simulator_config in self.configuration_dict.get(
            "user_simulators", []
        ):
            user_simulator_class_name = user_simulator_config.get(
                "class_name", "WrapperUserSimulator"
            )
            user_simulator = self._component_generator.generate_component(
                "user_simulator",
                user_simulator_class_name,
                user_simulator_config,
            )

            user_simulator_image_name = user_simulator_config.get("image", None)
            user_simulator_custom_parameters = user_simulator_config.get(
                "parameters", {}
            )
            user_simulators.append(
                ParticipantConfiguration(
                    user_simulator_image_name,
                    user_simulator,
                    user_simulator_custom_parameters,
                )
            )
        return user_simulators

    def _get_component_generator(self) -> BaseComponentGenerator:
        """Returns a component generator."""
        if self.configuration_dict.get("map_type_to_module_name"):
            return BaseComponentGenerator(
                self.configuration_dict["map_type_to_module_name"]
            )
        return BaseComponentGenerator()
