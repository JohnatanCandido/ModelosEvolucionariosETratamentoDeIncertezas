from random import randint


operadores = ['+', '-', '*', '/']
valores = ['x', '+', '-', '*', '/', 1, 2, 3, 4, 5, 6, 7, 8, 9]


class Node:
    def __init__(self, valor, raiz):
        self.valor = valor
        if isinstance(valor, str) and valor != 'x':
            self.left = Node(valores[randint(0, len(valores)-1)], self)
            self.right = Node(valores[randint(0, len(valores)-1)], self)
        else:
            self.left = None
            self.right = None
        self.raiz = raiz


def calc_prof(node, left=1, right=1):
    if node.left is not None:
        left += calc_prof(node.left)
    if node.right is not None:
        right += calc_prof(node.right)
    return left if left > right else right


def printa_funcao(node, funcao=''):
    if node.left is not None:
        funcao += printa_funcao(node.left, funcao)
    print(node.valor, end='')
    funcao += str(node.valor)
    if node.right is not None:
        funcao += printa_funcao(node.right)
    return str(funcao)


def executa_funcao(funcao, x):
    while len(funcao) > 2:
        i = 0
        n1 = ''
        n2 = ''
        while funcao[i] not in operadores:
            n1 += funcao[i] if funcao[i] != 'x' else x
            i += 1
        n1 = n1 if n1 != '' else 0
        o = funcao[i]
        i += 1
        while i < len(funcao) and funcao[i] not in operadores:
            n2 += funcao[i] if funcao[i] != 'x' else x
            i += 1
        r = executa_operacao(int(n1), o, int(n2))
        funcao = str(r) + funcao[i:]
    return x if funcao == 'x' else funcao


def executa_operacao(n1, o, n2):
    if o == '+':
        return str(n1 + n2)
    elif o == '-':
        return str(n1 - n2)
    elif o == '*':
        return str(n1 * n2)
    elif o == '/':
        return str(int(n1 / n2))


def gera_arvore():
    raiz = Node(valores[randint(0, 4)], None)
    print('Função: ', end='')
    funcao = printa_funcao(raiz)
    print(f'\nTeste:  {funcao}')
    print(f'\n\nProfundidade: {calc_prof(raiz)}')
    print(f'Resultado: {executa_funcao(funcao, 1)}')


if __name__ == '__main__':
    gera_arvore()