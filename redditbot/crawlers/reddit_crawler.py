import asyncio
from http import HTTPStatus
from itertools import chain

import aiohttp

BASE_URL = 'https://www.reddit.com'

REDDIT_URL = 'https://www.reddit.com/r/{0}/top.json'


async def get_subreddits(subreddits):
    """Recupera as threads e suas informações do subreddit

    :param subreddit: subreddit a ser pesquisado
    :return: lista de threads do subreddit
    """

    async with aiohttp.ClientSession() as session:
        threads = await asyncio.gather(
            *[asyncio.create_task(_get_threads_for_subreddit(session, subreddit))
                for subreddit in sorted(subreddits)]
        )

    return list(chain.from_iterable(threads))


async def _get_threads_for_subreddit(session, subreddit):

    headers = {
        'User-Agent': 'telegram:redditbot:v1',
    }
    async with session.get(
            REDDIT_URL.format(subreddit),
            params={'sort': 'new'},
            headers=headers
    ) as response:
        elements_threads = []
        if response.status == HTTPStatus.OK:
            data = await response.json()
            elements_threads = data['data']['children']

        threads = [convert_element_to_thread(element) for element in elements_threads]
        return threads


def convert_element_to_thread(element):

    thread = {}
    dados = element['data']
    thread['subreddit'] = dados['subreddit']
    thread['title'] = dados['title']
    thread['upvotes'] = dados['ups']
    thread['comments'] = BASE_URL + dados['permalink']
    thread['link'] = convert_internal_link_to_absolute(dados['url'])

    return thread


def convert_internal_link_to_absolute(link):
    if link.startswith('/r/'):
        return BASE_URL + link
    else:
        return link


def print_subreddits(threads):
    """Imprime de maneira formatada as threads do subreddit"""
    for thread in threads:
        print(f"r/{thread['subreddit']} - [{thread['upvotes']}] {thread['title']}")
        print(f"\tLink: {thread['link']}")
        print(f"\tComments: {thread['comments']}\n")


def filter_by_votes(threads, min_votes=1):
    return [thread for thread in threads if thread['upvotes'] > min_votes]
