export PYTHONPATH=$(shell pwd)/redditbot/

dependencies:
	@poetry install

lint:
	@poetry run flake8 redditbot

test:
	@poetry run pytest -x

test-cov:
	@poetry run pytest --cov=redditbot

run-bot:
	@poetry run python -m redditbot.ui.bot
