from unittest import mock
from unittest.mock import MagicMock, call

from redditbot.ui import bot
from redditbot.ui.bot import nada_para_fazer, start


class TestMain:

    @mock.patch('redditbot.ui.bot.os')
    @mock.patch('redditbot.ui.bot.Updater')
    def test_main_should_register_bot_handlers_and_start_polling(
        self,
        updater,
        os
    ):
        updater_mock = updater.return_value
        dispatcher_mock = updater_mock.dispatcher

        bot.main()

        assert dispatcher_mock.add_handler.call_count == 2

        updater_mock.start_polling.assert_called_once()


class TestNadaParaFazerBot:

    def test_start(self):
        bot_mock = MagicMock()
        update_mock = MagicMock()
        update_mock.message.chat_id = 1

        start(bot_mock, update_mock)

        bot_mock.send_message.assert_called_once_with(
            chat_id=1,
            text='Está sem o que fazer? Dá um confere no Reddit!'
        )

    def test_nada_para_fazer_should_send_help(self):
        bot_mock = MagicMock()
        update_mock = MagicMock()
        update_mock.message.chat_id = 1
        args = ''

        nada_para_fazer(bot_mock, update_mock, args)

        bot_mock.send_message.assert_called_once_with(
            chat_id=update_mock.message.chat_id,
            text='Digite o termo da procura, ex: /nadaparafazer dogs;python'
        )

    def test_nada_para_fazer_should_send_messages(
        self,
        mock_request_dog
    ):
        bot_mock = MagicMock()
        update_mock = MagicMock()
        update_mock.message.chat_id = 1
        args = ['dogs']
        calls = [
            call(
                chat_id=update_mock.message.chat_id,
                text='Procurando o que está bombando em r/dogs...'
            ),
            call(
                chat_id=update_mock.message.chat_id,
                text='r/dogs - [9999 votos]\n'
                     'Cute Dogs\n'
                     'Link: https://www.reddit.com/r/cutedogs\n'
                     'Comentários: https://www.reddit.com/r/cute_dogs'
            )
        ]

        nada_para_fazer(bot_mock, update_mock, args)

        assert bot_mock.send_message.call_count == 2
        bot_mock.send_message.assert_has_calls(calls)

    def test_nada_para_fazer_should_send_not_found(
        self,
        mock_request_dog_with_low_votes,
    ):
        bot_mock = MagicMock()
        update_mock = MagicMock()
        update_mock.message.chat_id = 1
        args = ['dogs']
        calls = [
            call(
                chat_id=update_mock.message.chat_id,
                text='Procurando o que está bombando em r/dogs...'
            ),
            call(
                chat_id=update_mock.message.chat_id,
                text='Não encontrei nada bombando em r/dogs'
            )
        ]

        nada_para_fazer(bot_mock, update_mock, args)

        assert bot_mock.send_message.call_count == 2
        bot_mock.send_message.assert_has_calls(calls)
