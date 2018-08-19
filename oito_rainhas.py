from random import random
from copy import copy
from tkinter import *

master = Tk()

geracoes = []
TAM_GERACAO = 20
QT_GERACOES = 100
ponto_corte = None
TOTAL_TENTATIVAS = 0
TOTAL_MUTACOES = 0
board = Canvas(master, width=599, height=599)


class Geracao:
    def __init__(self, num, populacao):
        self.num = num
        self.populacao = populacao

    def busca_melhor_individuo(self):
        melhor = None
        for ind in self.populacao:
            if melhor is None or melhor.calc_fitness() > ind.calc_fitness():
                melhor = ind
        return melhor


class Tabuleiro:
    def __init__(self, genotipo):
        self.genotipo = genotipo

    def calc_fitness(self):
        fitness = 0
        for i in range(len(self.genotipo)):
            for j in range(i + 1, len(self.genotipo)):
                if abs(self.genotipo[i] - self.genotipo[j]) == j - i:
                    fitness += 1
        return fitness


def main():
    geracao, solucao, encontrou = encontra_solucao()
    if not encontrou:
        print('### Não encontrado! ###')
    print(f'Geração: {geracao}, fitness: {solucao.calc_fitness()}')
    print(f'\n\nTOTAL TENTATIVAS: {TOTAL_TENTATIVAS}')
    print(f'TOTAL MUTAÇÕES: {TOTAL_MUTACOES} ({str(TOTAL_MUTACOES/TOTAL_TENTATIVAS*100)[:5]}%)')
    mostrar_solucao(solucao.genotipo)


def encontra_solucao():
    for i in range(QT_GERACOES):
        if not geracoes:
            geracoes.append(cria_populacao_inicial())
        geracao = geracoes[i]
        for ind in geracao.populacao:
            if ind.calc_fitness() == 0:
                return geracao.num, ind, True
        geracao.populacao.sort(key=lambda x: x.calc_fitness())
        nova_geracao = cruzar(copy(geracao.populacao)[:10])
        geracoes.append(Geracao(i + 2, nova_geracao))
    ger, sol, e = busca_melhor_solucao()
    return ger, sol, e


def cria_populacao_inicial():
    geracao = []
    for _ in range(TAM_GERACAO):
        individuo = []
        while len(individuo) < 8:
            linha = int(random() * 8)
            if linha not in individuo:
                individuo.append(linha)
        global TOTAL_TENTATIVAS
        TOTAL_TENTATIVAS += 1
        geracao.append(Tabuleiro(individuo))
    return Geracao(1, geracao)


def cruzar(geracao):
    nao_cruzados = copy(geracao)
    while len(geracao) < TAM_GERACAO:
        i1 = -1
        i2 = -1
        while i1 == i2:
            i1 = int(random() * len(nao_cruzados))
            i2 = int(random() * len(nao_cruzados))
        pai1 = nao_cruzados[i1]
        pai2 = nao_cruzados[i2]
        nao_cruzados.remove(pai1)
        nao_cruzados.remove(pai2)
        global ponto_corte
        if ponto_corte is None:
            ponto_corte = int(random() * 8)
        filho1 = pai1.genotipo[:ponto_corte]
        filho2 = pai2.genotipo[:ponto_corte]
        for j in range(8):
            if pai2.genotipo[j] not in filho1 and len(filho1) < 8:
                filho1.append(pai2.genotipo[j])
            if pai1.genotipo[j] not in filho2 and len(filho2) < 8:
                filho2.append(pai1.genotipo[j])
        geracao.append(mutar(Tabuleiro(filho1)))
        geracao.append(mutar(Tabuleiro(filho2)))
    return geracao


def mutar(tabuleiro):
    global TOTAL_TENTATIVAS, TOTAL_MUTACOES
    TOTAL_TENTATIVAS += 1
    genotipo = tabuleiro.genotipo
    if random() > 0.98:
        TOTAL_MUTACOES += 1
        gene1 = int(random() * 7)
        gene2 = int(random() * 7)
        placeholder = genotipo[gene1]
        genotipo[gene1] = genotipo[gene2]
        genotipo[gene2] = placeholder
    return tabuleiro


def busca_melhor_solucao():
    melhor = None
    ger = -1
    for geracao in geracoes:
        melhor_da_geracao = geracao.busca_melhor_individuo()
        if melhor is None:
            ger = geracao.num
            melhor = melhor_da_geracao
        elif melhor.calc_fitness() > melhor_da_geracao.calc_fitness():
            ger = geracao.num
            melhor = melhor_da_geracao
    return ger, melhor, False


board.grid(row=0, column=0)


def mostrar_solucao(genoma):
    for i in range(8):
        for j in range(8):
            cor = "white" if (i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1) else "light gray"
            board.create_rectangle(i * 75 + 2, j * 75 + 2, i * 75 + 75, j * 75 + 75, fill=cor, width=1)
            if genoma[i] == j:
                board.create_oval(i * 75 + 2, j * 75 + 2, i * 75 + 75, j * 75 + 75, fill="red", width=1)
    master.mainloop()


if __name__ == '__main__':
    main()
