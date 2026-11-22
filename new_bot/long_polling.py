"""Long polling module."""

import logging
import time

from new_bot.dispatcher import Dispatcher
from new_bot.messenger import Messenger

RETRY_DELAY = 5

logger = logging.getLogger(__name__)


def poll_once(dispatcher: Dispatcher, messenger: Messenger, offset: int) -> int:
    """Poll for updates once and dispatch them."""
    updates = messenger.get_updates(
        offset=offset,
        limit=67,
        timeout=30,
        allowed_updates=["message"],
    )
    for update in updates:
        offset = max(offset, update["update_id"] + 1)
        dispatcher.dispatch(update)
    return offset


def start_long_polling(dispatcher: Dispatcher, messenger: Messenger) -> None:
    """Start long polling for updates and dispatch them."""
    offset = 0
    while True:
        try:
            offset = poll_once(dispatcher, messenger, offset)
        except Exception:
            logger.exception("Polling failed, retrying in %s s", RETRY_DELAY)
            time.sleep(RETRY_DELAY)
