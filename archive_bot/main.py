from logging import getLogger

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler

from archive_bot.db import init_db, add_message, count_messages, list_messages
from echo.config import load_config
from echo.utils import debug_requests

config = load_config()

logger = getLogger(__name__)


COMMAND_COUNT = 'count'
COMMAND_LIST = 'list'


def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Number of messages", callback_data=COMMAND_COUNT),
            ],
            [
                InlineKeyboardButton(text='My messages',
                                     callback_data=COMMAND_LIST),
            ],
        ],
    )


@debug_requests
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonimous'

    text = update.effective_message.text
    reply_text = f'Hi, {name}!\n\n{text}'

    # Reply to user
    await update.message.reply_text(
        text=reply_text,
        reply_markup=get_keyboard(),
    )

    # Write message to database
    if text:
        add_message(
            user_id=user.id,
            text=text,
        )


@debug_requests
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    callback_data = update.callback_query.data

    if callback_data == COMMAND_COUNT:
        count = count_messages(user_id=user.id)
        text = f'You have {count} messages!'
    elif callback_data == COMMAND_LIST:
        messages = list_messages(user_id=user.id, limit=5)
        text = '\n\n'.join(
            [f'#{message_id} - {message_text}' for message_id, message_text in messages])
    else:
        text = 'An error has occurred'

    await update.effective_message.reply_text(
        text=text,
    )


def main():
    logger.info('Start ArchiveBot')

    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    # Connect to DBMS
    init_db()

    # Attach command handlers
    application.add_handler(MessageHandler(filters.ALL, message_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))

    # Start infinite processing of incoming messages
    application.run_polling()
    logger.info('Stop ArchiveBot')


if __name__ == '__main__':
    main()
