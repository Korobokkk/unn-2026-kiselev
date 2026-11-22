"""Unit tests for the Dispatcher class and its chain of handlers."""

import unittest
from typing import Any, override

from .fake import Fake

from new_bot.dispatcher import Dispatcher
from new_bot.handlers.handler import Handler, HandlerStatus
from new_bot.messenger import Messenger


class RecordingHandler(Handler):
    """A handler that records calls to can_handle and handle methods for testing purposes."""

    def __init__(self, name: str, can_handle: bool, status: HandlerStatus, calls: list[str]) -> None:
        """Initialize the recording handler with a name, can_handle value, status, and a list to record calls."""  # noqa: E501
        self._name = name
        self._can_handle = can_handle
        self._status = status
        self._calls = calls

    @override
    def can_handle(self, update: dict[str, Any]) -> bool:
        """Record the call and return the predefined can_handle value."""
        return self._can_handle

    @override
    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        """Record the call and return the predefined status."""
        self._calls.append(self._name)
        return self._status


class DispatcherChainTest(unittest.TestCase):
    """Test case for the Dispatcher class with a chain of handlers."""

    def dispatch(self, first: RecordingHandler, second: RecordingHandler) -> None:
        """Helper method to dispatch an update through the dispatcher with two handlers."""
        dispatcher = Dispatcher(Fake({}))
        dispatcher.add_handlers(first, second)
        dispatcher.dispatch({"update_id": 1})

    def test_stop_breaks_chain(self) -> None:
        """Test that if the first handler stops, the second handler is not called."""
        calls: list[str] = []
        self.dispatch(
            RecordingHandler(
                name="first",
                can_handle=True,
                status=HandlerStatus.STOP,
                calls=calls,
            ),
            RecordingHandler(
                name="second",
                can_handle=True,
                status=HandlerStatus.STOP,
                calls=calls,
            ),
        )

        self.assertEqual(calls, ["first"])

    def test_continue_passes_to_next_handler(self) -> None:
        """Test that if the first handler returns CONTINUE, the second handler is called."""
        calls: list[str] = []
        self.dispatch(
            RecordingHandler(
                name="first",
                can_handle=True,
                status=HandlerStatus.CONTINUE,
                calls=calls,
            ),
            RecordingHandler(
                name="second",
                can_handle=True,
                status=HandlerStatus.STOP,
                calls=calls,
            ),
        )

        self.assertEqual(calls, ["first", "second"])

    def test_handler_that_cannot_handle_is_skipped(self) -> None:
        """Test that a handler that cannot handle the update is skipped and the next handler is called."""
        calls: list[str] = []
        self.dispatch(
            RecordingHandler(
                name="first",
                can_handle=False,
                status=HandlerStatus.STOP,
                calls=calls,
            ),
            RecordingHandler(
                name="second",
                can_handle=True,
                status=HandlerStatus.STOP,
                calls=calls,
            ),
        )

        self.assertEqual(calls, ["second"])
