import asyncio
from telegram import Bot


from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))


from echo.config import load_config
from apis.nbu import get_rates


NOTIFY_USER_ID = ""


async def main():
    item = get_rates()
    message = f"Exchange Rate {item.name} = {item.rate} UAH"
    config = load_config()

    bot = Bot(config.TG_TOKEN)
    await bot.send_message(
        chat_id=NOTIFY_USER_ID,
        text=message
    )


if __name__ == '__main__':
    asyncio.run(main())
