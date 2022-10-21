from subprocess import Popen, PIPE

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes

from config import load_config


async def do_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! Send me anything",
    )


async def do_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This is a tutorial bot\n\n"
        "The list of available commands is in the menu\n\n"
        "I also reply to any message",
    )


async def do_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Check server time
    """
    process = Popen("date", stdout=PIPE)
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
    )


async def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = "Your ID = {}\n\n{}".format(chat_id, update.message.text)

    await context.bot.send_message(
        chat_id=chat_id,
        text=text
    )


def main():
    config = load_config()

    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(filters.TEXT, do_echo)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(time_handler)
    application.add_handler(message_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
