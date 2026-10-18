import json
import os
from urllib import parse, request, error
import logging

logging.basicConfig(level=logging.INFO)

BASE_URL = os.environ["BASE_URL"]
TOKEN_TG_BOT=os.environ["TOKEN_TG_BOT"]


def request_telegram_bot_api(method, **params):
    """реквестаем по апи"""
    url = f"{BASE_URL}/bot{TOKEN_TG_BOT}/{method}"

    curr_request = request.Request(
        url,
        data= parse.urlencode(params).encode(),
        method="POST",
    )

    try:
        with request.urlopen(curr_request, timeout=40) as response:
            payload = json.loads(response.read())
    except error.HTTPError as error_message:
        logging.error(f"HTTP error: {error_message.code} {error_message.reason}")
        raise
    except error.URLError as error_message:
        logging.error(f"Network error: {error_message.reason}")
        raise

    if not payload["ok"]:
        raise RuntimeError(f"Telegram API error: {payload['description']}")
    
    return payload["result"]


def main():
    logging.info("WORK WORK WORK\nJOB JOB JOB")

    offset=0

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
                logging.info(f"Received text message: {message['text']}")
            elif "sticker" in message:
                logging.info(f"Received sticker message: {message}")
                request_telegram_bot_api(
                    "sendSticker",
                    chat_id=message["chat"]["id"],
                    sticker="CAACAgIAAxkBAAM8atTFFVQZkbjLS_m62zr9rHTZxo8AAiJ1AALfQMBL0QZ6oNQWpUc9BA"
                )
            else:
                logging.info(f"Received unsupported message type: {message}")
                continue

if __name__== "__main__":
    main()