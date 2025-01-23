"""Base class for configuration readers."""

import json
import os
from typing import List

from simlab.core.run_configuration import (
    ParticipantConfiguration,
    RunConfiguration,
)
from simlab.tasks.task import Task
from simlab.utils.configuration_readers.component_generators.base_component_generator import (  # noqa: E501
    BaseComponentGenerator,
)


class BaseConfigurationReader:
    def __init__(self, configuration_path: str) -> None:
        """Initializes a configuration reader.

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

        self.configuration_path = configuration_path
        self.configuration_dict = json.load(open(configuration_path, "r"))
        self._component_generator = self._get_component_generator()

    @property
    def configuration(self) -> RunConfiguration:
        """Returns the configuration object.

        Returns:
            Run configuration object.
        """
        return self._configuration_parser()

    def _configuration_parser(self) -> RunConfiguration:
        """Parses the configuration file.

        Raises:
            ValueError: If the configuration file is invalid.

        Returns:
            RunConfiguration object.
        """
        if "name" not in self.configuration_dict:
            raise ValueError("Configuration file must have a name.")
        name = self.configuration_dict.pop("name")
        public = self.configuration_dict.pop("public", False)
        task = self._parse_task()
        agent_configurations = self._parse_agent_configurations()
        user_simulator_configurations = (
            self._parse_user_simulator_configurations()
        )

        return RunConfiguration(
            name,
            public,
            task,
            agent_configurations,
            user_simulator_configurations,
        )

    def _parse_task(self) -> Task:
        """Parses the task configuration.

        Returns:
            Task object.
        """
        task_config_dict = self.configuration_dict.get("task", {})
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
        task_config_dict.get("arguments", {}).update({"metrics": metrics})

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

            agent_image_name = agent_config_dict.get("image_name", None)
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

            user_simulator_image_name = user_simulator_config.get(
                "image_name", None
            )
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
