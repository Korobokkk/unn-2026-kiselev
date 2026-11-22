"""Messenger module."""

from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    """Abstract base class for messenger implementations."""

    @abstractmethod
    def get_updates(self, **params: object) -> list[dict[str, Any]]:
        """Get updates from messenger."""
        pass

    @abstractmethod
    def send_message(self, **params: object) -> dict[str, Any]:
        """Send message through messenger."""
        pass

    @abstractmethod
    def send_sticker(self, **params: object) -> dict[str, Any]:
        """Send sticker through messenger."""
        pass
