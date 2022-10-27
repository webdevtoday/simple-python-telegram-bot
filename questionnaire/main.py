from logging import getLogger

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, MessageHandler, filters, CommandHandler, ContextTypes

from echo.config import load_config
from echo.utils import debug_requests
from questionnaire.validators import GENDER_MAP, gender_hru, validate_age, validate_gender


config = load_config()

logger = getLogger(__name__)


NAME, GENDER, AGE = range(3)


@debug_requests
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ask for a name
    await update.message.reply_text(
        'Enter your name to continue:',
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


@debug_requests
async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get a name
    context.user_data[NAME] = update.message.text
    logger.info('user_data: %s', context.user_data)

    # Ask gender
    genders = [f'{key} - {value}' for key, value in GENDER_MAP.items()]
    genders = '\n'.join(genders)
    await update.message.reply_text(f'''
Select your gender to continue:
{genders}
''')
    # TODO: buttons !
    return GENDER


@debug_requests
async def age_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get gender
    gender = validate_gender(text=update.message.text)
    if gender is None:
        await update.message.reply_text('Please enter the correct gender!')
        return GENDER

    context.user_data[GENDER] = gender
    logger.info('user_data: %s', context.user_data)

    # Ask age
    await update.message.reply_text('''
Enter your age:
''')
    return AGE


@debug_requests
async def finish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get age
    age = validate_age(text=update.message.text)
    if age is None:
        await update.message.reply_text('Please enter a valid age!')
        return AGE

    context.user_data[AGE] = age
    logger.info('user_data: %s', context.user_data)

    # TODO: here is the final entry
    # TODO 2: clear `user_data`

    # End dialogue
    await update.message.reply_text(f'''
All data successfully saved!
You are: {context.user_data[NAME]}, gender: {gender_hru(context.user_data[GENDER])}, age: {context.user_data[AGE]}
''')
    return ConversationHandler.END


@debug_requests
async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Cancel the entire dialogue process. Data will be lost
    """
    await update.message.reply_text('Cancel. To start from scratch press /start')
    return ConversationHandler.END


@debug_requests
async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Click /start to fill out the form!',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    logger.info('Start bot')

    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
        ],
        states={
            NAME: [
                MessageHandler(filters.ALL, name_handler),
            ],
            GENDER: [
                MessageHandler(filters.ALL, age_handler),
            ],
            AGE: [
                MessageHandler(filters.ALL, finish_handler),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.ALL, echo_handler))

    application.run_polling()

    logger.info('Finish bot')


if __name__ == '__main__':
    main()
