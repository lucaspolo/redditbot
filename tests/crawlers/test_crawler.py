from unittest import mock

from redditbot.crawlers.reddit_crawler import (
    filter_by_votes,
    convert_element_to_thread,
    convert_internal_link_to_absolute,
    print_subreddits,
    get_subreddits,
    get_user_info
)


def test_filter_by_upvotes():
    threads = [
        {
            'upvotes': 1,
        },
        {
            'upvotes': 100,
        },
        {
            'upvotes': 200,
        },
        {
            'upvotes': 300,
        },
    ]

    assert len(filter_by_votes(threads, min_votes=150)) == 2


def test_convert_element_to_thread(dados):

    thread = convert_element_to_thread(dados)
    assert thread['subreddit'] == 'r/python'
    assert thread['title'] == 'python'
    assert thread['upvotes'] == '1'
    assert thread['comments'] == 'https://www.reddit.com/r/python/comments'
    assert thread['link'] == 'https://www.google.com'

    dados['data']['url'] = '/r/batata'

    thread = convert_element_to_thread(dados)

    assert thread['link'] == 'https://www.reddit.com/r/batata'


def test_convert_internal_link_to_absolute():
    assert convert_internal_link_to_absolute('/r/python/comments') == 'https://www.reddit.com/r/python/comments'


@mock.patch('builtins.print')
def test_print_subreddits(print_mock):
    thread = {
        'subreddit': 'Dog',
        'upvotes': 999,
        'title': 'Cute Dogs',
        'link': 'http://doguitos.com',
        'comments': 'http://comments.com'
    }

    print_subreddits([thread])

    assert print_mock.call_count == 3


async def test_get_subreddits_should_return_threads(mock_request_dog):
    threads = await get_subreddits(['dogs'])

    assert len(threads) == 1


async def test_get_user_info_should_return_user_data(mock_request_user):
    user = await get_user_info('testuser')

    assert user['name'] == 'testuser'
    assert user['link_karma'] == 1000
    assert user['comment_karma'] == 500
    assert user['created_utc'] == 1609459200.0


async def test_get_user_info_should_return_none_for_not_found(
    mock_request_user_not_found
):
    user = await get_user_info('nonexistent')

    assert user is None