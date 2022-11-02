import asyncio

from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters


def log_errors(f):

    async def inner(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            print(f'[error]: {e}')
            raise e

    return inner


@log_errors
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonymous'

    text = update.effective_message.text
    reply_text = f'Hi, {name}!\n\n{text}'

    await update.message.reply_text(
        text=reply_text
    )


async def bot_get_me(app):
    print(await app.bot.get_me())


def main():
    print('Start')

    app = ApplicationBuilder().token('').connect_timeout(0.5).read_timeout(1.0).build()

    # Check that the bot has correctly connected to the Telegram API
    asyncio.ensure_future(bot_get_me(app))

    # Attach command handlers
    app.add_handler(MessageHandler(filters.ALL, message_handler))

    app.run_polling()
    print('Finish')


if __name__ == '__main__':
    main()
