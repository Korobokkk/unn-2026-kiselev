"""Unit tests for the MessageTextHandler class."""

import unittest
from typing import Any

from .fake import Fake

from new_bot.handlers.handler import HandlerStatus
from new_bot.handlers.message_text import MessageTextHandler
from new_bot.messenger import Messenger


class MessageTextHandlerTest(unittest.TestCase):
    """Test case for the MessageTextHandler class."""

    def test_can_handle_message_with_text(self) -> None:
        """Test that can_handle returns True for an update containing a text message."""
        update = {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "chat": {"id": 227, "type": "private"},
                "text": "Hello world",
            },
        }

        self.assertTrue(MessageTextHandler().can_handle(update))

    def test_can_handle_rejects_update_without_text(self) -> None:
        """Test that can_handle returns False for an update without a text message."""
        update = {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "chat": {"id": 227, "type": "private"},
            },
        }

        self.assertFalse(MessageTextHandler().can_handle(update))

    def test_handle_echoes_text_and_stops(self) -> None:
        """Test that handle sends back the text message and returns HandlerStatus.STOP."""
        update = {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "chat": {"id": 227, "type": "private"},
                "text": "Hello world",
            },
        }
        sent = []

        def fake_send_message(**params: Any) -> None:
            """Fake send_message method that records sent messages."""
            sent.append(params)

        messenger: Messenger = Fake({"send_message": fake_send_message})

        status = MessageTextHandler().handle(update, messenger)

        self.assertEqual(status, HandlerStatus.STOP)
        self.assertEqual(sent, [{"chat_id": 227, "text": "Hello world"}])
