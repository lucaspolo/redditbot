from unittest import mock
from unittest.mock import MagicMock

from redditbot.ui import bot
from redditbot.ui.bot import nada_para_fazer


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
