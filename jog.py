from constantes import *


def troca_turno(turno, j1, j2):
    if turno == j1:
        vez = j2
    else:
        vez = j1
    return vez


def movi_obrigatorio(m, t):
    casas = []
    for i in range(tam):
        for j in range(tam):
            if t == pino_vermelho:
                if m[i][j] == pino_vermelho:
                    obrig = capturas(m, i, j)
                    if obrig == 1:
                        casas.append([i+1, j+1])

            else:
                if m[i][j] == pino_amarelo:
                    obrig = capturas(m, i, j)
                    if obrig == 1:
                        casas.append([i+1, j+1])

    if len(casas) > 0:
        print('Movimento obrigatório de captura, casa(s) a ser(em) escolhida(s):')
        for i in range(len(casas)):
            for j in range(len(casas[i])):
                if j == 0:
                    print(f'({casas[i][j]},', end=' ')
                else:
                    print(f'{casas[i][j]})', end='')
                    print()

    return casas


def movi_possiveis(m, x, y):
    obrig = capturas(m, x, y)
    if obrig == 1:
        return 2
        #movi_captura(m, x, y)
    elif m[x][y] == pino_vermelho and (m[x-1][y-1] == quad_preto or m[x-1][y+1] == quad_preto):
        return 1
        #movi_simples(m, x, y)
    elif m[x][y] == pino_amarelo and (m[x+1][y-1] == quad_preto or m[x+1][y+1] == quad_preto):
        return 1
    else:
        return 0


def movi_simples(m, x, y):
    while True:
        l, c = map(int, input('Escolha o movimento(l c): ').split())
        l = l-1
        c = c-1
        if l == tam or c == tam or l == -1 or c == -1:
            print('Movimento inválido, fora do tabuleiro')
        elif m[l][c] == pino_amarelo or m[l][c] == pino_vermelho:
            print('Movimento inválido, casa ocupada.')
        elif m[x][y] == pino_amarelo:
            if l != x + 1 or (c != y - 1 and c != y + 1):
                print('Movimento inválido, essa peça só pode andar na diagonal e pra frente.')
            else:
                break
        elif m[x][y] == pino_vermelho:
            if l != x - 1 or (c != y - 1 and c != y + 1):
                print('Movimento inválido, essa peça só pode andar na diagonal e pra frente.')
            else:
                break
        else:
            break

    m[l][c] = m[x][y]
    m[x][y] = quad_preto
    return m


def movi_captura(m, x, y):
    while True:
        l, c = map(int, input('Escolha o movimento(l c): ').split())
        l = l-1
        c = c-1
        if (l != x-2 and c != y-2) and (l != x-2 and c != y+2) and (l != x+2 and c != y-2) and (l != x+2 and c != y+2):
            print('''Captura obrigatória!
            Sempre uma casa a mais na direção da peça a ser capturada.''')
        elif l == tam or c == tam or l == -1 or c == -1:
            print('Movimento inválido, fora do tabuleiro')
        elif m[l][c] == pino_amarelo or m[l][c] == pino_vermelho:
            print('Movimento inválido, casa ocupada.')
        else:
            break

    peca_comida = []
    if l == x-2 and c == y-2:
        peca_comida.append(x-1)
        peca_comida.append(y-1)
    elif l == x-2 and c == y+2:
        peca_comida.append(x-1)
        peca_comida.append(y+1)
    elif l == x+2 and c == y-2:
        peca_comida.append(x+1)
        peca_comida.append(y-1)
    elif l == x+2 and c == y+2:
        peca_comida.append(x+1)
        peca_comida.append(y+1)
    m[l][c] = m[x][y]
    m[x][y] = quad_preto
    l_c, c_c = map(int, peca_comida)
    m[l_c][c_c] = quad_preto
    obrig = capturas(m, l, c)
    if obrig == 1:
        print('Captura obrigatória de mais uma peça, informe o novo movimento.')
        movi_captura(m, l, c)
    else:
        return m


def capturas(m, x, y):
    opositora = ''
    if m[x][y] == pino_vermelho:
        opositora = pino_amarelo
    elif m[x][y] == pino_amarelo:
        opositora = pino_vermelho

    if y > 1 and x > 1 and (m[x - 1][y - 1] == opositora and m[x - 2][y - 2] == quad_preto):
        return 1
    if y > 1 and x < 6 and (m[x + 1][y - 1] == opositora and m[x + 2][y - 2] == quad_preto):
        return 1
    if y < 6 and x > 1 and (m[x - 1][y + 1] == opositora and m[x - 2][y + 2] == quad_preto):
        return 1
    if y < 6 and x < 6 and (m[x + 1][y + 1] == opositora and m[x + 2][y + 2] == quad_preto):
        return 1
    else:
        return 0




