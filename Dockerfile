FROM python:3.11-slim
ENV PYTHONPATH=.
WORKDIR /usr/src/app

COPY . .

RUN pip install -U pip poetry
RUN poetry install --only main

CMD [ "poetry", "run", "python", "./redditbot/ui/bot.py" ]
