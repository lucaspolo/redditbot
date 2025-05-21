import pytest
import httpx
from unittest import mock

from redditbot.crawlers.reddit_crawler import (
    filter_by_votes,
    convert_element_to_thread,
    convert_internal_link_to_absolute,
    print_subreddits, get_subreddits,
    get_user_info, # import the function to be tested
    BASE_URL # import for constructing url in mock
)
from http import HTTPStatus # import for status codes


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


@pytest.mark.asyncio
async def test_get_user_info_success():
    """Test get_user_info for a successful API call."""
    username = "testuser"
    mock_response_data = {
        "data": {
            "name": username,
            "total_karma": 12345,
            "created_utc": 1609459200,  # Example timestamp: 2021-01-01 00:00:00 UTC
        }
    }
    expected_result = {
        "name": username,
        "karma": 12345,
        "created_utc": 1609459200,
    }

    mock_response = mock.Mock(spec=httpx.Response)
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = mock_response_data

    with mock.patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        user_data = await get_user_info(username)
        mock_get.assert_called_once_with(
            f"{BASE_URL}/user/{username}/about.json",
            headers={'User-Agent': 'telegram:redditbot:v1'}
        )
        assert user_data == expected_result


@pytest.mark.asyncio
async def test_get_user_info_not_found():
    """Test get_user_info for a user not found (404) response."""
    username = "nonexistentuser"

    mock_response = mock.Mock(spec=httpx.Response)
    mock_response.status_code = HTTPStatus.NOT_FOUND

    with mock.patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        user_data = await get_user_info(username)
        mock_get.assert_called_once_with(
            f"{BASE_URL}/user/{username}/about.json",
            headers={'User-Agent': 'telegram:redditbot:v1'}
        )
        assert user_data is None


@pytest.mark.asyncio
async def test_get_user_info_api_error():
    """Test get_user_info for an API error (e.g., 500 status)."""
    username = "testuser_api_error"

    mock_response = mock.Mock(spec=httpx.Response)
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    # Configure raise_for_status to raise an exception, as it would in httpx
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error", request=mock.Mock(), response=mock_response
    )


    with mock.patch('httpx.AsyncClient.get', return_value=mock_response) as mock_get:
        with pytest.raises(httpx.HTTPStatusError):
            await get_user_info(username)
        mock_get.assert_called_once_with(
            f"{BASE_URL}/user/{username}/about.json",
            headers={'User-Agent': 'telegram:redditbot:v1'}
        )