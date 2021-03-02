FROM python:3.9
ENV PYTHONPATH=.
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./redditbot/ui/bot.py" ]
