from unittest import mock
from unittest.mock import MagicMock, call

from redditbot.ui import bot
from redditbot.ui.bot import nada_para_fazer, start


class TestMain:

    @mock.patch('redditbot.ui.bot.Updater')
    def test_main_should_register_bot_handlers_and_start_polling(
        self,
        updater,
    ):
        updater_mock = updater.return_value
        dispatcher_mock = updater_mock.dispatcher

        bot.main()

        assert dispatcher_mock.add_handler.call_count == 2

        updater_mock.start_polling.assert_called_once()


class TestNadaParaFazerBot:

    def test_start(self):
        update = MagicMock()
        context = MagicMock()

        start(update, context)

        update.message.reply_text.assert_called_once_with(
            text='Está sem o que fazer? Dá um confere no Reddit!'
        )

    def test_nada_para_fazer_should_send_help(self):
        update = MagicMock()
        context = MagicMock()
        context.args = ''

        nada_para_fazer(update, context)

        update.message.reply_text.assert_called_once_with(
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )

    def test_nada_para_fazer_should_send_messages(
        self,
        mock_request_dog
    ):
        update = MagicMock()
        context = MagicMock()
        context.args = ['dogs']
        calls = [
            call(
                text='Procurando o que está bombando em r/dogs...'
            ),
            call(
                text='r/dogs - [9999 votos]\n'
                     'Cute Dogs\n'
                     'Link: https://www.reddit.com/r/cutedogs\n'
                     'Comentários: https://www.reddit.com/r/cute_dogs'
            )
        ]

        nada_para_fazer(update, context)

        assert update.message.reply_text.call_count == 2
        update.message.reply_text.assert_has_calls(calls)

    def test_nada_para_fazer_should_send_not_found(
        self,
        mock_request_dog_with_low_votes,
    ):
        update = MagicMock()
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

        nada_para_fazer(update, context)

        assert update.message.reply_text.call_count == 2
        update.message.reply_text.assert_has_calls(calls)
