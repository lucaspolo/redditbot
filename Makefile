lint:
	flake8 redditbot

test:
	pytest -x

test-cov:
	pytest --cov=redditbot
