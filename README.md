# Desafios IDwall

# Para ver as instruções das resoluções role para baixo!

Aqui estão os desafios para a primeira fase de testes de candidatos da IDwall.  
Escolha em qual linguagem irá implementar (a não ser que um de nossos colaboradores lhe instrua a utilizar uma linguagem específica).  

Não há diferença de testes para diferentes níveis de profissionais, porém o teste será avaliado com diferentes critérios, dependendo do perfil da vaga.

1. [Manipulação de strings](https://github.com/idwall/desafios/tree/master/strings)
2. [Crawlers](https://github.com/idwall/desafios/tree/master/crawlers)

## Como entregar estes desafios
Você deve forkar este projeto e fazer o *push* no seu próprio repositório e enviar o link para _jobs@idwall.co_ ou para o email do recrutador, junto com seu LinkedIn atualizado.  

A implementação deve ficar na pasta correspondente ao desafio. Fique à vontade para adicionar qualquer tipo de conteúdo que julgue útil ao projeto, alterar/acrescentar um README com instruções de como executá-lo, etc.

**Obs.:** Você não deve fazer um Pull Request para este projeto! 

## Carreira IDwall

Caso queira mais detalhes de como trabalhamos, quais são nossos valores e ideais, confira a página [Carreira IDwall](https://idwall.co/carreira) e mesmo que seu perfil não esteja listado nas vagas em aberto, lhe encorajamos a mandar seu CV! Valorizamos bons profissionais sempre e gostamos de manter contato com gente boa.

Boas implementações! 🎉

## Resolução - Strings

Para chamar o teste do programa execute:

`python3.6 strings.text_slicer`

Ele irá imprimir duas vezes o texto, a primeira sem justificar e a segunda justificando. Caso seja passado um caminho de um arquivo de texto o mesmo será impresso reformatado:

Ex:

`python3.6 strings.text_slicer ~/meu_arquivo.txt`

## Resolução - Crawler e Bot

Para executar direto no CLI chame o bot da seguinte forma:

`python3.6 -m crawlers.reddit_crawler askreddit;dogs;gifs`

Será apresentada as informações sobre o tópico questionado.

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

 ### Execução pelo Docker
 
 Para executar o bot basta rodar o comando:
 
 `docker run -e telegram-token='[TOKEN-TELEGRAM]' -it --rm --name bot lucaspolo/reddit-bot`
 
 Ele irá buscar a imagem no registry e iniciará o container.
 
 Para subir o container direto do Dockerfile é necessário primeiro realizar o build da imagem:
 
 `docker build -t meu_bot .`
 
 Depois deve-se iniciar o container-bot passando uma variável de ambiente chamada telegram-token com o Token do bot:
 
 `docker run -e telegram-token='[SEU TOKEN]' -it --rm --name bot meu_bot`