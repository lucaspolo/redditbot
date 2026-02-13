export PYTHONPATH=$(shell pwd)/redditbot/

dependencies:
	@uv sync

lint:
	@uv run flake8 redditbot

test:
	@uv run pytest -x

test-cov:
	@uv run pytest --cov redditbot

run-bot:
	@uv run python -m redditbot.ui.bot
