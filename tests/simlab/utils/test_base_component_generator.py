"""Tests for base component generator."""

from typing import Any, Dict

import pytest

from simlab.metrics.metric import Metric
from simlab.metrics.task_performance.success_rate import SuccessRate
from simlab.participant.wrapper_agent import WrapperAgent
from simlab.utils.configuration_readers.component_generators.base_component_generator import (  # noqa: E501
    BaseComponentGenerator,
)


@pytest.fixture
def base_component_generator() -> BaseComponentGenerator:
    """Returns a base component generator."""
    return BaseComponentGenerator()


def test_base_component_generator_custom_type_mapping() -> None:
    """Tests base component generator custom type to module mapping."""
    component_generator = BaseComponentGenerator(
        map_type_to_module_name={"type1": "simlab.type1"}
    )

    assert component_generator.map_type_to_module_name == {
        "type1": "simlab.type1"
    }


@pytest.mark.parametrize(
    "module_name, expected",
    [
        ("simlab.participant.wrapper_agent", {"WrapperAgent": WrapperAgent}),
        ("simlab.metrics", {"Metric": Metric, "SuccessRate": SuccessRate}),
    ],
)
def test_get_available_classes(
    base_component_generator: BaseComponentGenerator,
    module_name: str,
    expected: Dict[str, Any],
) -> None:
    """Tests retrieval of available classes from a module.

    Args:
        base_component_generator: Base component generator.
        module_name: Module name.
        expected: Expected available classes.
    """
    available_classes = base_component_generator.get_available_classes(
        module_name
    )

    assert available_classes == expected


def test_get_available_classes_module_not_found(
    base_component_generator: BaseComponentGenerator,
) -> None:
    """Tests get available classes with module not found."""
    with pytest.raises(ValueError):
        base_component_generator.get_available_classes("non_existent_module")


def test_generate_component_invalid_class_name(
    base_component_generator: BaseComponentGenerator,
) -> None:
    """Tests generate component with invalid class name."""
    with pytest.raises(ValueError):
        base_component_generator.generate_component(
            "metric", "InvalidMetric", {"name": "Invalid Metric"}
        )
