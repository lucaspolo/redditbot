import asyncio
from http import HTTPStatus
from itertools import chain

import httpx

BASE_URL = 'https://www.reddit.com'

REDDIT_URL = 'https://www.reddit.com/r/{0}/top.json'
USER_URL = 'https://www.reddit.com/user/{0}/about.json'


async def get_subreddits(subreddits):
    """Recupera as threads e suas informações do subreddit

    :param subreddit: subreddit a ser pesquisado
    :return: lista de threads do subreddit
    """

    async with httpx.AsyncClient() as client:
        threads = await asyncio.gather(
            *[asyncio.create_task(_get_threads_for_subreddit(client, subreddit))
                for subreddit in sorted(subreddits)]
        )

    return list(chain.from_iterable(threads))


async def _get_threads_for_subreddit(client, subreddit):
    threads = []
    headers = {
        'User-Agent': 'telegram:redditbot:v1',
    }
    response = await client.get(
            REDDIT_URL.format(subreddit),
            params={'sort': 'new'},
            headers=headers
    )
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        elements_threads = filter(
            lambda x: x['data'].get('subreddit'), data['data']['children']
        )
        threads = [convert_element_to_thread(element) for element in elements_threads]
    return threads


def convert_element_to_thread(element):

    thread = {}
    data = element['data']
    thread['subreddit'] = data['subreddit']
    thread['title'] = data['title']
    thread['upvotes'] = data['ups']
    thread['comments'] = BASE_URL + data['permalink']
    thread['link'] = convert_internal_link_to_absolute(data['url'])

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


async def get_user_info(username):
    """Fetch Reddit user information

    :param username: Reddit username to look up
    :return: dict with user info or None if not found
    """
    headers = {
        'User-Agent': 'telegram:redditbot:v1',
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            USER_URL.format(username),
            headers=headers
        )
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        user_data = data.get('data', {})
        return {
            'name': user_data.get('name'),
            'link_karma': user_data.get('link_karma', 0),
            'comment_karma': user_data.get('comment_karma', 0),
            'created_utc': user_data.get('created_utc', 0),
        }
    return None
