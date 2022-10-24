from telegram import KeyboardButton, ReplyKeyboardMarkup

BUTTON1_HELP = "Help"
BUTTON2_TIME = "Time"


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_HELP),
            KeyboardButton(BUTTON2_TIME),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
