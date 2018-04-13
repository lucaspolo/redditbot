import textwrap
import sys
from itertools import zip_longest


def text_slicer(text, largura):
    wraper = textwrap.TextWrapper(drop_whitespace=False, width=largura)
    wraped_texts = wraper.wrap(text)

    return [wraped_text.lstrip().replace("  ", "\n") for wraped_text in wraped_texts]


def justificar(linha, largura=40):
    palavras = linha.split(" ")
    total_caracteres = len(''.join(palavras))
    total_espacos = largura - total_caracteres
    separacoes = len(palavras) - 1

    if len(palavras) - 1 == separacoes:
        separacoes -= 1

    novos_espacos = [(" " * (total_espacos // separacoes))] * separacoes
    espacos_sobra = [" "] * (total_espacos % separacoes)

    nova_linha = ''
    none_to_space = lambda x: x if x else ''

    for p, e, s in zip_longest(palavras, novos_espacos, espacos_sobra):
        nova_linha += p + none_to_space(e) + none_to_space(s)

    return nova_linha


def limitar_texto(texto, largura=40, justifica=False):
    texto_fatiado = text_slicer(texto, largura)

    if justifica:
        texto_fatiado = [justificar(linha) for linha in texto_fatiado]

    texto_unido = str.join("\n", texto_fatiado)

    return texto_unido


if __name__ == "__main__":
    arquivo = 'texto_exemplo.txt'

    if len(sys.argv[1:]) == 1:
        arquivo = sys.argv[1]

    with open(sys.argv[1], "r") as file:
        texto = file.read()
        texto_fatiado = limitar_texto(texto)
        print(texto_fatiado)
        print("\n\n")
        texto_justificado = limitar_texto(texto, justifica=True)
        print(texto_justificado)
