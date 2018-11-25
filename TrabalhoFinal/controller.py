class Elemento:
    def __init__(self, nome):
        self.nome = nome
        self.variaveis = {}

    def calcula_resultado(self, x):
        var, pert = '', 0
        for variavel in self.variaveis:
            p = self.variaveis[variavel].retorna_pertinencia(x)
            if pert < p:
                var = variavel
                pert = p
        return var, pert


class Variavel:
    def __init__(self, nome, suporte, nucleo):
        self.nome = nome
        self.suporte = [float(s) for s in suporte]
        self.nucleo = [float(n) for n in nucleo]
        self.pertinencia = 0

    def calcula_pertinencia(self, x):
        self.pertinencia = self.retorna_pertinencia(x)

    def retorna_pertinencia(self, x):
        if self.nucleo[0] <= x <= self.nucleo[1]:
            return 1
        elif self.suporte[0] <= x <= self.nucleo[0]:
            return (x - self.suporte[0]) / (self.nucleo[0] - self.suporte[0])
        elif self.nucleo[1] <= x <= self.suporte[1]:
            return (self.suporte[1] - x) / (self.suporte[1] - self.nucleo[1])
        else:
            return 0


regras = []
elementos = {}


def add_elemento(nome):
    elementos[nome] = Elemento(nome)


def remove_elemento(nome):
    del elementos[nome]


def add_variavel(elemento, nome, suporte, nucleo):
    elementos[elemento].variaveis[nome] = Variavel(nome, suporte.split(','), nucleo.split(','))


def calcular(valores, label_resultado):
    resultado = ''
    for elem in valores:
        if valores[elem].get() == '':
            return
        elif valores[elem].get() == 'r':
            resultado = elem
        elif valores[elem].get() != 'r':
            for var in elementos[elem].variaveis:
                elementos[elem].variaveis[var].calcula_pertinencia(float(valores[elem].get()))

    regras_tratadas = {}
    valores = {}
    divisor = 0
    for reg in regras:
        if ' e ' in reg[0]:
            regra_tratada = []
            regra = reg[0].split(' e ')
            for r in regra:
                r1 = r.split(' é ')
                regra_tratada.append(elementos[r1[0]].variaveis[r1[1]].pertinencia)
            res = reg[1].split(' é ')[1]
            if res not in regras_tratadas or regras_tratadas[res] < min(regra_tratada):
                regras_tratadas[res] = min(regra_tratada)
        if ' ou ' in reg[0]:
            regra_tratada = []
            regra = reg[0].split(' ou ')
            for r in regra:
                r1 = r.split(' é ')
                regra_tratada.append(elementos[r1[0]].variaveis[r1[1]].pertinencia)
            res = reg[1].split(' é ')[1]
            if res not in regras_tratadas or regras_tratadas[res] < max(regra_tratada):
                regras_tratadas[res] = max(regra_tratada)

    minimo = int(min([elementos[resultado].variaveis[v].suporte[0] for v in elementos[resultado].variaveis]))
    maximo = int(max([elementos[resultado].variaveis[v].suporte[1] for v in elementos[resultado].variaveis]))

    for i in range(minimo, maximo+1):
        valor_i = -1
        for var in elementos[resultado].variaveis:
            variavel = elementos[resultado].variaveis[var]
            if variavel.suporte[0] <= i <= variavel.suporte[1] \
                    and valor_i < regras_tratadas[var] <= elementos[resultado].variaveis[var].retorna_pertinencia(i):
                valor_i = regras_tratadas[var]
        if valor_i > 0:
            if valor_i not in valores:
                valores[valor_i] = []
            valores[valor_i].append(i)
            divisor += valor_i

    dividendo = 0
    for valor in valores:
        soma = 0
        for n in valores[valor]:
            soma += n
        dividendo += (soma*valor)
    x = dividendo / divisor

    variavel, pertinencia = elementos[resultado].calcula_resultado(x)

    label_resultado.configure(text=variavel + ': ' + str(pertinencia)[:5] + ' (' + str(x)[:5] + ')')
