import textwrap


def text_slicer(text, width):
    wraper = textwrap.TextWrapper(drop_whitespace=False, width=width)
    wraped_texts = wraper.wrap(text)

    return [wraped_text.lstrip().replace("  ", "\n") for wraped_text in wraped_texts]


def limitar_texto(texto, width=40):
    texto_fatiado = text_slicer(texto, width)
    texto_unido = str.join("\n", texto_fatiado)

    return texto_unido


if __name__ == "__main__":
    with open("texto_exemplo.txt", "r") as file:
        texto = file.read()
        texto_fatiado = limitar_texto(texto)
        print(texto_fatiado)