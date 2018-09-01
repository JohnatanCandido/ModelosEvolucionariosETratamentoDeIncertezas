from random import randint, random, shuffle
from math import sqrt
from tkinter import Tk, Canvas, W

master = Tk()

geracao_atual = 0
geracoes = []
TAM_GERACAO_INICIAL = 100
NUMERO_GERACOES = 30
CHANCE_MUTAR = 0.02
MAX_FITNESS = 63 ** 2
mutacoes = [0 for _ in range(NUMERO_GERACOES)]

matriz_numeros = [
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]
]

MOVIMENTOS_VALIDOS = [
    (-2, 1),
    (-2, -1),
    (-1, -2),
    (-1, 2),
    (2, -1),
    (2, 1),
    (1, 2),
    (1, -2)
]


class Individuo:
    def __init__(self, geracao, matriz):
        self.geracao = geracao
        self.matriz = matriz
        self.genotipo = self.cria_genotipo()
        self.maior_seq = [-1, -1, 0]
        self.fitness = self.calc_fitness()
        self.exp_vida = int(self.fitness/350)

    def cria_genotipo(self):
        vetor = []
        for i in range(1, 65):
            i, j = self.encontra_numero(i)
            vetor.append(matriz_numeros[i][j])
        return vetor

    def calc_fitness(self):
        fitness = 0
        tam_seq = 0
        inicial = 1
        for n in range(1, 65):
            if self._possui_movimento_valido(n):
                tam_seq += 1
            else:
                if tam_seq > self.maior_seq[2]:
                    self.maior_seq = [inicial, n - 1, tam_seq]
                inicial = n
                fitness += (tam_seq - 1) ** 2
                tam_seq = 0
        return fitness

    def _possui_movimento_valido(self, n):
        i, j = self.encontra_numero(n)
        proximo = n + 1
        for m in MOVIMENTOS_VALIDOS:
            if -1 < i + m[0] < 8 and -1 < j + m[1] < 8:
                if self.matriz[i + m[0]][j + m[1]] == proximo:
                    return True
        return False

    def encontra_numero(self, n):
        for i in range(8):
            for j in range(8):
                if self.matriz[i][j] == n:
                    return i, j

    def morreu(self):
        return self.geracao + self.exp_vida < geracao_atual


class Geracao:
    def __init__(self, populacao, geracao):
        self.populacao = populacao
        self.geracao = geracao
        self.media_de_fitness = 0

    def calc_fitness_total(self):
        total = 0
        for ind in self.populacao:
            total += ind.calc_fitness()
        return total

    def busca_solucao(self):
        for ind in self.populacao:
            if ind.fitness == MAX_FITNESS:
                return ind
        return None

    def calcula_media_fitness(self):
        self.media_de_fitness = self.calc_fitness_total() / len(self.populacao)


def encontra_solucao():
    global geracao_atual
    for geracao_atual in range(1, NUMERO_GERACOES + 1):
        if not geracoes:
            geracoes.append(gera_populacao(TAM_GERACAO_INICIAL))
            geracoes[geracao_atual - 1].calcula_media_fitness()
        else:
            geracoes.append(gera_nova_geracao(geracoes[geracao_atual - 2]))
            geracoes[geracao_atual - 1].populacao.sort(key=lambda x: x.fitness, reverse=True)
            if len(geracoes[geracao_atual - 1].populacao) < TAM_GERACAO_INICIAL:
                geracoes[geracao_atual - 1].populacao += gera_populacao(TAM_GERACAO_INICIAL, True)
            geracoes[geracao_atual - 1].calcula_media_fitness()
            solucao = geracoes[geracao_atual - 1].busca_solucao()
            if solucao is not None:
                return solucao
        print(f'{geracao_atual} - {len(geracoes[geracao_atual-1].populacao)} '
              f'- Média: {sqrt(geracoes[geracao_atual-1].media_de_fitness)} - Mutações: {mutacoes[geracao_atual-1]}')
    return None


def gera_populacao(qt, adding=False):
    populacao = []
    for _ in range(qt):
        populacao.append(gera_individuo())
    if adding:
        print('.')
        return populacao
    return Geracao(populacao, geracao_atual)


def gera_individuo():
    matriz = [[0 for _ in range(8)] for _ in range(8)]
    i, j = randint(0, 7), randint(0, 7)
    n = 1
    matriz[i][j] = n

    while n < 64:
        n += 1
        movimentos = MOVIMENTOS_VALIDOS
        shuffle(movimentos)
        shuffle(movimentos)
        for mov in movimentos:
            if -1 < i + mov[0] < 8 and -1 < j + mov[1] < 8:
                if matriz[i + mov[0]][j + mov[1]] == 0:
                    matriz[i + mov[0]][j + mov[1]] = n
                    i += mov[0]
                    j += mov[1]
                    break
        else:
            while True:
                i, j = randint(0, 7), randint(0, 7)
                if matriz[i][j] == 0:
                    matriz[i][j] = n
                    break

    '''
    while n < 64:
        n += 1
        movimentos = []
        for mov in MOVIMENTOS_VALIDOS:
            if -1 < i + mov[0] < 8 and -1 < j + mov[1] < 8:
                if matriz[i + mov[0]][j + mov[1]] == 0:
                    ni = i + mov[0]
                    nj = j + mov[1]
                    movimentos.append([ni, nj, calcula_adjacencias_validas(matriz, ni, nj)])
        if movimentos:
            movimentos.sort(key=lambda x: x[2], reverse=True)
            m = movimentos[0]
            matriz[m[0]][m[1]] = n
            i = m[0]
            j = m[1]
        else:
            while True:
                i, j = randint(0, 7), randint(0, 7)
                if matriz[i][j] == 0:
                    matriz[i][j] = n
                    break
'''
    return Individuo(geracao_atual, matriz)


def calcula_adjacencias_validas(matriz, i, j):
    total = 0
    for m in MOVIMENTOS_VALIDOS:
        if -1 < i + m[0] < 8 and -1 < j + m[1] < 8:
            if matriz[i + m[0]][j + m[1]] == 0:
                total += 1
    return total


def gera_nova_geracao(geracao):
    nova_geracao = executa_roleta(Geracao(geracao.populacao[:], geracao_atual))
    for ind in nova_geracao.populacao:
        if ind.morreu():
            nova_geracao.populacao.remove(ind)
    return cruzar(nova_geracao)


def cruzar(geracao):
    tam_inicial = len(geracao.populacao)
    nao_cruzado = geracao.populacao[:]
    while len(nao_cruzado) > tam_inicial * 0.30:
        pai_1 = nao_cruzado.pop(randint(0, len(nao_cruzado) - 1))
        pai_2 = nao_cruzado.pop(randint(0, len(nao_cruzado) - 1))
        filho_1 = [0 for _ in range(64)]
        filho_2 = [0 for _ in range(64)]
        for i in range(pai_1.maior_seq[0]-1, pai_1.maior_seq[1]):
            filho_1[i] = pai_1.genotipo[i]
        for i in range(pai_2.maior_seq[0]-1, pai_2.maior_seq[1]):
            filho_2[i] = pai_2.genotipo[i]
        for i in range(64):
            for j in range(64):
                if filho_1[j] == 0 and pai_2.genotipo[i] not in filho_1:
                    filho_1[j] = pai_2.genotipo[i]
                if filho_2[j] == 0 and pai_1.genotipo[i] not in filho_2:
                    filho_2[j] = pai_1.genotipo[i]
        filho_1 = converte_genotipo_matriz(filho_1)
        filho_2 = converte_genotipo_matriz(filho_2)
        geracao.populacao.append(mutar(filho_1, geracao.geracao))
        geracao.populacao.append(mutar(filho_2, geracao.geracao))
    return geracao


def converte_genotipo_matriz(genotipo):
    matriz = [[0 for _ in range(8)] for _ in range(8)]
    for n in range(64):
        i, j = encontra_coords(genotipo[n])
        matriz[i][j] = n + 1
    return matriz


def encontra_coords(n):
    for i in range(8):
        for j in range(8):
            if matriz_numeros[i][j] == n:
                return i, j


def mutar(matriz, num_ger):
    individuo = Individuo(num_ger, matriz)
    if geracoes[geracao_atual - 3].media_de_fitness < geracoes[geracao_atual - 2].media_de_fitness:
        chance_mutacao = CHANCE_MUTAR
    else:
        chance_mutacao = CHANCE_MUTAR * 3
    if random() <= chance_mutacao:
        mutacoes[geracao_atual - 1] += 1
        for _ in range(randint(1, 20)):
            while True:
                gene1 = [randint(0, 7), randint(0, 7)]
                gene2 = [randint(0, 7), randint(0, 7)]
                if gene1 != gene2:
                    m1 = individuo._possui_movimento_valido(individuo.matriz[gene1[0]][gene1[1]])
                    m2 = individuo._possui_movimento_valido(individuo.matriz[gene2[0]][gene2[1]])
                    if not m1 and not m2:
                        break
            placeholder = individuo.matriz[gene1[0]][gene1[1]]
            individuo.matriz[gene1[0]][gene1[1]] = individuo.matriz[gene2[0]][gene2[1]]
            individuo.matriz[gene2[0]][gene2[1]] = placeholder
    return individuo


def executa_roleta(geracao):
    total = geracao.calc_fitness_total()
    soma = 0
    roleta = []
    for ind in geracao.populacao:
        roleta.append([ind, soma, ind.fitness / total + soma])
        soma += ind.fitness / total
    tam_geracao = len(geracao.populacao)
    sobreviventes = []
    while TAM_GERACAO_INICIAL * 3 < len(geracao.populacao) <= tam_geracao:
        numero = random()
        for r in roleta:
            if r[1] <= numero <= r[2]:
                geracao.populacao.remove(r[0])
                roleta.remove(r)
                sobreviventes.append(r[0])
                break
    geracao.populacao = sobreviventes if sobreviventes else geracao.populacao
    return geracao


def main():
    solucao = encontra_solucao()
    if solucao is not None:
        for i in range(8):
            print(solucao.tabuleiro[i])
    else:
        print('Não encontrou')
    melhor_candidato = None
    for geracao in geracoes:
        if melhor_candidato is None or geracao.populacao[0].fitness > melhor_candidato.fitness:
            melhor_candidato = geracao.populacao[0]
    print(f'Fitness: {sqrt(melhor_candidato.fitness)+1} - Geração: {melhor_candidato.geracao}')
    print(f'Maior sequência: {melhor_candidato.maior_seq}')
    for linha in melhor_candidato.matriz:
        print(linha)
    mostrar_solucao(melhor_candidato.matriz)


board = Canvas(master, width=599, height=599)
board.grid(row=0, column=0)


def mostrar_solucao(matriz):
    for i in range(8):
        for j in range(8):
            cor = "white" if (i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1) else "light gray"
            board.create_rectangle(i * 75 + 2, j * 75 + 2, i * 75 + 75, j * 75 + 75, fill=cor, width=1)
            x = (((i * 75 + 75) - (i * 75 + 2)) / 2) + (i * 75 + 2)
            y = (((j * 75 + 75) - (j * 75 + 2)) / 2) + (j * 75 + 2)
            board.create_text(x, y, anchor=W, text=str(matriz[j][i]), fill="black")
    master.mainloop()


if __name__ == '__main__':
    main()
