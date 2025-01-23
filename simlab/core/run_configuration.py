"""Run configuration."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Union

from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.tasks.task import Task


@dataclass
class ParticipantConfiguration:
    """Participant configuration with image name and custom parameters."""

    image_name: str
    participant: Union[WrapperAgent, WrapperUserSimulator]
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RunConfiguration:
    """Run configuration with task and participants."""

    name: str
    public: bool
    task: Task
    agent_configurations: List[ParticipantConfiguration]
    user_simulator_configurations: List[ParticipantConfiguration]
    kwargs: Dict[str, Any] = field(default_factory=dict)
