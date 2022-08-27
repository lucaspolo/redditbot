from unittest import mock
from unittest.mock import MagicMock, call

import asynctest
from asynctest import CoroutineMock

from redditbot.ui import bot
from redditbot.ui.bot import nada_para_fazer, start


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
        update = MagicMock()
        update.message.reply_text = CoroutineMock()
        context = MagicMock()

        await start(update, context)

        update.message.reply_text.assert_awaited_once()

    async def test_start(self):
        update = MagicMock()
        update.message.reply_text = CoroutineMock()
        context = MagicMock()

        await start(update, context)

        update.message.reply_text.assert_awaited_once_with(
            text='Está sem o que fazer? Dá um confere no Reddit!'
        )

    async def test_nada_para_fazer_should_send_help(self):
        update = MagicMock()
        update.message.reply_text = CoroutineMock()
        context = MagicMock()
        context.args = ''

        await nada_para_fazer(update, context)

        update.message.reply_text.assert_called_once_with(
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )

    async def test_nada_para_fazer_should_send_messages(
        self,
        mock_request_dog
    ):
        update = MagicMock()
        update.message.reply_text = CoroutineMock()
        update.message.reply_markdown_v2 = CoroutineMock()
        context = MagicMock()
        context.args = ['dogs']
        calls_text = [
            call(
                text='Procurando o que está bombando em r/dogs...'
            )
        ]
        calls_markdown = [
            call(
                text='r/dogs \\- [9999 votos]'
                     '\n**Cute Dogs**'
                     '\n[Link](https://www\\.reddit\\.com/r/cutedogs)'
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
        update = MagicMock()
        update.message.reply_text = CoroutineMock()
        context = MagicMock()
        context.args = ['dogs']
        calls = [
            call(
                text='Procurando o que está bombando em r/dogs...'
            ),
            call(
                text='Não encontrei nada bombando em r/dogs'
            )
        ]

        await nada_para_fazer(update, context)

        assert update.message.reply_text.call_count == 2
        update.message.reply_text.assert_has_calls(calls)
