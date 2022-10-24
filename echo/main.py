import datetime
from logging import getLogger
from subprocess import Popen, PIPE

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler

from config import load_config
from apis.coinmarketcap import CoinMarketCapClient, CoinMarketCapError
from echo.buttons import BUTTON1_HELP, BUTTON2_TIME, get_base_reply_keyboard

config = load_config()

logger = getLogger(__name__)


def debug_requests(f):
    """ Decorator for debugging telegram events
    """
    def inner(*args, **kwargs):
        try:
            logger.info("Calling a function {}".format(f.__name__))
            return f(*args, **kwargs)
        except Exception:
            logger.exception("Error in handler {}".format(f.__name__))
            raise

    return inner


# `callback_data` -- is what TG will send when each button is clicked.
# So each id must be unique
CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"
CALLBACK_BUTTON3_MORE = "callback_button3_more"
CALLBACK_BUTTON4_BACK = "callback_button4_back"
CALLBACK_BUTTON5_TIME = "callback_button5_time"
CALLBACK_BUTTON6_PRICE = "callback_button6_price"
CALLBACK_BUTTON7_PRICE = "callback_button7_price"
CALLBACK_BUTTON8_PRICE = "callback_button8_price"
CALLBACK_BUTTON_HIDE_KEYBOARD = "callback_button9_hide"


TITLES = {
    CALLBACK_BUTTON1_LEFT: "A new message ⚡",
    CALLBACK_BUTTON2_RIGHT: "Edit ✏️",
    CALLBACK_BUTTON3_MORE: "More ➡️",
    CALLBACK_BUTTON4_BACK: "Back ⬅️",
    CALLBACK_BUTTON5_TIME: "Time ⏰",
    CALLBACK_BUTTON6_PRICE: "BTC 💰",
    CALLBACK_BUTTON7_PRICE: "LTC 💰",
    CALLBACK_BUTTON8_PRICE: "ETH 💰",
    CALLBACK_BUTTON_HIDE_KEYBOARD: "Hide keyboard",
}

client = CoinMarketCapClient(config.COIN_MARKET_CAP_API_KEY)


def get_base_inline_keyboard():
    """ Get a keyboard for a message
        This keyboard will be visible under every post where it has been pinned
    """
    # Each list inside `keyboard` -- is one horizontal row of buttons
    keyboard = [
        # Each element inside the list -- is one vertical column.
        # How many buttons -- how many columns
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
        ],
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON_HIDE_KEYBOARD),
        ],
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_keyboard2():
    """ Get second page of keyboard for messages
        Can only be obtained by pressing a button on the first keyboard
    """
    keyboard = [
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
        ],
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
        ],
        [
            InlineKeyboardButton(
                TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


@debug_requests
async def do_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! Send me something",
        reply_markup=get_base_reply_keyboard(),
    )


@debug_requests
async def do_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This is a tutorial bot\n\n"
        "The list of available commands is in the menu\n\n"
        "I also reply to any message",
        reply_markup=get_base_inline_keyboard(),
    )


@debug_requests
async def keyboard_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Handler for ALL buttons from ALL keyboards
    """
    query = update.callback_query

    await query.answer()

    data = query.data
    now = datetime.datetime.now()

    # Note that `effective_message` is used
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON1_LEFT:
        # "Delete" the keyboard from the previous message
        # (actually edit it so that the text stays the same and the keyboard disappears)
        await query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        # Send a new message on button click
        await context.bot.send_message(
            chat_id=chat_id,
            text="A new message\n\ncallback_query.data={}".format(data),
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON2_RIGHT:
        # Let's edit the text of the message, but leave the keyboard
        await query.edit_message_text(
            text="Successfully edited in {}".format(now),
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON3_MORE:
        # Show next keyboard screen
        # (keep the same text but specify a different array of buttons)
        await query.edit_message_text(
            text=current_text,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        # Show previous keyboard screen
        # (keep the same text but specify a different array of buttons)
        await query.edit_message_text(
            text=current_text,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_TIME:
        # Show new text and keep the same keyboard
        text = "*Exact time*\n\n{}".format(now)
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE, CALLBACK_BUTTON8_PRICE):
        pair = {
            CALLBACK_BUTTON6_PRICE: ("BTC", "USD"),
            CALLBACK_BUTTON7_PRICE: ("LTC", "USD"),
            CALLBACK_BUTTON8_PRICE: ("ETH", "USD"),
        }[data]

        try:
            current_price = client.get_last_price(pair=pair)
            text = "*Rate:*\n\n*{}* = ${}".format(pair, current_price)
        except CoinMarketCapError:
            text = "An error has occurred :(\n\nTry again"
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON_HIDE_KEYBOARD:
        # Hide keyboard
        # Only works when sending a new message
        # It could be edited, but then you need to know for sure that the message had no buttons
        await context.bot.send_message(
            chat_id=chat_id,
            text="Hidden the keyboard\n\nPress /start to bring it back",
            reply_markup=ReplyKeyboardRemove(),
        )


@debug_requests
async def do_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Check server time
    """
    process = Popen(["date"], stdout=PIPE)
    text, error = process.communicate()
    # Process invocation error may occur (return code not 0)
    if error:
        text = "An error occurred, time unknown"
    else:
        # Decode command response from process
        text = text.decode("utf-8")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=get_base_inline_keyboard(),
    )


@debug_requests
async def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    if text == BUTTON1_HELP:
        return await do_help(update=update, context=context)
    elif text == BUTTON2_TIME:
        return await do_time(update=update, context=context)
    else:
        reply_text = "Your ID = {}\n\n{}".format(chat_id, text)
        await context.bot.send_message(
            chat_id=chat_id,
            text=reply_text,
            reply_markup=get_base_inline_keyboard(),
        )


def main():
    logger.info("Launching the bot...")

    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(filters.TEXT, do_echo)
    buttons_handler = CallbackQueryHandler(
        callback=keyboard_callback_handler)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(time_handler)
    application.add_handler(message_handler)
    application.add_handler(buttons_handler)

    application.run_polling()

    logger.info('Finished...')


if __name__ == '__main__':
    main()
