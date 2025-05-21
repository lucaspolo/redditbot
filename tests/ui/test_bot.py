import pytest
import datetime
from unittest import mock
from unittest.mock import AsyncMock # For AsyncMock

from telegram import Update, User, Message, Chat # For simulating Update and related objects
from telegram.ext import ContextTypes # For simulating Context

from redditbot.ui import bot
from redditbot.ui.bot import nada_para_fazer, start, user_info # Import user_info
import httpx # For simulating API error


class TestMain:

    @mock.patch('redditbot.ui.bot.ApplicationBuilder')
    def test_main_should_register_bot_handlers_and_start_polling(
        self,
        application_builder_mock,
    ):
        app_mock = (
            application_builder_mock.return_value.token.return_value.build.return_value
        )

        bot.main()

        assert app_mock.add_handler.call_count == 4

        app_mock.run_polling.assert_called_once()


class TestNadaParaFazerBot:

    async def test_get_version_should_return_version(self):
        update = mock.MagicMock()
        update.message.reply_text = mock.AsyncMock()
        update.message.reply_sticker = mock.AsyncMock()
        context = mock.MagicMock()

        await start(update, context)

        update.message.reply_text.assert_awaited_once()

    async def test_start(self):
        update = mock.MagicMock()
        update.message.reply_text = mock.AsyncMock()
        update.message.reply_sticker = mock.AsyncMock()
        context = mock.MagicMock()

        await start(update, context)

        update.message.reply_text.assert_awaited_once_with(
            text='Está sem o que fazer? Dá um confere no Reddit!'
        )

    async def test_nada_para_fazer_should_send_help(self):
        update = mock.MagicMock()
        update.message.reply_text = mock.AsyncMock()
        update.message.reply_sticker = mock.AsyncMock()
        context = mock.MagicMock()
        context.args = ''

        await nada_para_fazer(update, context)

        update.message.reply_text.assert_called_once_with(
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )

    async def test_nada_para_fazer_should_send_messages(
        self,
        mock_request_dog
    ):
        update = mock.MagicMock()
        update.message.reply_text = mock.AsyncMock()
        update.message.reply_markdown_v2 = mock.AsyncMock()
        update.message.reply_sticker = mock.AsyncMock()
        context = mock.MagicMock()
        context.args = ['dogs']
        calls_text = [
            mock.call(
                text='Procurando o que está bombando em r/dogs...'
            )
        ]
        calls_markdown = [
            mock.call(
                text='r/dogs \\- [9999 votos]'
                     '\n**[Cute Dogs](https://www\\.reddit\\.com/r/cutedogs)**\n'
                     '\n[Comentários](https://www\\.reddit\\.com/r/cute\\_dogs)'
            )
        ]

        await nada_para_fazer(update, context)

        assert update.message.reply_text.call_count == 1
        assert update.message.reply_markdown_v2.call_count == 1
        update.message.reply_text.assert_has_calls(calls_text)
        update.message.reply_markdown_v2.assert_has_calls(calls_markdown)

    async def test_nada_para_fazer_should_send_not_found(
        self,
        mock_request_dog_with_low_votes,
    ):
        update = mock.MagicMock()
        update.message.reply_text = mock.AsyncMock()
        update.message.reply_sticker = mock.AsyncMock()
        context = mock.MagicMock()
        context.args = ['dogs']
        calls = [
            mock.call(
                text='Procurando o que está bombando em r/dogs...'
            ),
            mock.call(
                text='Não encontrei nada bombando em r/dogs'
            )
        ]

        await nada_para_fazer(update, context)

        assert update.message.reply_text.call_count == 2
        update.message.reply_text.assert_has_calls(calls)


class TestUserInfoBot:
    @pytest.mark.asyncio
    @mock.patch('redditbot.crawlers.reddit_crawler.get_user_info', new_callable=AsyncMock)
    async def test_user_info_success(self, mock_get_user_info):
        """Test user_info command for a successful user lookup."""
        username = 'testuser'
        user_data = {'name': username, 'karma': 123, 'created_utc': 1609459200.0}
        mock_get_user_info.return_value = user_data

        update = mock.create_autospec(Update, instance=True)
        update.message = mock.create_autospec(Message, instance=True)
        update.message.chat = mock.create_autospec(Chat, instance=True)
        update.message.from_user = mock.create_autospec(User, instance=True)
        update.message.reply_text = AsyncMock()

        context = mock.create_autospec(ContextTypes.DEFAULT_TYPE, instance=True)
        context.args = [username]

        await user_info(update, context)

        expected_date = datetime.datetime.fromtimestamp(user_data['created_utc'], tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        expected_message = f"User: {user_data['name']}\nKarma: {user_data['karma']}\nAccount Created: {expected_date}"
        update.message.reply_text.assert_called_once_with(expected_message)

    @pytest.mark.asyncio
    @mock.patch('redditbot.crawlers.reddit_crawler.get_user_info', new_callable=AsyncMock)
    async def test_user_info_not_found(self, mock_get_user_info):
        """Test user_info command when the user is not found."""
        username = 'nonexistentuser'
        mock_get_user_info.return_value = None

        update = mock.create_autospec(Update, instance=True)
        update.message = mock.create_autospec(Message, instance=True)
        update.message.chat = mock.create_autospec(Chat, instance=True)
        update.message.from_user = mock.create_autospec(User, instance=True)
        update.message.reply_text = AsyncMock()

        context = mock.create_autospec(ContextTypes.DEFAULT_TYPE, instance=True)
        context.args = [username]

        await user_info(update, context)

        update.message.reply_text.assert_called_once_with(f'User {username} not found.')

    @pytest.mark.asyncio
    async def test_user_info_no_username_provided(self):
        """Test user_info command when no username is provided."""
        update = mock.create_autospec(Update, instance=True)
        update.message = mock.create_autospec(Message, instance=True)
        update.message.chat = mock.create_autospec(Chat, instance=True)
        update.message.from_user = mock.create_autospec(User, instance=True)
        update.message.reply_text = AsyncMock()

        context = mock.create_autospec(ContextTypes.DEFAULT_TYPE, instance=True)
        context.args = []  # No arguments

        await user_info(update, context)

        update.message.reply_text.assert_called_once_with('Please provide a Reddit username. Usage: /userinfo <username>')

    @pytest.mark.asyncio
    @mock.patch('redditbot.crawlers.reddit_crawler.get_user_info', new_callable=AsyncMock)
    async def test_user_info_api_error(self, mock_get_user_info):
        """Test user_info command when an API error occurs."""
        username = 'erroruser'
        mock_get_user_info.side_effect = httpx.HTTPStatusError(
            "API Error", request=mock.Mock(), response=mock.Mock()
        )

        update = mock.create_autospec(Update, instance=True)
        update.message = mock.create_autospec(Message, instance=True)
        update.message.chat = mock.create_autospec(Chat, instance=True)
        update.message.from_user = mock.create_autospec(User, instance=True)
        update.message.reply_text = AsyncMock()

        context = mock.create_autospec(ContextTypes.DEFAULT_TYPE, instance=True)
        context.args = [username]

        await user_info(update, context)

        update.message.reply_text.assert_called_once_with('Sorry, something went wrong while fetching user information.')
