from logging import getLogger

import asyncio
from telegram import Bot

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from echo.config import load_config
from apis.coinmarketcap import CoinMarketCapClient, CoinMarketCapError


logger = getLogger(__name__)


NOTIFY_PAIR = ("BTC", "USD")
NOTIFY_USER_ID = ""

COIN_MARKET_CAP_API_KEY = ""


async def main():
    client = CoinMarketCapClient(COIN_MARKET_CAP_API_KEY)

    try:
        current_price = client.get_last_price(pair=NOTIFY_PAIR)
        message = "{} = {}".format(NOTIFY_PAIR, current_price)
    except CoinMarketCapError:
        logger.error("CoinMarketCapError")
        message = "An error has occurred"

    config = load_config()

    bot = Bot(config.TG_TOKEN)
    await bot.send_message(
        chat_id=NOTIFY_USER_ID,
        text=message
    )


if __name__ == '__main__':
    asyncio.run(main())
