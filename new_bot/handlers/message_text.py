"""Message text handler module."""

from typing import Any

from new_bot.handlers.handler import Handler, HandlerStatus
from new_bot.messenger import Messenger


class MessageTextHandler(Handler):
    """Handler for text messages."""

    def can_handle(self, update: dict[str, Any]) -> bool:
        """Check if the update is a text message."""
        message = update.get("message")
        return isinstance(message, dict) and "text" in message

    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        """Handle the text message by sending it back to the user."""
        message = update["message"]
        messenger.send_message(
            chat_id=message["chat"]["id"],
            text=message["text"],
        )
        return HandlerStatus.STOP
