class Elemento:
    def __init__(self, nome):
        self.nome = nome
        self.variaveis = {}


class Variavel:
    def __init__(self, nome, suporte, nucleo):
        self.nome = nome
        self.suporte = suporte
        self.nucleo = nucleo


regras = []
elementos = {}
resultado = '-'


def add_elemento(nome):
    elementos[nome] = Elemento(nome)


def remove_elemento(nome):
    del elementos[nome]


def add_variavel(elemento, nome, suporte, nucleo):
    elementos[elemento].variaveis[nome] = Variavel(nome, suporte.split(','), nucleo.split(','))


def calcular(valores, label_resultado):
    global resultado
    resultado = 42
    for val in valores:
        print(val)
    label_resultado.configure(text=resultado)
