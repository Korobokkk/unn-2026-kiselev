"""Handlers module."""

from new_bot.handlers.handler import Handler
from new_bot.handlers.message_sticker import MessageStickerHandler
from new_bot.handlers.message_text import MessageTextHandler


def get_handlers() -> list[Handler]:
    """Get the list of handlers."""
    return [
        MessageTextHandler(),
        MessageStickerHandler(),
    ]
