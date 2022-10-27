""" Sample message with different font styles:
    - bold
    - italic
    - link
    - on line code
    - multiline code

    Also, how do I attach an image to the text?
"""
from logging import getLogger

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from echo.config import load_config
from echo.utils import debug_requests

config = load_config()

logger = getLogger(__name__)


@debug_requests
async def bold_text_md(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '*Bold* font',
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
async def bold_text_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '<b>Bold</b> font',
        parse_mode=ParseMode.HTML,
    )


@debug_requests
async def italic_text_md(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '_Italic_ font. Cannot be combined _*with*_ *_bold_* :(',
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
async def italic_text_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '<i>Italic</i> font',
        parse_mode=ParseMode.HTML,
    )


@debug_requests
async def text_with_url_md(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Learning on the [channel](https://www.youtube.com/c/it_everyday)! '
        'There is a lot of information for self-education',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@debug_requests
async def text_with_url_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Learning on the <a href="https://www.youtube.com/c/it_everyday">channel</a>! '
        'There is a lot of information for self-education',
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@debug_requests
async def code_md(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        'Examples with code:',
        '',
        'Code on one line: `update.message.reply_text()`',
        '',
        'Code on multiple lines:',
        '```',
        'await update.message.reply_text(',
        '   "xex",',
        '   parse_mode=ParseMode.MARKDOWN,',
        ')',
        '```',
    ]
    await update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
async def code_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        'Examples with code:',
        '',
        'Code on one line: <code>update.message.reply_text()</code>',
        '',
        'Code on multiple lines:',
        '<pre>',
        'await update.message.reply_text(',
        '   "xex",',
        '   parse_mode=ParseMode.HTML,',
        ')',
        '</pre>',
    ]
    await update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
    )


@debug_requests
async def image_hack_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        'blah blah <a href="https://picsum.photos/200/300">&#8205;</a>',
        'there can be any amount of text, the main thing is that the picture is the first link ',
        'in the entire text, and there is an invisible space inside the "a" tag',
    ]
    await update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


@debug_requests
async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        'Telegram Features for Marking Messages:',
        '',
        '*MarkDown*',
        '/bold1 -- bold font',
        '/italic1 -- italic font',
        '/url1 -- link in text',
        '/code1 -- working with code',
        '',
        '*HTML*',
        '/bold2 -- bold font',
        '/italic2 -- italic font',
        '/url2 -- link in text',
        '/code2 -- working with code',
        '/img -- hack: picture under text',
    ]
    await update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.MARKDOWN,
    )


def main():
    logger.info('Started Markup-Bot')
    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    # Show different formatting
    application.add_handler(CommandHandler('bold1', bold_text_md))
    application.add_handler(CommandHandler('bold2', bold_text_html))
    application.add_handler(CommandHandler('italic1', italic_text_md))
    application.add_handler(CommandHandler('italic2', italic_text_html))
    application.add_handler(CommandHandler('url1', text_with_url_md))
    application.add_handler(CommandHandler('url2', text_with_url_html))
    application.add_handler(CommandHandler('code1', code_md))
    application.add_handler(CommandHandler('code2', code_html))
    application.add_handler(CommandHandler('img', image_hack_html))

    # If nothing came up - send a list of commands
    application.add_handler(MessageHandler(filters.ALL, echo_handler))

    application.run_polling()
    logger.info('Stopped Markup-Bot')


if __name__ == "__main__":
    main()
