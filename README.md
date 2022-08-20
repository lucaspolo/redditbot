# RedditBot

Um bot que envia para você as coisas mais interessantes do Reddit!

## Execução direto na linha de comando

Para executar direto no CLI chame o bot da seguinte forma:

`python -m redditbot.ui.nadaparafazer -s "dogs;python" {-m VOTOS_MINIMOS}`

Caso necessário, para verificar quais os comandos disponíveis e seus valores padrões, digite:

`python -m redditbot.ui.nadaparafazer --help`

### Execução pelo Docker

Para executar o bot basta rodar o comando:
 
`docker run -e TELEGRAM_TOKEN='[TOKEN-TELEGRAM]' -it --rm --name bot lucaspolo/redditbot`
 
Ele irá buscar a imagem no registry e iniciará o container.
 
Para subir o container direto do Dockerfile é necessário primeiro realizar o build da imagem:
 
`docker build -t meu_bot .`
 
Depois deve-se iniciar o container-bot passando uma variável de ambiente chamada TELEGRAM_TOKEN com o Token do bot:
 
`docker run -e TELEGRAM_TOKEN='[SEU TOKEN]' -it --rm --name bot meu_bot`
 
### Execução do bot no terminal

Para executar o bot é necessário ter uma variável de ambiente com o Token do Telegram:

`export TELEGRAM_TOKEN=[SEU TOKEN]`

Depois disso basta iniciar a execução do bot:

`python -m redditbot.ui.bot.py`

Os comandos do bot são 

- /start: Inicia o bot, recebendo uma mensagem de boas vindas.
- /nadaparafazer [subreddits]: Busca nos subreddits indicados as threads que estão bombando (upvotes > 5000).

Ex:

`/nadaparafazer dogs;askreddit`
