from unittest.mock import Mock, call

import pytest
from baby_steps import given, then, when
from district42.types import Schema
from valera import ValidationException, validate_or_fail

from vedro.core import Dispatcher, Plugin, ScenarioResult
from vedro.events import (
    ExceptionRaisedEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    ScenarioRunEvent,
)
from vedro_valera_validator import ValeraValidator, ValeraValidatorPlugin

from ._utils import (
    dispatcher,
    format_exc_info,
    make_exc_info,
    patch_override,
    raise_nested_exception,
    validator,
)

__all__ = ("dispatcher", "validator",)  # fixtures


def test_validator():
    with when:
        validator = ValeraValidatorPlugin(ValeraValidator)

    with then:
        assert isinstance(validator, Plugin)


@pytest.mark.asyncio
@pytest.mark.usefixtures(validator.__name__)
async def test_scenario_run_event(*, dispatcher: Dispatcher):
    with given:
        scenario_result = Mock(ScenarioResult)
        event = ScenarioRunEvent(scenario_result)

    with when, patch_override() as mock:
        await dispatcher.fire(event)

    with then:
        assert mock.mock_calls == [
            call("__eq__", validate_or_fail)
        ]


@pytest.mark.asyncio
@pytest.mark.usefixtures(validator.__name__)
@pytest.mark.parametrize("event_class", [ScenarioPassedEvent, ScenarioFailedEvent])
async def test_scenario_end_event(event_class, *, dispatcher: Dispatcher):
    with given:
        scenario_result = Mock(ScenarioResult)
        with patch_override():
            await dispatcher.fire(ScenarioRunEvent(scenario_result))
        event = event_class(scenario_result)

    with when, patch_override() as mock:
        await dispatcher.fire(event)

    with then:
        assert mock.mock_calls == [
            call("__eq__", Schema.__eq__)
        ]


@pytest.mark.asyncio
@pytest.mark.usefixtures(validator.__name__)
async def test_exception_raised_event(*, dispatcher: Dispatcher):
    with given:
        exc_info = make_exc_info(AssertionError())
        formatted = format_exc_info(exc_info)
        event = ExceptionRaisedEvent(exc_info)

    with when:
        await dispatcher.fire(event)

    with then:
        assert format_exc_info(exc_info) == formatted


@pytest.mark.asyncio
@pytest.mark.usefixtures(validator.__name__)
async def test_exception_raised_validation_event(*, dispatcher: Dispatcher):
    with given:
        exc_info = make_exc_info(ValidationException(), raise_nested_exception)
        formatted = format_exc_info(exc_info)
        event = ExceptionRaisedEvent(exc_info)

    with when:
        await dispatcher.fire(event)

    with then:
        assert format_exc_info(exc_info) == formatted[:4] + formatted[5:]
