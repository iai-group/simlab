"""Run configuration."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from simlab.participant.wrapper_agent import WrapperAgent
from simlab.participant.wrapper_user_simulator import WrapperUserSimulator
from simlab.tasks.task import Task


@dataclass
class RunConfiguration:
    """Run configuration with task and participants."""

    name: str
    task: Task
    agents: List[WrapperAgent]
    user_simulators: List[WrapperUserSimulator]
    kwargs: Dict[str, Any] = field(default_factory=dict)
