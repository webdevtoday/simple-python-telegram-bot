import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

button_help = 'Help'


def log_error(f):

    async def inner(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e

    return inner


async def button_help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text='This is help!',
        reply_markup=ReplyKeyboardRemove(),
    )


@log_error
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == button_help:
        return await button_help_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help),
            ],
        ],
        resize_keyboard=True,
    )

    await update.message.reply_text(
        text='Hey, click the button below!',
        reply_markup=reply_markup,
    )


async def bot_get_me(app):
    print(await app.bot.get_me())


def main():
    print('Start')

    app = ApplicationBuilder().token('<TOKEN>').connect_timeout(0.5).build()

    asyncio.ensure_future(bot_get_me(app))

    app.add_handler(MessageHandler(
        filters=filters.ALL, callback=message_handler))

    app.run_polling()

    print('Finish')


if __name__ == '__main__':
    main()
