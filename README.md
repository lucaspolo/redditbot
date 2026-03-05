# RedditBot

Um bot que envia para você as coisas mais interessantes do Reddit!

## Execução direto na linha de comando

Para executar direto no CLI chame o bot da seguinte forma:

`python -m redditbot.ui.nadaparafazer -s "dogs;python" {-m VOTOS_MINIMOS}`

Caso necessário, para verificar quais os comandos disponíveis e seus valores padrões, digite:

`python -m redditbot.ui.nadaparafazer --help`

## Execução do Bot

O bot do Telegram aceita os seguintes comandos:

```
/start: inicia a conversa respodendo com uma mensagem de boas vindas.
/nadaparafazer (ou /n) [TÓPICOS SEPARADOS POR ESPAÇO]: procura e responde com os tópicos mais votados
```

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


### docker-compose

Para executar o projeto com o docker-compose basta executar o seguinte exemplo, lembrando de alterar o token do Telegram:

```yaml
version: "3"
services:
  redditbot:
  	image: lucaspolo/redditbot:latest
  restart: always
  environment:
  	TELEGRAM_TOKEN=$YOUR_TELEGRAM_TOKEN  # PLEASE PAY ATTENTION HERE
```

### Kubernetes

Para publicar a aplicação como um deployment no Kubernetes você pode usar o seguinte:

Primeiro crie uma secret para armazenar o token do Telegram:

```bash
kubectl create configmap redditbot-config --from-literal=telegram-token=$TELEGRAM_TOKEN
```

Com isso já é possível aplicar o deployment:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redditbot-deployment
  labels:
    app: redditbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redditbot
  template:
    metadata:
      labels:
        app: redditbot
    spec:
      containers:
        - name: redditbot
          image: lucaspolo/redditbot
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
          env:
            - name: TELEGRAM_TOKEN
              valueFrom:
                configMapKeyRef:
                  name: redditbot-config
                  key: telegram-token

## Como Contribuir

Este projeto está configurado para ser desenvolvido no **GitHub Codespaces**. Isso significa que você pode configurar um ambiente de desenvolvimento completo diretamente no seu navegador ou no VS Code local com apenas um clique.

Você pode usar o Codespaces para:
- **Desenvolver**: O ambiente já vem com todas as dependências instaladas (`uv`, `python`, etc).
- **Testar**: Execute `make test` para rodar a suíte de testes.
- **Alterar**: Modifique o código e veja as mudanças em tempo real.

Para mais detalhes sobre padrões de código, linting e testes, consulte o arquivo [AGENTS.md](AGENTS.md).
```
