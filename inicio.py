from jog import *
from constantes import *


def escolha_pino(m, t):
    print(f'É a sua vez {t}!')
    print()
    vez = ''
    val = 0
    if t == jog1:
        vez = pino_vermelho
    else:
        vez = pino_amarelo
    casa = movi_obrigatorio(m, vez)

    while True:
        l, c = map(int, input('Escolha o pino(l c): ').split())
        l = l-1
        c = c-1
        if m[l][c] != pino_vermelho and m[l][c] != pino_amarelo:
            print('Nessa casa não existe pino.')
        elif t == jog1 and m[l][c] != pino_vermelho:
            print('Pino inválido, sua cor é o vermelho.')
        elif t == jog2 and m[l][c] != pino_amarelo:
            print('Pino inválido, sua cor é o amarelo.')
        elif len(casa) > 0:
            comb = 0
            for i in range(len(casa)):
                for j in range(len(casa[i])):
                    if casa[i][j] - 1 == l and casa[i][j+1] - 1 == c:
                        comb = 1
                    break
            if comb == 0:
                print('Movimento de captura obrigatório, escolha um pino que possa capturar.')
            else:
                val = 2
                break
        else:
            val = movi_possiveis(m, l, c)
            if val == 0:
                print('Pino inválido, sem movimentos possivéis.')
            else:
                break


    if val == 1:
        movi_simples(m, l, c)
    elif val == 2:
        movi_captura(m, l, c)
    escreve_matriz(m, tam)
    turno = troca_turno(t, jog1, jog2)
    escolha_pino(m, turno)


def escreve_matriz(m, n):
    coluna = list(range(1, n+1))
    for i in coluna:
        if i == 1:
            print('\033[1;32ml\c', end=' ')
        print(i, end='  ')
    print()
    val_l = 0
    for i in range(n):
        val_l += 1
        print(f'\033[1;32m{val_l}\033[m', end='  ')
        for j in range(n):
            if m[i][j] == quad_branco:
                print('\033[1;47m   \033[m', end='')
            elif m[i][j] == quad_preto:
                print('\033[1;40m   \033[m', end='')
            elif m[i][j] == pino_vermelho:
                print('\033[1;31;40m ● \033[m', end='')
            elif m[i][j] == pino_amarelo:
                print('\033[1;33;40m ● \033[m', end='')
        print()
    print()


def matriz_inicial(n, p, c1, c2):
    matriz_i = []
    for i in range(n):
        matriz_i.append([])
        for j in range(n):
            if (j % 2 != 0 and i % 2 != 0) or (j % 2 == 0 and i % 2 == 0) or (j == i):
                matriz_i[i].append(quad_branco)
            else:
                if i == 3 or i == 4:
                    matriz_i[i].append(quad_preto)
                elif i < 3:
                    matriz_i[i].append(pino_amarelo)
                elif i > 4:
                    matriz_i[i].append(pino_vermelho)

    return matriz_i


def imprime_inicio(n):
    print('=' * n)
    print('\033[1;31m  JOGO DE DAMAS  \033[m')
    print('=' * n)
    print()


imprime_inicio(17)
while True:
    opcoes = int(input('Deseja ver as regras ou iniciar o jogo? Regras(1) Iniciar(2) '))
    if opcoes == 2:
        break
    print('Regras...')

jog1 = input(f'Nome do jogador 1(cor = \033[1;{c1}mvermelho\033[m): ')
jog2 = input(f'Nome do jogador 2(cor = \033[1;{c2}mamarelo\033[m): ')

turno = jog1
matriz = matriz_inicial(tam, pino, c1, c2)
escreve_matriz(matriz, tam)
escolha_pino(matriz, turno)
