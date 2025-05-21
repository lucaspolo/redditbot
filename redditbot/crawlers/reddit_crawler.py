import asyncio
from http import HTTPStatus
from itertools import chain

import httpx

BASE_URL = 'https://www.reddit.com'

REDDIT_URL = 'https://www.reddit.com/r/{0}/top.json'


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


async def get_user_info(username: str):
    """Fetches information about a Reddit user.

    Args:
        username: The username of the Reddit user.

    Returns:
        A dictionary containing user information (name, karma, created_utc),
        or None if the user is not found.
    Raises:
        Exception: If there is an API error.
    """
    url = f"{BASE_URL}/user/{username}/about.json"
    headers = {'User-Agent': 'telegram:redditbot:v1'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == HTTPStatus.OK:
        data = response.json()['data']
        return {
            'name': data['name'],
            'karma': data['total_karma'],
            'created_utc': data['created_utc'],
        }
    elif response.status_code == HTTPStatus.NOT_FOUND:
        return None
    else:
        response.raise_for_status()
