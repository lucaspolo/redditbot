import textwrap
import sys
from itertools import zip_longest


def text_slicer(texto, largura):
    """Divide o texto sem quebrar as palavras

    :param text: Texto para ser divido
    :param largura: largura máxima
    :return: o texto reformatado com a largura limitada
    """
    wraper = textwrap.TextWrapper(drop_whitespace=False, width=largura)
    wraped_texts = wraper.wrap(texto)

    return [wraped_text.lstrip().replace("  ", "\n") for wraped_text in wraped_texts]


def justificar(linha, largura=40):
    """Justifica a linha redistribuindo os espaços até atingir a largura

    TODO Ajustar quando há quebra de linha

    >>> justificar("Batata doce doc")
    'Batata              doce             doc'

    :param linha: linha a ser justificada
    :param largura: largura máxima
    :return: linha justificada de acordo com a largura
    """
    palavras = linha.split(" ")
    total_caracteres = len(''.join(palavras))
    total_espacos = largura - total_caracteres
    separacoes = len(palavras) - 1

    if len(palavras) == separacoes:
        separacoes -= 1

    if palavras[-1] == "\n":
        separacoes -= 1

    novos_espacos = [(" " * (total_espacos // separacoes))] * separacoes
    espacos_sobra = [" "] * (total_espacos % separacoes)

    nova_linha = ''
    none_to_space = lambda x: x if x else ''

    for p, e, s in zip_longest(palavras, novos_espacos, espacos_sobra):
        nova_linha += p + none_to_space(e) + none_to_space(s)

    return nova_linha


def limitar_texto(texto, largura=40, justifica=False):
    """Limita cada linha do texto de acordo com largura

    :param texto: texto a ser limitado
    :param largura: largura máxima do texto
    :param justifica: caso True justifica o texto de acordo com a largura
    :return: texto com a largura limitada
    """
    texto_fatiado = text_slicer(texto, largura)

    if justifica:
        texto_fatiado = [justificar(linha) for linha in texto_fatiado]

    texto_unido = str.join("\n", texto_fatiado)

    return texto_unido


if __name__ == "__main__":
    arquivo = 'texto_exemplo.txt'

    if len(sys.argv[1:]) == 1:
        arquivo = sys.argv[1]

    with open(arquivo, "r") as file:
        texto = file.read()
        texto_fatiado = limitar_texto(texto)
        print(texto_fatiado)
        print("\n\n")
        texto_justificado = limitar_texto(texto, justifica=True)
        print(texto_justificado)
