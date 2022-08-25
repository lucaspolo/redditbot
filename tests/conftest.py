import pytest
from aioresponses import aioresponses


@pytest.fixture
def mock_request_dog():
    with aioresponses() as m:
        m.get(
            url='https://www.reddit.com/r/dogs/top.json?sort=new',
            status=200,
            payload={
                'data': {
                    'children': [
                        {
                            'data': {
                                'subreddit': 'dogs',
                                'title': 'Cute Dogs',
                                'ups': 9999,
                                'permalink': '/r/cute_dogs',
                                'url': '/r/cutedogs'
                            }
                        }
                    ]
                }
            },
        )
        yield m


@pytest.fixture
def mock_request_dog_with_low_votes():
    with aioresponses() as m:
        m.get(
            url='https://www.reddit.com/r/dogs/top.json?sort=new',
            status=200,
            payload={
                'data': {
                    'children': [
                        {
                            'data': {
                                'subreddit': 'dogs',
                                'title': 'Cute Dogs',
                                'ups': 1,
                                'permalink': '/r/cute_dogs',
                                'url': '/r/cutedogs'
                            }
                        }
                    ]
                }
            },
        )
        yield m
