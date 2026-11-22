"""Unit tests for the long polling mechanism of the bot."""

import unittest
from typing import Any

from .fake import Fake

from new_bot.dispatcher import Dispatcher
from new_bot.long_polling import poll_once
from new_bot.messenger import Messenger


class PollOnceTest(unittest.TestCase):
    """Test case for the poll_once function to ensure correct polling and dispatching of updates."""

    def test_single_update_dispatches_and_advances_offset(self) -> None:
        """Test that a single update is dispatched and the offset is advanced correctly."""
        update = {
            "update_id": 227,
            "message": {
                "message_id": 1,
                "chat": {"id": 1, "type": "private"},
                "text": "Hello world",
            },
        }
        requested = []
        dispatched = []

        def fake_get_updates(**params: Any) -> list[dict[str, Any]]:
            """Fake get_updates method that records the request parameters and returns a single update."""
            requested.append(params)
            return [update]

        messenger: Messenger = Fake({"get_updates": fake_get_updates})
        dispatcher: Dispatcher = Fake({"dispatch": dispatched.append})

        next_offset = poll_once(dispatcher, messenger, offset=0)

        self.assertEqual(
            requested,
            [{"offset": 0, "limit": 67, "timeout": 30, "allowed_updates": ["message"]}],
        )
        self.assertEqual(dispatched, [update])
        self.assertEqual(next_offset, 228)

    def test_empty_updates_does_not_dispatch(self) -> None:
        """Test that when no updates are returned, nothing is dispatched and the offset remains unchanged."""
        dispatched = []
        messenger: Messenger = Fake({"get_updates": lambda **_: []})
        dispatcher: Dispatcher = Fake({"dispatch": dispatched.append})

        next_offset = poll_once(dispatcher, messenger, offset=0)

        self.assertEqual(dispatched, [])
        self.assertEqual(next_offset, 0)

    def test_unordered_update_ids_uses_max_offset(self) -> None:
        """Test that when updates are returned with unordered update_ids, the offset is set to the maximum update_id + 1."""  # noqa: E501
        update_high = {"update_id": 100, "message": {"text": "first"}}
        update_low = {"update_id": 50, "message": {"text": "second"}}
        dispatched = []
        messenger: Messenger = Fake({"get_updates": lambda **_: [update_high, update_low]})
        dispatcher: Dispatcher = Fake({"dispatch": dispatched.append})

        next_offset = poll_once(dispatcher, messenger, offset=0)

        self.assertEqual(dispatched, [update_high, update_low])
        self.assertEqual(next_offset, 101)
