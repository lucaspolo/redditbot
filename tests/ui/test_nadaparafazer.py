from unittest import mock

from click.testing import CliRunner

from redditbot.ui.nadaparafazer import main


class TestNadaParaFazer:

    @mock.patch('redditbot.ui.nadaparafazer.filter_by_votes')
    @mock.patch('redditbot.ui.nadaparafazer.get_subreddits')
    @mock.patch('redditbot.ui.nadaparafazer.print_subreddits')
    def test_nada_para_fazer_main_should_call_print(
        self,
        print_subreddits_mock,
        get_threads_mock,
        filter_by_votes_mock
    ):
        runner = CliRunner()
        result = runner.invoke(main, ['-s', 'fake'])

        assert result.exit_code == 0
        print_subreddits_mock.assert_called_once()
