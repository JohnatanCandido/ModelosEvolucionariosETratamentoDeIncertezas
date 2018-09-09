from copy import deepcopy
from math import sqrt
from random import randint, random


MAX_INT = 99**9
pares = [[1, 0.67], [2, 2], [3, 4], [4, 6.67], [5, 10], [6, 14], [7, 18.67], [8, 24], [9, 30], [10, 36.67]]
operadores = ['+', '-', '*', '/']
valores = ['x', '+', '-', '*', '/', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

num_geracoes = 250
tam_geracao = 100
max_profundidade = 5
chance_mutacao = 0.5


class Geracao:
    def __init__(self, populacao, geracao):
        self.populacao = sorted(populacao, key=lambda x: x.fitness)
        self.geracao = geracao
        self.media_fitness = self.calc_media_fitness()
        self.melhor = self.populacao[0]

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
            self.left = Node(valores[randint(0, len(valores)-1)], self, profundidade + 1)
            self.right = Node(valores[randint(0, len(valores)-1)], self, profundidade + 1)
            if self.left.raiz != self or self.right.raiz != self:
                raise AssertionError('Q merda velho')
        if self.raiz is None:
            self.geracao = geracao
            self.funcao = cria_funcao(self)
            self.lista = self.cria_lista_nos([])
            if self in self.lista:
                self.lista.remove(self)
            self.fitness = -1
            self.calc_fitness()
            self.exp_vida = 5  # TODO Criar uma função de expectativa de vida

    def __str__(self):
        return 'Função: ' + self.funcao + \
               '\nFitness: ' + str(self.fitness)[:6] + \
               ' - Profundidade: ' + str(calc_prof(self)) + \
               '\nGeração: ' + str(self.geracao)

    def refaz_raizes(self, raiz):
        self.raiz = raiz
        if self.valor in operadores:
            self.left.refaz_raizes(self)
            self.right.refaz_raizes(self)

    def cria_lista_nos(self, lista):
        if self.raiz is not None or self.profundidade < max_profundidade:
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
        self.refaz_raizes(None)
        self.lista = self.cria_lista_nos([])
        if self.lista != -1:
            self.lista.remove(self)
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
        raiz = Node(operadores[randint(0, 3)], None, ger)
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
    max_cruzamento = len(nao_cruzados) * 0.20
    while len(nao_cruzados) > max_cruzamento:
        pai = nao_cruzados.pop(randint(0, len(nao_cruzados) - 1))
        mae = nao_cruzados.pop(randint(0, len(nao_cruzados) - 1))

        populacao += cruzar_individuos(pai, mae, num_ger)
    print('')
    return Geracao(populacao, num_ger)


def cruzar_individuos(pai, mae, ger):
    filho_1 = deepcopy(pai)
    filho_2 = deepcopy(mae)

    gene_1 = filho_1.lista[randint(0, len(filho_1.lista) - 1)]
    gene_2 = filho_2.lista[randint(0, len(filho_2.lista) - 1)]

    raiz_1 = gene_1.raiz
    raiz_2 = gene_2.raiz

    if raiz_2.left == gene_2:
        gene_2.raiz.left = gene_1
    elif raiz_2.right == gene_2:
        gene_2.raiz.right = gene_1
    else:
        raise AssertionError('Isso não deveria ter acontecido')

    if raiz_1.left == gene_1:
        gene_1.raiz.left = gene_2
    elif raiz_1.right == gene_1:
        gene_1.raiz.right = gene_2
    else:
        raise AssertionError('Isso não deveria ter acontecido')

    gene_1.raiz = raiz_2
    gene_2.raiz = raiz_1

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
        remover = ind.lista[randint(0, len(ind.lista) - 1)]
        raiz = remover.raiz
        if raiz.left == remover:
            raiz.left = Node(valores[randint(0, len(valores)-1)], raiz, raiz.profundidade + 1)
        elif raiz.right == remover:
            raiz.right = Node(valores[randint(0, len(valores) - 1)], raiz, raiz.profundidade + 1)
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


def cria_funcao(node, funcao=''):
    if node.valor in operadores:
        funcao += cria_funcao(node.left, funcao)
    funcao += str(node.valor)
    if node.valor in operadores:
        funcao += cria_funcao(node.right)
    if node.valor in['+', '-'] and node.raiz is not None and node.raiz.valor in['*', '/']:
        funcao = '(' + funcao + ')'
    return str(funcao)


def main(num_ger, tam_ger, max_prof, chan_mut):
    global num_geracoes, tam_geracao, max_profundidade, chance_mutacao
    num_geracoes = int(num_ger)
    tam_geracao = int(tam_ger)
    max_profundidade = int(max_prof)
    chance_mutacao = float(chan_mut)

    geracoes = []
    try:
        for i in range(num_geracoes):
            if not geracoes:
                populacao = cria_populacao(i+1)
                geracoes.append(Geracao(populacao, i+1))
            else:
                geracoes.append(gera_nova_geracao(geracoes[-1], i+1))
            if geracoes[-1].melhor.fitness == 0:
                break
            print(str(geracoes[-1]))
    except MemoryError:
        print('\n\n>>> MEMORY ERROR <<<\n\n')

    return sorted(geracoes, key=lambda x: x.melhor.fitness)[0].melhor


if __name__ == '__main__':
    pass
