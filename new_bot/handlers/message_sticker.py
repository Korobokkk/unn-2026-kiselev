"""Message sticker handler module."""

from typing import Any

from new_bot.handlers.handler import Handler, HandlerStatus
from new_bot.messenger import Messenger


class MessageStickerHandler(Handler):
    """Handler for sticker messages."""

    def can_handle(self, update: dict[str, Any]) -> bool:
        """Check if the update is a sticker message."""
        message = update.get("message")
        return isinstance(message, dict) and "sticker" in message

    def handle(self, update: dict[str, Any], messenger: Messenger) -> HandlerStatus:
        """Handle the sticker message by sending it back to the user."""
        message = update["message"]
        messenger.send_sticker(
            chat_id=message["chat"]["id"],
            sticker=message["sticker"]["file_id"],
        )
        return HandlerStatus.STOP
