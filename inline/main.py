import asyncio

from logging import getLogger

from telegram import Update, ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters, InlineQueryHandler

from echo.config import load_config
from echo.utils import debug_requests
from inline.search import Searcher

config = load_config()
logger = getLogger(__name__)

search = Searcher()


@debug_requests
async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    bot_details = await context.bot.get_me()
    bot_username = bot_details.username
    await update.message.reply_text(
        text=f'There is nothing in the bot. Go to any other dialog and start typing the bot\'s username @{bot_username}',
        reply_markup=ReplyKeyboardRemove(),
    )


@debug_requests
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    query = query.strip().lower()
    logger.info('inline: %s', query)

    # List of similar coin names
    results = []
    names = search.parse_query(text=query)[0:50]
    prices = search.get_prices(names=names)
    for i, (name, price) in enumerate(prices):
        results.append(
            InlineQueryResultArticle(
                id=i + 1,
                title=f'{name} now?',
                input_message_content=InputTextMessageContent(
                    message_text=f'{name} is ${price} now!',
                )
            )
        )

    # Nothing found
    if query and not results:
        results.append(
            InlineQueryResultArticle(
                id=999,
                title='Nothing found',
                input_message_content=InputTextMessageContent(
                    message_text=f'No results were found for "{query}"',
                ),
            )
        )

    await update.inline_query.answer(
        results=results,
        cache_time=10,
    )


async def bot_get_me(app):
    logger.info(await app.bot.get_me())


def main():
    # Create a bot
    logger.info('Start bot')

    app = ApplicationBuilder().token('<TOKEN>').build()

    asyncio.ensure_future(bot_get_me(app))

    app.add_handler(MessageHandler(
        filters=filters.TEXT, callback=echo_handler))
    app.add_handler(InlineQueryHandler(inline_handler))

    app.run_polling()

    logger.info('Finish bot')


if __name__ == '__main__':
    main()
