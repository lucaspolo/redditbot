import pytest


@pytest.fixture
def mock_request_dog(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='https://www.reddit.com/r/dogs/top.json?sort=new',
        json={
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


@pytest.fixture
def mock_request_dog_with_low_votes(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='https://www.reddit.com/r/dogs/top.json?sort=new',
        json={
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


@pytest.fixture
def mock_request_user(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='https://www.reddit.com/user/testuser/about.json',
        json={
            'data': {
                'name': 'testuser',
                'link_karma': 1000,
                'comment_karma': 500,
                'created_utc': 1609459200.0,
            }
        },
    )


@pytest.fixture
def mock_request_user_not_found(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='https://www.reddit.com/user/nonexistent/about.json',
        status_code=404,
    )
