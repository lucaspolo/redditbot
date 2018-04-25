# RedditBot

Um bot que envia para você as coisas mais interessantes do Reddit!

## Execução direto na linha de comando

Para executar direto no CLI chame o bot da seguinte forma:

`python3.6 -m crawlers.reddit_crawler`

Será questionado quais são os subreddits de interesse, bastando inserir eles separados por ; (ponto-e-virgula).

### Execução pelo Docker

Para executar o bot basta rodar o comando:
 
`docker run -e telegram-token='[TOKEN-TELEGRAM]' -it --rm --name bot lucaspolo/reddit-bot`
 
Ele irá buscar a imagem no registry e iniciará o container.
 
Para subir o container direto do Dockerfile é necessário primeiro realizar o build da imagem:
 
`docker build -t meu_bot .`
 
Depois deve-se iniciar o container-bot passando uma variável de ambiente chamada telegram-token com o Token do bot:
 
`docker run -e telegram-token='[SEU TOKEN]' -it --rm --name bot meu_bot`
 
### Execução do bot no terminal

Para executar o bot é necessário ter uma variável de ambiente com o Token do Telegram:

`telegram-token=[SEU TOKEN]`

Depois disso basta iniciar a execução do bot:

`python3.6 bot.py`

Os comandos do bot são 

- /start: Inicia o bot, recebendo uma mensagem de boas vindas.
- /nadaparafazer [subreddits]: Busca nos subreddits indicados as threads que estão bombando (upvotes > 5000).

Ex:

`/nadaparafazer dogs;askreddit`
