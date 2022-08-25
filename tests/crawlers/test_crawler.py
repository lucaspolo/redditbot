from unittest import mock

from redditbot.crawlers.reddit_crawler import (
    filter_by_votes,
    convert_element_to_thread,
    convert_internal_link_to_absolute,
    get_threads,
    print_subreddits
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


def test_get_threads(mock_request_dog):

    threads = get_threads(['dogs'])

    assert len(threads) == 1


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
