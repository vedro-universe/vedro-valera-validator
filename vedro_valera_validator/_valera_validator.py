from typing import Any, Union

from district42.types import Schema
from valera import ValidationException, validate_or_fail
from vedro.core import Dispatcher, Plugin
from vedro.events import (
    ExceptionRaisedEvent,
    ScenarioFailedEvent,
    ScenarioPassedEvent,
    ScenarioRunEvent,
)

__all__ = ("ValeraValidator",)


class ValeraValidator(Plugin):
    def __init__(self) -> None:
        self._eq: Any = None

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(ScenarioPassedEvent, self.on_scenario_end) \
                  .listen(ScenarioFailedEvent, self.on_scenario_end) \
                  .listen(ExceptionRaisedEvent, self.on_exception_raised)

    def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        self._eq = Schema.__eq__
        Schema.__override__("__eq__", validate_or_fail)

    def on_scenario_end(self, event: Union[ScenarioPassedEvent, ScenarioFailedEvent]) -> None:
        Schema.__override__("__eq__", self._eq)

    def on_exception_raised(self, event: ExceptionRaisedEvent) -> None:
        if event.exc_info.type is not ValidationException:
            return
        prev = event.exc_info.traceback
        tb = prev.tb_next
        while tb is not None:
            if tb.tb_next is None:
                prev.tb_next = None
            prev = tb
            tb = tb.tb_next
