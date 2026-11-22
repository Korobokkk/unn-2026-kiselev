"""Handler module."""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any

from new_bot.messenger import Messenger


class HandlerStatus(Enum):
    """Enum for handler status."""

    CONTINUE = auto()
    STOP = auto()


class Handler(ABC):
    """Abstract base class for handlers."""

    @abstractmethod
    def can_handle(self, update: dict[str, Any]) -> bool:
        """Check if the handler can handle the update."""
        pass

    @abstractmethod
    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        """Handle the update."""
        pass
