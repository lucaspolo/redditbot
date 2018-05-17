import pytest

from crawlers.reddit_crawler import convert_upvotes_to_num, filter_by_votes, \
    convert_element_to_thread, convert_internal_link_to_absolute


@pytest.mark.parametrize('input,expected', [
    ('10k', 10000),
    ('100', 100),
])
def test_convert_upvotes_to_num(input, expected):
    assert convert_upvotes_to_num(input) == expected


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


def test_convert_element_to_thread():
    dados = {
        'data': {
            'subreddit': 'r/python',
            'title': 'python',
            'ups': '1',
            'permalink': '/r/python/comments',
            'url': 'https://www.google.com',
        }
    }

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
