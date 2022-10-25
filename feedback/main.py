from logging import getLogger

from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler, ContextTypes, CommandHandler

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from echo.config import load_config


logger = getLogger(__name__)

config = load_config()



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


async def do_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send me a text and I will forward it to the author of the channel",
    )


@debug_requests
async def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id == config.FEEDBACK_USER_ID:
        # Look at replays
        reply = update.effective_message.reply_to_message
        if reply:
            logger.info(reply)

            # TODO: improve sending attachments
            text = "Message from the author of the channel:\n\n" + update.message.text
            await context.bot.send_message(
                chat_id=reply.forward_from.id,
                text=text,
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Make a reply to reply to the author of the post",
            )
    else:
        # Send everything as is
        # TODO: improve sending attachments
        await context.bot.forward_message(
            chat_id=config.FEEDBACK_USER_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.effective_message.id,
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="The message has been sent.",
        )


def main():
    logger.info("Launching the bot...")

    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(filters.ALL, do_echo)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()

    logger.info('Finished...')


if __name__ == "__main__":
    main()
