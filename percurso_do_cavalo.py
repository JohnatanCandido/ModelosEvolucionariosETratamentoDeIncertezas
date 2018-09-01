from random import randint, random, shuffle


geracao_atual = 0
geracoes = []
TAM_GERACAO_INICIAL = 100
NUMERO_GERACOES = 100
CHANCE_MUTAR = 0.02

melhor_candidato = None

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
    def __init__(self, geracao, tabuleiro):
        self.geracao = geracao
        self.tabuleiro = tabuleiro
        self.matriz = [self.tabuleiro[i*8:i*8+8] for i in range(8)]
        self.fitness = self.calc_fitness()
        self.exp_vida = int(self.fitness/10) + 1

    def calc_fitness(self):
        fitness = 0
        for i in range(8):
            for j in range(8):
                fitness += self._possui_movimento_valido(i, j)
        return fitness

    def _possui_movimento_valido(self, i, j):
        proximo = self.matriz[i][j] + 1
        for m in MOVIMENTOS_VALIDOS:
            try:
                if i + m[0] > -1 and j + m[1] > -1:
                    if self.matriz[i + m[0]][j + m[1]] == proximo:
                        return 1
            except IndexError:
                pass
        return 0

    def is_ded(self):
        return self.geracao + self.exp_vida < geracao_atual

    def converte_matriz_lista(self):
        self.tabuleiro = []
        for linha in self.matriz:
            self.tabuleiro += linha
        self.fitness = self.calc_fitness()


class Geracao:
    def __init__(self, populacao, geracao):
        self.populacao = populacao
        self.geracao = geracao

    def calc_fitness_total(self):
        total = 0
        for ind in self.populacao:
            total += ind.calc_fitness()
        return total

    def busca_solucao(self):
        for ind in self.populacao:
            if ind.fitness == 64:
                return ind
        return None

    def media_fitness(self):
        return self.calc_fitness_total() / len(self.populacao)

    def teste(self):
        total = 0
        for ind in self.populacao:
            total += ind.calc_fitness()**2
        return total


def gera_populacao(qt, adding=False):
    populacao = []
    for _ in range(qt):
        populacao.append(gera_individuo())
    if adding:
        return populacao
    return Geracao(populacao, geracao_atual)


def gera_individuo():
    tabuleiro = [i for i in range(1, 65)]
    shuffle(tabuleiro)
    return Individuo(geracao_atual, tabuleiro)


def cruzar(geracao):
    tam_inicial = len(geracao.populacao)
    nao_cruzado = [ind for ind in geracao.populacao]
    while len(nao_cruzado) > tam_inicial * 0.30:
        pai_1 = nao_cruzado.pop(randint(0, len(nao_cruzado)-1))
        pai_2 = nao_cruzado.pop(randint(0, len(nao_cruzado)-1))
        filho_1 = []
        filho_2 = []
        for i in range(64):
            if i % 2 == 0:
                filho_1.append(pai_1.tabuleiro[i])
                filho_2.append(pai_2.tabuleiro[i])
            else:
                filho_1.append(-1)
                filho_2.append(-1)
        for i in range(64):
            for j in range(64):
                if filho_1[j] == -1 and pai_2.tabuleiro[i] not in filho_1:
                    filho_1[j] = pai_2.tabuleiro[i]
                if filho_2[j] == -1 and pai_1.tabuleiro[i] not in filho_2:
                    filho_2[j] = pai_1.tabuleiro[i]
        if -1 in filho_1 or -1 in filho_2:
            raise Exception('Não deveria haver o valor -1 nos indivíduos')
        geracao.populacao.append(mutar(filho_1, geracao.geracao))
        geracao.populacao.append(mutar(filho_2, geracao.geracao))
    return geracao


def mutar(genotipo, num_ger):
    if random() <= CHANCE_MUTAR*10 if geracoes[geracao_atual-2].media_fitness() < 5 else CHANCE_MUTAR:
        for _ in range(randint(1, 30)):
            gene1 = -1
            gene2 = -1
            while gene1 == gene2:
                gene1 = randint(0, 63)
                gene2 = randint(0, 63)
            placeholder = genotipo[gene1]
            genotipo[gene1] = genotipo[gene2]
            genotipo[gene2] = placeholder
    return Individuo(num_ger, genotipo)


def gera_nova_geracao(geracao):
    nova_geracao = executa_roleta(Geracao(geracao.populacao[:], geracao_atual))
    for ind in nova_geracao.populacao:
        if ind.is_ded():
            nova_geracao.populacao.remove(ind)
    return cruzar(nova_geracao)


def encontra_solucao():
    global geracao_atual
    for geracao_atual in range(1, 101):
        if not geracoes:
            geracoes.append(gera_populacao(TAM_GERACAO_INICIAL))
        else:
            geracoes.append(gera_nova_geracao(geracoes[geracao_atual-2]))
            if len(geracoes[geracao_atual-1].populacao) < TAM_GERACAO_INICIAL:
                geracoes[geracao_atual-1].populacao += gera_populacao(TAM_GERACAO_INICIAL, True)
        solucao = geracoes[geracao_atual-1].busca_solucao()
        if solucao is not None:
            return solucao
        print(f'{geracao_atual} - {len(geracoes[geracao_atual-1].populacao)} '
              f'- Média: {geracoes[geracao_atual-1].media_fitness()}')
    return None


def executa_roleta(geracao):
    total = geracao.teste()
    soma = 0
    roleta = []
    for ind in geracao.populacao:
        roleta.append([ind, soma, (ind.fitness**2)/total+soma])
        soma += ind.fitness**2/total
    tam_geracao = len(geracao.populacao)
    sobreviventes = []
    while TAM_GERACAO_INICIAL*5 < len(geracao.populacao) <= tam_geracao:
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
        print('Não encontrou...')

    global melhor_candidato
    for geracao in geracoes:
        for ind in geracao.populacao:
            if melhor_candidato is None or ind.calc_fitness() > melhor_candidato.calc_fitness():
                melhor_candidato = ind
    print(melhor_candidato.fitness)
    for linha in melhor_candidato.matriz:
        print(linha)


if __name__ == '__main__':
    main()