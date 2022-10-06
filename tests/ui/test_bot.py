from unittest import mock

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
