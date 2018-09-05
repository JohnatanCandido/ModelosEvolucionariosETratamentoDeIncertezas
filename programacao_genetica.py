from random import randint


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


def printa_funcao(node):
    if node.left is not None:
        printa_funcao(node.left)
    print(node.valor, end='')
    if node.right is not None:
        printa_funcao(node.right)


def gera_arvore():
    raiz = Node(valores[randint(0, 4)], None)
    print('Função: ', end='')
    printa_funcao(raiz)
    print(f'\n\nProfundidade: {calc_prof(raiz)}')


if __name__ == '__main__':
    gera_arvore()