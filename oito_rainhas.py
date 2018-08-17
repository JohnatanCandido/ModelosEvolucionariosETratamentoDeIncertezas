from random import random
from copy import copy

geracoes = []
TAM_GERACAO = 20
ponto_corte = None


class Tabuleiro:
    def __init__(self, geracao, genotipo):
        self.geracao = geracao
        self.genotipo = genotipo
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        fitness = 0
        for i in range(len(self.genotipo)):
            for j in range(i+1, len(self.genotipo)):
                if abs(self.genotipo[i] - self.genotipo[j]) == j-i:
                    fitness += 1
        return fitness


def main():
    solucao = encontra_solucao()
    if solucao == 'Não encontrado':
        geracao = geracoes[999]
        geracao.sort(key=lambda x: x.fitness)
        solucao = geracao[0]
    print(f'Geração: {solucao.geracao}, fitness: {solucao.calc_fitness()}')
    print('----------------------------------')
    for i in range(8):
        for j in range(8):
            print('|', end='')
            if j == solucao.genotipo[i]:
                print(' O ', end='')
            else:
                print('   ', end='')
        print('|')
        print('----------------------------------')


def encontra_solucao():
    num_geracao = 1
    for i in range(1000):
        print(i)
        if not geracoes:
            geracoes.append(cria_populacao_inicial())
        geracao = geracoes[i]
        for ind in geracao:
            if ind.fitness == 0:
                return ind
        geracao.sort(key=lambda x: x.fitness)
        num_geracao += 1
        nova_geracao = cruzar(copy(geracao)[:10], num_geracao)
        geracoes.append(nova_geracao)
        len(geracoes)
    return 'Não encontrado'


def cria_populacao_inicial():
    geracao = []
    for _ in range(TAM_GERACAO):
        individuo = []
        while len(individuo) < 8:
            linha = int(random()*8)
            if linha not in individuo:
                individuo.append(linha)
        geracao.append(Tabuleiro(1, individuo))
    return geracao


def cruzar(geracao, num_geracao):
    nao_cruzados = copy(geracao)
    while len(geracao) < TAM_GERACAO:
        i1 = -1
        i2 = -1
        while i1 == i2:
            i1 = int(random()*len(nao_cruzados))
            i2 = int(random()*len(nao_cruzados))
        pai1 = nao_cruzados[i1]
        pai2 = nao_cruzados[i2]
        nao_cruzados.remove(pai1)
        nao_cruzados.remove(pai2)
        global ponto_corte
        if ponto_corte is None:
            ponto_corte = int(random()*8)
        filho1 = pai1.genotipo[:ponto_corte]
        filho2 = pai2.genotipo[:ponto_corte]
        for j in range(8):
            if pai2.genotipo[j] not in filho1 and len(filho1) < 8:
                filho1.append(pai2.genotipo[j])
            if pai1.genotipo[j] not in filho2 and len(filho2) < 8:
                filho2.append(pai1.genotipo[j])
        geracao.append(Tabuleiro(num_geracao, filho1))
        geracao.append(Tabuleiro(num_geracao, filho2))
    return geracao


if __name__ == '__main__':
    main()
