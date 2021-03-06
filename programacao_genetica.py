from copy import deepcopy
from math import sqrt
from random import randint, random


MAX_INT = 99**9
pares = [[1, 0.67], [2, 2], [3, 4], [4, 6.67], [5, 10], [6, 14], [7, 18.67], [8, 24], [9, 30], [10, 36.67]]
# pares = [[i, eval('x*(x+1)/3'.replace('x', str(i)))] for i in range(1, 11)]
operadores = ['+', '-', '*', '/']
valores = ['x', '+', '-', '*', '/'] + [i + 1 for i in range(10)]

num_geracoes = 250
tam_geracao = 100
max_profundidade = 5
chance_mutacao = 0.5

melhores = []


class Geracao:
    def __init__(self, populacao, geracao):
        self.populacao = sorted(populacao, key=lambda x: x.fitness)
        self.geracao = geracao
        self.media_fitness = self.calc_media_fitness()
        self.melhor = self.populacao[0]
        melhores.append(self.populacao[0])

    def calc_media_fitness(self):
        return self.calc_fitness_total() / len(self.populacao)

    def calc_fitness_total(self):
        fitness = 0
        for ind in self.populacao:
            fitness += ind.fitness
        return fitness

    def __str__(self):
        return f'{self.geracao} ' \
               f'- Média: {str(self.media_fitness)[:5] if self.media_fitness < MAX_INT else 999999} ' \
               f'- Melhor: {str(self.melhor.fitness)[:6]} - ({self.melhor.funcao}) ' \
               f'- Pior: {str(self.populacao[-1].fitness)[:7]} - ({self.populacao[-1].funcao}) ' \
               f'- Tamanho: {len(self.populacao)}'


class Node:
    def __init__(self, valor, raiz, profundidade, geracao=-1):
        self.valor = valor if profundidade <= max_profundidade else valores[randint(5, len(valores) - 1)]
        self.raiz = raiz
        self.profundidade = profundidade
        if self.valor in operadores:
            self.left = Node(valores[randint(0, len(valores)-1)], False, profundidade + 1)
            self.right = Node(valores[randint(0, len(valores)-1)], False, profundidade + 1)
        if self.raiz:
            self.geracao = geracao
            self.funcao = cria_funcao(self)
            self.lista = self.cria_lista_nos([])
            self.fitness = -1
            self.calc_fitness()
            self.exp_vida = int(max(-0.15*self.fitness+20, 1))

    def __deepcopy__(self, memodict={}):
        copy_object = Node(self.valor, self.raiz, self.profundidade)
        if self.valor in operadores:
            copy_object.left = deepcopy(self.left)
            copy_object.right = deepcopy(self.right)
        return copy_object

    def __str__(self):
        return 'Função: ' + self.funcao + \
               '\nFitness: ' + str(self.fitness)[:6] + \
               ' - Profundidade: ' + str(calc_prof(self)) + \
               '\nGeração: ' + str(self.geracao)

    def cria_lista_nos(self, lista):
        if not self.raiz or self.profundidade < max_profundidade:
            try:
                if self.valor in operadores:
                    lista_esquerda = self.left.cria_lista_nos(lista)
                    lista_direita = self.right.cria_lista_nos(lista)
                    if lista_esquerda == -1 or lista_direita == -1:
                        return -1
                    lista += lista_esquerda
                    lista += lista_direita
                lista.append(self)
                return lista
            except MemoryError:
                return -1
        return []

    def refresh(self):
        self.lista = self.cria_lista_nos([])
        self.funcao = cria_funcao(self)
        self.calc_fitness()
        return self

    def calc_fitness(self):
        fitness = 0
        for par in pares:
            try:
                r = eval(self.funcao.replace('x', str(par[0])))
            except ZeroDivisionError:
                r = MAX_INT
            fitness += (par[1] - r)**2
        self.fitness = sqrt(fitness)
        return self.fitness

    def morreu(self, ger_atual):
        return self.geracao + self.exp_vida < ger_atual


def cria_populacao(ger):
    populacao = []
    for _ in range(tam_geracao):
        raiz = Node(operadores[randint(0, 3)], True, 1, ger)
        # if calc_prof(raiz) < max_profundidade and raiz.lista and raiz.fitness < MAX_INT:
        if raiz.lista and raiz.fitness < MAX_INT:
            populacao.append(raiz)
    return populacao


def gera_nova_geracao(geracao, num_ger):
    # Dos que passam na roleta, tira aqueles cuja expectativa de vida + geração incial é menor que a geração atual
    nova_populacao = [ind for ind in executa_roleta(geracao) if not ind.morreu(num_ger)]
    return cruzar_populacao(nova_populacao, num_ger)


def executa_roleta(geracao):
    geracao.populacao = [ind for ind in geracao.populacao if ind.fitness < MAX_INT*0.8]
    total = geracao.calc_fitness_total()
    soma = 0
    roleta = []
    tam_desejado = len(geracao.populacao) * 0.75
    if len(geracao.populacao) > tam_geracao * 5:
        tam_desejado = len(geracao.populacao) * 0.2
    nova_populacao = geracao.populacao[:]
    for ind in nova_populacao:
        roleta.append([ind, soma, ind.fitness / total + soma])
        soma += ind.fitness / total
    while len(nova_populacao) > tam_desejado:
        numero = random()
        for r in roleta:
            if r[1] <= numero <= r[2]:
                nova_populacao.remove(r[0])
                roleta.remove(r)
                break
    return nova_populacao


def cruzar_populacao(populacao, num_ger):
    nao_cruzados = populacao[:]
    max_cruzamento = len(nao_cruzados) * 0.5
    while len(nao_cruzados) > max_cruzamento:
        pai = nao_cruzados.pop(randint(0, len(nao_cruzados) - 1))
        mae = nao_cruzados.pop(randint(0, len(nao_cruzados) - 1))

        populacao += cruzar_individuos(pai, mae, num_ger)
    print('')
    return Geracao(populacao, num_ger)


def cruzar_individuos(pai, mae, ger):
    filho_1 = deepcopy(pai)
    filho_2 = deepcopy(mae)

    filho_1.refresh()
    filho_2.refresh()

    gene_1 = [i for i in filho_1.lista if not i.raiz][randint(0, len(filho_1.lista) - 2)]
    gene_2 = [i for i in filho_2.lista if not i.raiz][randint(0, len(filho_2.lista) - 2)]

    raiz_1 = [r for r in filho_1.lista if r.valor in operadores and gene_1 in[r.left, r.right]][0]
    raiz_2 = [r for r in filho_2.lista if r.valor in operadores and gene_2 in[r.left, r.right]][0]

    if raiz_2.left == gene_2:
        raiz_2.left = gene_1
    elif raiz_2.right == gene_2:
        raiz_2.right = gene_1
    else:
        raise AssertionError('Isso não deveria ter acontecido')

    if raiz_1.left == gene_1:
        raiz_1.left = gene_2
    elif raiz_1.right == gene_1:
        raiz_1.right = gene_2
    else:
        raise AssertionError('Isso não deveria ter acontecido')

    retorno = []
    filho_1 = mutar(filho_1.refresh(), ger)
    filho_2 = mutar(filho_2.refresh(), ger)
    # if filho_1 is not None and filho_1.lista and filho_1.fitness < MAX_INT:
    if filho_1 is not None and calc_prof(filho_1) < max_profundidade and filho_1.lista and filho_1.fitness < MAX_INT:
        retorno.append(filho_1)
    # if filho_2 is not None and filho_2.lista and filho_2.fitness < MAX_INT:
    if filho_2 is not None and calc_prof(filho_2) < max_profundidade and filho_2.lista and filho_2.fitness < MAX_INT:
        retorno.append(filho_2)

    return retorno


def mutar(ind, ger):
    if ind.lista == -1:
        return None
    if random() < chance_mutacao:
        print('.', end='')
        remover = [i for i in ind.lista if not i.raiz][randint(0, len(ind.lista) - 2)]
        raiz = [r for r in ind.lista if r.valor in operadores and remover in[r.left, r.right]][0]
        if raiz.left == remover:
            raiz.left = Node(valores[randint(0, len(valores)-1)], False, raiz.profundidade + 1)
        elif raiz.right == remover:
            raiz.right = Node(valores[randint(0, len(valores) - 1)], False, raiz.profundidade + 1)
        else:
            raise AssertionError('Isso não deveria ter acontecido')
        del remover
    ind.geracao = ger
    ind.refresh()
    return ind


def calc_prof(node, left=1, right=1):
    if node.valor in operadores:
        left += calc_prof(node.left)
        right += calc_prof(node.right)
    return left if left > right else right


def cria_funcao(node, parenteses=False, funcao=''):
    if node.valor in operadores:
        funcao += cria_funcao(node.left, node.valor in['*', '/'] and node.left.valor in ['+', '-'], funcao)
    funcao += str(node.valor)
    if node.valor in operadores:
        funcao += cria_funcao(node.right, node.valor in['*', '/'] and node.right.valor in ['+', '-'])
    if parenteses:
        funcao = '(' + funcao + ')'
    return str(funcao)


def main(num_ger, tam_ger, max_prof, chan_mut):
    global num_geracoes, tam_geracao, max_profundidade, chance_mutacao
    num_geracoes = int(num_ger)
    tam_geracao = int(tam_ger)
    max_profundidade = int(max_prof)
    chance_mutacao = float(chan_mut)

    melhores.clear()
    geracao = None
    try:
        for i in range(num_geracoes):
            if geracao is None:
                populacao = cria_populacao(i+1)
                geracao = Geracao(populacao, i+1)
            else:
                geracao = gera_nova_geracao(geracao, i+1)
            if geracao.melhor.fitness < 0.01:
                return geracao.melhor
            print(str(geracao))
    except MemoryError:
        print('\n\n>>> MEMORY ERROR <<<\n\n')

    return sorted(melhores, key=lambda x: x.fitness)[0]


if __name__ == '__main__':
    pass
