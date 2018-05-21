import pytest


@pytest.fixture(scope="session")
def dados():
    # Setup
    dados = {
        'data': {
            'subreddit': 'r/python',
            'title': 'python',
            'ups': '1',
            'permalink': '/r/python/comments',
            'url': 'https://www.google.com',
        }
    }
    yield dados

    # O código abaixo desta função será executado como teardown
    print("Teardown")
