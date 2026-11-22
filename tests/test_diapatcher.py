"""Unit tests for the dispatcher module."""

import unittest
from typing import Any

from .fake import Fake

from new_bot.dispatcher import Dispatcher
from new_bot.handlers.message_sticker import MessageStickerHandler
from new_bot.handlers.message_text import MessageTextHandler
from new_bot.messenger import Messenger


class DispatcherRoutingTest(unittest.TestCase):
    """Test case for the Dispatcher class to ensure correct routing of updates to handlers."""

    def setUp(self) -> None:
        """Set up the test case with a fake messenger and a dispatcher with handlers."""
        self.sent_messages: list[dict[str, Any]] = []
        self.sent_stickers: list[dict[str, Any]] = []

        def fake_send_message(**params: Any) -> None:
            """Fake send_message method that records sent messages."""
            self.sent_messages.append(params)

        def fake_send_sticker(**params: Any) -> None:
            """Fake send_sticker method that records sent stickers."""
            self.sent_stickers.append(params)

        messenger: Messenger = Fake({"send_message": fake_send_message, "send_sticker": fake_send_sticker})
        self.dispatcher = Dispatcher(messenger)
        self.dispatcher.add_handlers(MessageTextHandler(), MessageStickerHandler())

    def test_text_goes_to_text_handler(self) -> None:
        """Test that a text message update is routed to the text handler."""
        update = {"update_id": 1, "message": {"chat": {"id": 227}, "text": "Hello world!!!"}}

        self.dispatcher.dispatch(update)

        self.assertEqual(self.sent_messages, [{"chat_id": 227, "text": "Hello world!!!"}])
        self.assertEqual(self.sent_stickers, [])

    def test_sticker_goes_to_sticker_handler(self) -> None:
        """Test that a sticker message update is routed to the sticker handler."""
        update = {
            "update_id": 1,
            "message": {"chat": {"id": 227}, "sticker": {"file_id": "sticker-file-id"}},
        }

        self.dispatcher.dispatch(update)

        self.assertEqual(self.sent_messages, [])
        self.assertEqual(self.sent_stickers, [{"chat_id": 227, "sticker": "sticker-file-id"}])

    def test_unsupported_update_is_ignored(self) -> None:
        """Test that an unsupported update is ignored and does not trigger any handlers."""
        update = {"update_id": 1, "message": {"chat": {"id": 227}, "voice_message": []}}

        self.dispatcher.dispatch(update)

        self.assertEqual(self.sent_messages, [])
        self.assertEqual(self.sent_stickers, [])
