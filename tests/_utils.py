import sys
from traceback import format_exception
from types import TracebackType
from typing import Callable, List, cast
from unittest.mock import Mock, patch

import pytest
from vedro.core import Dispatcher, ExcInfo

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
    try:
        from d42.declaration import Schema  # noqa
        return patch("d42.declaration.Schema.__override__", Mock())
    except ImportError:
        return patch("district42.types.Schema.__override__", Mock())
