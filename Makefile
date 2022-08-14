export PYTHONPATH=$(shel pwd)/redditbot/

dependencies:
	@poetry install

lint:
	@poetry run flake8 redditbot

test:
	@poetry run pytest -x

test-cov:
	@poetry run pytest --cov=redditbot
