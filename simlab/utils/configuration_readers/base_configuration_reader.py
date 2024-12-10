"""Base class for configuration readers."""

import json
import os
from typing import List

from simlab.core.run_configuration import RunConfiguration
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
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
        task = self._parse_task()
        agents = self._parse_agents()
        user_simulators = self._parse_user_simulators()

        return RunConfiguration(task, agents, user_simulators)

    def _parse_task(self) -> Task:
        """Parses the task configuration.

        Returns:
            Task object.
        """
        task_class_name = self.configuration_dict.get("task", {}).get(
            "class_name", "Task"
        )

        # Parse metrics
        metrics = [
            self._component_generator.generate_component(
                "metric", metric.get("class_name"), metric
            )
            for metric in self.configuration_dict.get("metrics", [])
        ]

        # Include parsed metrics in the task configuration
        self.configuration_dict.get("task", {}).get("arguments", {}).update(
            {"metrics": metrics}
        )
        task = self._component_generator.generate_component(
            "task",
            task_class_name,
            self.configuration_dict.get("task"),
        )
        return task

    def _parse_agents(self) -> List[WrapperAgent]:
        """Parses the agents configuration.

        Returns:
            List of agents.
        """
        agents = []
        for agent in self.configuration_dict.get("agents", []):
            agent_class_name = agent.get("class_name", "WrapperAgent")
            agents.append(
                self._component_generator.generate_component(
                    "agent", agent_class_name, agent
                )
            )
        return agents

    def _parse_user_simulators(self) -> List[WrapperUserSimulator]:
        """Parses the user simulators configuration.

        Returns:
            List of user simulators.
        """
        user_simulators = []
        for user_simulator in self.configuration_dict.get(
            "user_simulators", []
        ):
            user_simulator_class_name = user_simulator.get(
                "class_name", "WrapperUserSimulator"
            )
            user_simulators.append(
                self._component_generator.generate_component(
                    "user_simulator", user_simulator_class_name, user_simulator
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
