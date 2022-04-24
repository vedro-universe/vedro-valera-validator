import sys
from traceback import format_exception
from types import TracebackType
from typing import Callable, List, cast
from unittest.mock import Mock, call, patch

import pytest
from baby_steps import given, then, when
from district42.types import Schema
from valera import ValidationException, validate_or_fail
from vedro.core import Dispatcher, ExcInfo, Plugin, ScenarioResult
from vedro.events import (
    ExceptionRaisedEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    ScenarioRunEvent,
)

from vedro_valera_validator import ValeraValidator, ValeraValidatorPlugin


@pytest.fixture()
def dispatcher() -> Dispatcher:
    return Dispatcher()


@pytest.fixture()
def validator(dispatcher: Dispatcher) -> ValeraValidatorPlugin:
    validator = ValeraValidatorPlugin(ValeraValidator)
    validator.subscribe(dispatcher)
    return validator


def raise_exception(exc_val: Exception) -> None:
    raise exc_val


def raise_nested_exception(exc_val: Exception) -> None:
    def nested():
        raise_exception(exc_val)
    nested()


def make_exc_info(exc_val: Exception, raise_: Callable = raise_exception) -> ExcInfo:
    try:
        raise_(exc_val)
    except type(exc_val):
        *_, traceback = sys.exc_info()
    return ExcInfo(type(exc_val), exc_val, cast(TracebackType, traceback))


def format_exc_info(exc_info: ExcInfo) -> List[str]:
    return format_exception(exc_info.type, exc_info.value, exc_info.traceback)


def patch_override():
    return patch("district42.types.Schema.__override__", Mock())


def test_valera_validator():
    with when:
        validator = ValeraValidatorPlugin(ValeraValidator)

    with then:
        assert isinstance(validator, Plugin)


@pytest.mark.asyncio
async def test_validator_scenario_run_event(*, dispatcher: Dispatcher,
                                            validator: ValeraValidatorPlugin):
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
@pytest.mark.parametrize("event_class", [ScenarioPassedEvent, ScenarioFailedEvent])
async def test_validator_scenario_end_event(event_class, *,
                                            dispatcher: Dispatcher,
                                            validator: ValeraValidatorPlugin):
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
async def test_validator_exception_raised_event(*, dispatcher: Dispatcher,
                                                validator: ValeraValidatorPlugin):
    with given:
        exc_info = make_exc_info(AssertionError())
        formatted = format_exc_info(exc_info)
        event = ExceptionRaisedEvent(exc_info)

    with when:
        await dispatcher.fire(event)

    with then:
        assert format_exc_info(exc_info) == formatted


@pytest.mark.asyncio
async def test_validator_exception_raised_validation_event(*, dispatcher: Dispatcher,
                                                           validator: ValeraValidatorPlugin):
    with given:
        exc_info = make_exc_info(ValidationException(), raise_nested_exception)
        formatted = format_exc_info(exc_info)
        event = ExceptionRaisedEvent(exc_info)

    with when:
        await dispatcher.fire(event)

    with then:
        assert format_exc_info(exc_info) == formatted[:4] + formatted[5:]
