"""Main module for the bot."""

import logging
import os

from new_bot.dispatcher import Dispatcher
from new_bot.handlers import get_handlers
from new_bot.long_polling import start_long_polling
from new_bot.telegram_messenger import TelegramMessenger

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot with long polling."""
    logging.basicConfig(level=logging.INFO)
    messenger = TelegramMessenger(
        token=os.environ["TELEGRAM_TOKEN"],
        base_url=os.environ["TELEGRAM_BASE_URL"],
    )
    dispathcer = Dispatcher(messenger)
    dispathcer.add_handlers(*get_handlers())
    try:
        start_long_polling(dispathcer, messenger)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")


if __name__ == "__main__":
    main()
