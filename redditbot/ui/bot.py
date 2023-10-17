import logging

from importlib.metadata import version as version_function
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.helpers import escape_markdown

import redditbot.crawlers.reddit_crawler as rc
from redditbot.config import settings

DEFAULT_MESSAGE = """r/{subreddit} \\- [{upvotes} votos]
**[{title}]({link})**\n
[Comentários]({comments})"""

STICKERS = {
    'crying_piglet': 'CAACAgIAAxkBAAEXhYNjCojvibG9_v_VIAABGaq0YhoIrYQAAo8BAAIWQmsKO2O0DZs84FkpBA',
    'alpaca_hi': 'CAACAgIAAxkBAAEXhaRjComgByhjRuOjuFsM_0pZa9I8sQAClwADO2AkFLPjVSHrbN7ZKQQ',
    'duck_finding': 'CAACAgIAAxkBAAEXhapjCoqLx-ApexksbOfFtQeiTXJ8RAACSQIAAladvQoqlwydCFMhDikE',
    'ok_piglet': 'CAACAgIAAxkBAAEXhaxjCovR30n5XwH5JmDUGrUNZToNyQACegEAAhZCawqYRZuYnxC0lykE',
}


async def start(update: Update, context: CallbackContext):
    await update.message.reply_sticker(
        sticker=STICKERS['alpaca_hi']
    )
    await update.message.reply_text(
        text='Está sem o que fazer? Dá um confere no Reddit!'
    )


async def nada_para_fazer(update: Update, context: CallbackContext):
    args = context.args
    joined_args = str.join(';', args)  # If you pass separeted we join using ; separator

    subreddits = joined_args.split(';')

    if len(subreddits) == 0 or len(args) == 0:
        await update.message.reply_text(
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )
        await update.message.reply_sticker(
            sticker=STICKERS['duck_finding']
        )
        return

    await send_subreddit(update, subreddits)


async def send_subreddit(update, subreddits):
    canais_message = ', '.join([
        f'r/{subreddit}' for subreddit in subreddits
    ])
    await update.message.reply_text(
        text=f'Procurando o que está bombando em {canais_message}...'
    )
    await update.message.reply_sticker(
        sticker=STICKERS['ok_piglet']
    )

    threads = await rc.get_subreddits(subreddits)
    filtered_threads = rc.filter_by_votes(threads, min_votes=settings.MIN_VOTES)
    for thread in filtered_threads:
        message = DEFAULT_MESSAGE.format(
            subreddit=escape_markdown(thread['subreddit'], version=2),
            upvotes=thread['upvotes'],
            title=escape_markdown(thread['title'], version=2),
            link=escape_markdown(thread['link'], version=2),
            comments=escape_markdown(thread['comments'], version=2),
        )
        await update.message.reply_markdown_v2(
            text=message
        )
    if len(filtered_threads) == 0:
        await update.message.reply_text(
            text=f'Não encontrei nada bombando em {canais_message}'
        )
        await update.message.reply_sticker(
            sticker=STICKERS['crying_piglet']
        )


async def get_version(update: Update, context: CallbackContext):
    version = version_function('redditbot')

    await update.message.reply_text(
        text=f'Version: {version}'
    )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = settings.TELEGRAM_TOKEN

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(
        CommandHandler('nadaparafazer', nada_para_fazer)
    )
    app.add_handler(
        CommandHandler('n', nada_para_fazer)
    )
    app.add_handler(
        CommandHandler('version', get_version)
    )

    app.run_polling()


if __name__ == '__main__':
    main()
