"""Dispatcher module."""

from typing import Any

from new_bot.handlers.handler import Handler, HandlerStatus
from new_bot.messenger import Messenger


class Dispatcher:
    """Dispatcher class to manage and dispatch updates to handlers."""

    def __init__(self, messenger: Messenger) -> None:
        """Initialize the dispatcher with a messenger and an empty list of handlers."""
        self._messenger = messenger
        self._handlers: list[Handler] = []

    def add_handlers(self, *handlers: Handler) -> None:
        """Add handlers to the dispatcher."""
        self._handlers.extend(handlers)

    def dispatch(self, update: dict[str, Any]) -> None:
        """Dispatch the update to the appropriate handler."""
        for handler in self._handlers:
            if not handler.can_handle(update):
                continue
            if handler.handle(update, self._messenger) == HandlerStatus.STOP:
                break
