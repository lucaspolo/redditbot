FROM python:3.10
ENV PYTHONPATH=.
WORKDIR /usr/src/app

COPY . .

RUN pip install poetry
RUN poetry install

CMD [ "poetry", "run", "python", "./redditbot/ui/bot.py" ]
