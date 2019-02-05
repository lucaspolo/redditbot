import os
import logging

from telegram.ext import Updater, CommandHandler

import redditbot.crawlers.reddit_crawler as rc

DEFAULT_MESSAGE = """r/{subreddit} - [{upvotes} votos]
{title}
Link: {link}
Comentários: {comments}"""


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Está sem o que fazer? Dá um confere no Reddit!')


def nada_para_fazer(bot, update, args):
    chat_id = update.message.chat_id

    joined_args = str.join(';', args)  # If you pass separeted we join using ; separator

    subreddits = joined_args.split(';')

    if len(subreddits) == 0 or len(args) == 0:
        bot.send_message(chat_id=chat_id,
                         text='Digite o termo da procura, ex: /nadaparafazer dogs;python')
        return

    for subreddit in subreddits:
        bot.send_message(chat_id=chat_id,
                         text=f'Procurando o que está bombando em r/{subreddit}...')
        threads = rc.filter_by_votes(rc.filter_by_votes(rc.get_threads(subreddit), min_votes=5000))
        for thread in threads:
            bot.send_message(chat_id=chat_id,
                             text=DEFAULT_MESSAGE.format(**thread))
        if len(threads) == 0:
            bot.send_message(chat_id=chat_id,
                             text=f'Não encontrei nada bombando em r/{subreddit}')


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = os.environ['TELEGRAM_TOKEN']

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('nadaparafazer', nada_para_fazer,
                                          pass_args=True))

    updater.start_polling()


if __name__ == '__main__':
    main()
