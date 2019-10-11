# RedditBot

Um bot que envia para você as coisas mais interessantes do Reddit!


[![Python 3](https://pyup.io/repos/github/lucaspolo/redditbot/python-3-shield.svg)](https://pyup.io/repos/github/lucaspolo/redditbot/)
[![Build Status](https://travis-ci.org/lucaspolo/redditbot.svg?branch=master)](https://travis-ci.org/lucaspolo/redditbot)
[![codecov](https://codecov.io/gh/lucaspolo/redditbot/branch/master/graph/badge.svg)](https://codecov.io/gh/lucaspolo/redditbot)
[![Maintainability](https://api.codeclimate.com/v1/badges/b460fae76331acbccff2/maintainability)](https://codeclimate.com/github/lucaspolo/redditbot/maintainability)
[![Updates](https://pyup.io/repos/github/lucaspolo/redditbot/shield.svg)](https://pyup.io/repos/github/lucaspolo/redditbot/)

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## Execução direto na linha de comando

Para executar direto no CLI chame o bot da seguinte forma:

`python3.7 -m redditbot.ui.nadaparafazer -s "dogs;python" {-m VOTOS_MINIMOS}`

Caso necessário, para verificar quais os comandos disponíveis e seus valores padrões, digite:

`python3.7 -m redditbot.ui.nadaparafazer --help`

### Execução pelo Docker

Para executar o bot basta rodar o comando:
 
`docker run -e telegram-token='[TOKEN-TELEGRAM]' -it --rm --name bot lucaspolo/reddit-bot`
 
Ele irá buscar a imagem no registry e iniciará o container.
 
Para subir o container direto do Dockerfile é necessário primeiro realizar o build da imagem:
 
`docker build -t meu_bot .`
 
Depois deve-se iniciar o container-bot passando uma variável de ambiente chamada telegram-token com o Token do bot:
 
`docker run -e TELEGRAM-TOKEN='[SEU TOKEN]' -it --rm --name bot meu_bot`
 
### Execução do bot no terminal

Para executar o bot é necessário ter uma variável de ambiente com o Token do Telegram:

`TELEGRAM_TOKEN=[SEU TOKEN]`

Depois disso basta iniciar a execução do bot:

`python3.7 -m redditbot.ui.bot.py`

Os comandos do bot são 

- /start: Inicia o bot, recebendo uma mensagem de boas vindas.
- /nadaparafazer [subreddits]: Busca nos subreddits indicados as threads que estão bombando (upvotes > 5000).

Ex:

`/nadaparafazer dogs;askreddit`
