"""Main module for telegram bot."""

import json
import logging
import os
from typing import Any
from urllib import error, parse, request

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

BASE_URL = os.environ["BASE_URL"]
TOKEN_TG_BOT = os.environ["TOKEN_TG_BOT"]


def request_telegram_bot_api(method: str, **params: Any) -> Any:
    """реквестаем по апи."""
    url = f"{BASE_URL}/bot{TOKEN_TG_BOT}/{method}"

    curr_request = request.Request(
        url,
        data=parse.urlencode(params).encode(),
        method="POST",
    )

    try:
        with request.urlopen(curr_request, timeout=15) as response:
            payload = json.loads(response.read())
    except error.HTTPError as error_message:
        logger.error("HTTP error: %s %s", error_message.code, error_message.reason)
        raise
    except error.URLError as error_message:
        logger.error("Network error: %s", error_message.reason)
        raise

    if not payload["ok"]:
        description = payload["description"]
        logger.error("Telegram API error: %s", description)
        raise RuntimeError(f"Telegram API error: {description}")

    return payload["result"]


def main() -> None:
    """Bot main loop."""
    logger.info("WORK WORK WORK\nJOB JOB JOB")

    offset = 0

    while True:
        updates = request_telegram_bot_api(
            "getUpdates",
            offset=offset,
            timeout=30,
            allowed_updates=json.dumps(["message"]),
        )

        for update in updates:
            offset = max(offset, update["update_id"] + 1)

            message = update["message"]

            if "text" in message:
                request_telegram_bot_api(
                    "sendMessage",
                    chat_id=message["chat"]["id"],
                    text=message["text"],
                )
                logger.info("Received text message: %s", message["text"])
            elif "sticker" in message:
                logger.info("Received sticker message: %s", message)
                request_telegram_bot_api(
                    "sendSticker",
                    chat_id=message["chat"]["id"],
                    sticker="CAACAgIAAxkBAAM8atTFFVQZkbjLS_m62zr9rHTZxo8AAiJ1AALfQMBL0QZ6oNQWpUc9BA",
                )
            else:
                logger.info("Received unsupported message type: %s", message)
                continue
