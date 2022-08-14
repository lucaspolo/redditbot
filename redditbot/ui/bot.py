import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import redditbot.crawlers.reddit_crawler as rc

DEFAULT_MESSAGE = """r/{subreddit} - [{upvotes} votos]
{title}
Link: {link}
Comentários: {comments}"""


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Está sem o que fazer? Dá um confere no Reddit!'
    )


def nada_para_fazer(update: Update, context: CallbackContext):
    args = context.args
    joined_args = str.join(';', args)  # If you pass separeted we join using ; separator

    subreddits = joined_args.split(';')

    if len(subreddits) == 0 or len(args) == 0:
        update.message.reply_text(
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )
        return

    send_subreddit(update, subreddits)


def send_subreddit(update, subreddits):
    canais_message = ', '.join([
        f'r/{subreddit}' for subreddit in subreddits
    ])
    update.message.reply_text(
        text=f'Procurando o que está bombando em {canais_message}...'
    )
    threads = rc.get_threads(subreddits)
    filtered_threads = rc.filter_by_votes(threads, min_votes=500)
    threads = rc.filter_by_votes(filtered_threads)
    for thread in threads:
        update.message.reply_text(
            text=DEFAULT_MESSAGE.format(**thread)
        )
    if len(threads) == 0:
        update.message.reply_text(
            text=f'Não encontrei nada bombando em {canais_message}'
        )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    token = os.getenv('TELEGRAM_TOKEN')

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        CommandHandler('nadaparafazer', nada_para_fazer)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
