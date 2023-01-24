import asyncio

from logging import getLogger

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from echo.config import load_config
from echo.utils import logger_factory


config = load_config()

logger = getLogger(__name__)

debug_requests = logger_factory(logger=logger)


@debug_requests
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonymous'

    text = update.effective_message.text
    reply_text = f'Hi, {name}!\n\n{text}'

    context.xxxx

    await update.message.reply_text(
        text=reply_text,
    )


async def bot_get_me(app):
    info = await app.bot.get_me()
    logger.info(f'Bot info: {info}')


def main():
    logger.info('Start')

    app = ApplicationBuilder().token(config.TG_TOKEN).connect_timeout(0.5).build()

    asyncio.ensure_future(bot_get_me(app))

    app.add_handler(MessageHandler(
        filters=filters.ALL, callback=message_handler))

    app.run_polling()

    logger.info('Finish')


if __name__ == '__main__':
    main()
