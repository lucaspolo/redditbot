FROM python:3.12-slim
ENV PYTHONPATH=.
WORKDIR /usr/src/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY . .

CMD [ "uv", "run", "python", "./redditbot/ui/bot.py" ]
