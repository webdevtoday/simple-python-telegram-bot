import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler


TOKEN = '<token>'

ADMIN_IDS = [123, 0, ]

MAIN_ADMIN_ID = 0


async def do_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Your ID = {}\n\n{}".format(
            update.message.chat_id, update.message.text)
    )


def admin_access(f):

    async def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message'):
            if update.message.chat_id in ADMIN_IDS:
                print("Access is allowed!")
                return await f(*args, **kwargs)
            else:
                print("Access is not allowed!")
        else:
            print('No update argument')

    return inner


def log_errors(f):

    async def inner(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            error_message = f'[ADMIN] An error has occurred: {e}'
            print(error_message)

            update = args[0]
            context = args[1]
            if update and hasattr(update, 'message'):
                # Any error message is always sent to the main admin
                if context and hasattr(context, 'bot'):
                    await context.bot.send_message(
                        chat_id=MAIN_ADMIN_ID,
                        text=error_message,
                    )

                # Send an error message only if it happened to you
                # if update.message.chat_id in ADMIN_IDS:
                #     await update.message.reply_text(
                #         text=error_message
                #     )

            raise e

    return inner


@admin_access
@log_errors
async def secret_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text='secret!')
    rrrr -= 1


@log_errors
async def secret_command2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.xxxx.reply_text(text='secret 222!')


async def bot_get_me(app):
    print(await app.bot.get_me())


def main():
    app = ApplicationBuilder().token(TOKEN).connect_timeout(
        0.5).read_timeout(1.0).build()

    asyncio.ensure_future(bot_get_me(app))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, do_echo))
    app.add_handler(CommandHandler('secret', secret_command))
    app.add_handler(CommandHandler('secret2', secret_command2))

    app.run_polling()


if __name__ == '__main__':
    main()
