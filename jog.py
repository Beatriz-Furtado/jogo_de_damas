"""
Nesse módulo está toda a lógica de um jogo de damas.
A interface deve usar essas funções para:
- Criar o primeiro tabuleiro
- Realizar e verificar os movimentos
- Promoção à dama
- Operar sobre o turno dos jogadores
- Verificar movimentos obrigatórios
"""


from constantes import *


def matriz_inicial(n):
    '''
    Cria a primeira matriz do jogo.
    :param n: Tamanho da matriz
    :return: Matriz inicial
    '''
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


def troca_turno(turno, j1, j2):
    '''
    Trocar o turno a cada jogada.
    :param turno: Informa de quem é a vez
    :param j1: Jogador 1
    :param j2: Jogador 2
    :return: De quem é a vez
    '''
    if turno == j1:
        vez = j2
    else:
        vez = j1
    return vez


def movi_obrigatorio(m, t):
    '''
    Verifica se tem alguma captura obrigatória.
    :param m: Matriz que representa o tabuleiro atual
    :param t: O turno atual
    :return: Lista de peças que podem capturar
    '''
    casas = []
    for i in range(tam):
        for j in range(tam):
            if (t == 'V' and m[i][j] == pino_vermelho) or (t == 'A' and m[i][j] == pino_amarelo):
                obrig = captura_peao(m, i, j)
                if obrig == 1:
                    casas.append([i+1, j+1])
            elif (t == 'V' and m[i][j] == dama_vermelha) or (t == 'A' and m[i][j] == dama_amarela):
                SE, SD, IE, ID = map(list, movi_possi_dama(m, i, j))
                cap = dama_possi_captura(m, SE, SD, IE, ID)
                if cap == 1:
                    casas.append([i+1, j+1])

    if len(casas) > 0:
        print('Movimento obrigatório de captura, pino(s) que pode(em) capturar:')
        for i in range(len(casas)):
            for j in range(len(casas[i])):
                if j == 0:
                    print(f'({casas[i][j]},', end=' ')
                else:
                    print(f'{casas[i][j]})', end='')
                    print()

    return casas


def movi_possiveis(m, x, y):
    '''
    Ver se há movimentos possíveis com a peça escolhida.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Movimentos possiveís, 0 = sem movimentos,
    1 = movimento simples da pedra, 2 = captura pela pedra,
    3 = movimento simples da dama, 4 = captura pela dama
    '''
    if m[x][y] == pino_vermelho or m[x][y] == pino_amarelo:
        obrig = captura_peao(m, x, y)
        if obrig == 1:
            return 2

        elif m[x][y] == pino_vermelho and ((y>0 and m[x-1][y-1] == quad_preto) or (y<7 and m[x-1][y+1] == quad_preto)):
            return 1
        elif m[x][y] == pino_amarelo and ((y>0 and m[x+1][y-1] == quad_preto) or (y<7 and m[x+1][y+1] == quad_preto)):
            return 1
        else:
            return 0
    elif m[x][y] == dama_vermelha or m[x][y] == dama_amarela:
        SE, SD, IE, ID = map(list, movi_possi_dama(m, x, y))
        if len(SE) == 0 and len(SD) == 0 and len(IE) == 0 and len(ID) == 0:
            return 0
        cap = dama_possi_captura(m, SE, SD, IE, ID)
        if cap == 1:
            return 4
        else:
            return 3


def movi_peao_simples(m, x, y):
    '''
    Realiza o movimento simples do peão.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Matriz após realizado o mivimento
    '''
    while True:
        try:
            l, c = map(int, input('Escolha o movimento(l c): ').split())
        except ValueError:
            print('Digite apenas números para fazer a jogada, lembrando de dar um espaço entre eles.')
        else:
            l = l-1
            c = c-1
            if l == tam or c == tam or l == -1 or c == -1:
                print('Movimento inválido, fora do tabuleiro.')
            elif m[l][c] == pino_amarelo or m[l][c] == pino_vermelho:
                print('Movimento inválido, casa ocupada.')
            elif m[x][y] == pino_amarelo:
                if l != x + 1 or (c != y - 1 and c != y + 1):
                    print('Movimento inválido, essa peça só pode andar uma casa na diagonal e pra frente.')
                else:
                    break
            elif m[x][y] == pino_vermelho:
                if l != x - 1 or (c != y - 1 and c != y + 1):
                    print('Movimento inválido, essa peça só pode andar uma casa na diagonal e pra frente.')
                else:
                    break
            else:
                break

    m[l][c] = m[x][y]
    m[x][y] = quad_preto
    promocao(m, l, c)
    return m


def movi_peao_captura(m, x, y):
    '''
    Realiza o movimento de captura pelo peão.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Matriz após realizado o mivimento
    '''
    while True:
        try:
            l, c = map(int, input('Escolha o movimento(l c): ').split())
        except ValueError:
            print('Digite apenas números para fazer a jogada, lembrando de dar um espaço entre eles.')
        else:
            l = l-1
            c = c-1
            if (l != x-2 and c != y-2) and (l != x-2 and c != y+2) and (l != x+2 and c != y-2) and (l != x+2 and c != y+2):
                print('Captura obrigatória!')
                print('Sempre uma casa a mais na direção da peça a ser capturada.')
            elif l == tam or c == tam or l == -1 or c == -1:
                print('Movimento inválido, fora do tabuleiro.')
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
    obrig = captura_peao(m, l, c)
    if obrig == 1:
        print('Captura obrigatória de mais uma peça, informe o novo movimento.')
        movi_peao_captura(m, l, c)
    else:
        promocao(m, l, c)
        return m


def captura_peao(m, x, y):
    '''
    Verifica se o peão pode realizar uma captura.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: 1 se a pedra pode capturar e 0 se não pode
    '''
    opositora1 = ''
    opositora2 = ''
    if m[x][y] == pino_vermelho:
        opositora1 = pino_amarelo
        opositora2 = dama_amarela
    elif m[x][y] == pino_amarelo:
        opositora1 = pino_vermelho
        opositora2 = dama_vermelha

    if y > 1 and x > 1 and ((m[x-1][y-1] == opositora1 or m[x-1][y-1] == opositora2) and m[x-2][y-2] == quad_preto):
        return 1
    if y > 1 and x < 6 and ((m[x+1][y-1] == opositora1 or m[x+1][y-1] == opositora2) and m[x+2][y-2] == quad_preto):
        return 1
    if y < 6 and x > 1 and ((m[x-1][y+1] == opositora1 or m[x-1][y+1] == opositora2) and m[x-2][y+2] == quad_preto):
        return 1
    if y < 6 and x < 6 and ((m[x+1][y+1] == opositora1 or m[x+1][y+1] == opositora2) and m[x+2][y+2] == quad_preto):
        return 1
    else:
        return 0


def promocao(m, x, y):
    '''
    Promove o peão à dama.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Matriz após realizada a promoção
    '''
    if m[x][y] == pino_vermelho and x == 0:
        m[x][y] = dama_vermelha
    elif m[x][y] == pino_amarelo and x == 7:
        m[x][y] = dama_amarela

    return m


def diagonal_livre_dama(m, x, y, v1, v2, mp, op):
    '''
    Verifica casas livres na diagonal da dama,
    para realizar seu movimento.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :param v1: Valor a ser somado, indicando a diagonal
    :param v2: Valor a ser somado, indicando a diagonal
    :param mp: Uma lista para adicionar casas possíveis
    :param op: Opositora da peça
    :return: Lista com casas possíveis na diagonal, para o movimento
    '''
    while True:
        x = x + (v1)
        y = y + (v2)
        if x < 0 or x > 7 or y < 0 or y > 7:
            break
        if 0 < x < 7 and 0 < y < 7:
            if op == 'A' and (m[x][y] == pino_amarelo or m[x][y] == dama_amarela) and m[x+(v1)][y+(v2)] == quad_preto:
                mp = captura_dama(m, x, y, v1, v2)
                break
            elif op == 'V' and (m[x][y] == pino_vermelho or m[x][y] == dama_vermelha) and m[x+(v1)][y+(v2)] == quad_preto:
                mp = captura_dama(m, x, y, v1, v2)
                break
        if m[x][y] != quad_preto:
            break
        mp.append([x, y])

    return mp


def movi_possi_dama(m, x, y):
    '''
    Verifica se há algum movimento possivel da dama.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: lista com todas as casas disponíveis nas
    diagonais, para o movimento
    '''
    opositora = ''
    if m[x][y] == pino_vermelho or m[x][y] == dama_vermelha:
        opositora = 'A'
    elif m[x][y] == pino_amarelo or m[x][y] == dama_amarela:
        opositora = 'V'
    mp = []

    SE = diagonal_livre_dama(m, x, y, -1, -1, mp, opositora)
    mp = []
    SD = diagonal_livre_dama(m, x, y, -1, +1, mp, opositora)
    mp = []
    IE = diagonal_livre_dama(m, x, y, +1, -1, mp, opositora)
    mp = []
    ID = diagonal_livre_dama(m, x, y, +1, +1, mp, opositora)

    return [SE, SD, IE, ID]


def movi_dama_simples(m, x, y):
    '''
    Realiza o movimento da dama.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Matriz após realizado o movimento
    '''
    SE, SD, IE, ID = map(list, movi_possi_dama(m, x, y))
    while True:
        try:
            l, c = map(int, input('Escolha o movimento(l c): ').split())
        except ValueError:
            print('Digite apenas números para fazer a jogada, lembrando de dar um espaço entre eles.')
        else:
            l = l-1
            c = c-1
            mov = [l, c]
            if l == tam or c == tam or l == -1 or c == -1:
                print('Movimento inválido, fora do tabuleiro.')
            elif m[l][c] == pino_amarelo or m[l][c] == pino_vermelho or m[l][c] == dama_vermelha or m[l][c] == dama_amarela:
                print('Movimento inválido, casa ocupada.')
            elif mov in SE or mov in SD or mov in IE or mov in ID:
                break
            else:
                print('Movimento inválido, essa peça só pode andar na diagonal, para frente e para trás.')

    m[l][c] = m[x][y]
    m[x][y] = quad_preto
    return m


def captura_dama(m, x, y, v1, v2):
    '''
    Lista as casas possíveis de parada depois
    da paça a ser capturada pela dama.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino a ser capturado está
    :param y: Coluna na qual o pino a ser capturado está
    :param v1: Valor a ser somado, indicando a diagonal
    :param v2: Valor a ser somado, indicando a diagonal
    :return: Matriz com casas de parada possíveis após
    a peça a ser capturada
    '''
    mp = []
    mp.append([x, y])
    while True:
        x = x + (v1)
        y = y + (v2)
        if x < 0 or x > 7 or y < 0 or y > 7 or m[x][y] != quad_preto:
            break

        mp.append([x, y])

    return mp


def dama_possi_captura(m, se, sd, ie, id):
    '''
    Verifica se a dama pode realizar uma captura.
    :param m: Matriz que representa o tabuleiro atual
    :param se: Lista das casas disponíveis na diagonal superior esquerda
    :param sd: Lista das casas disponíveis na diagonal superior direita
    :param ie: Lista das casas disponíveis na diagonal inferior esquerda
    :param id: Lista das casas disponíveis na diagonal inferior direita
    :return: 1 se a dama pode realizar uma captura e 0 se não pode
    '''
    if len(se) > 0 and m[se[0][0]][se[0][1]] != quad_preto or len(sd) > 0 and m[sd[0][0]][sd[0][1]] != quad_preto:
        return 1
    elif len(ie) > 0 and m[ie[0][0]][ie[0][1]] != quad_preto or len(id) > 0 and m[id[0][0]][id[0][1]] != quad_preto:
        return 1
    else:
        return 0


def movi_dama_captura(m, x, y):
    '''Realiza o movimento de captura pela dama.
    :param m: Matriz que representa o tabuleiro atual
    :param x: Linha na qual o pino está
    :param y: Coluna na qual o pino está
    :return: Matriz após realizado o mivimento
    '''
    SE, SD, IE, ID = map(list, movi_possi_dama(m, x, y))
    peca_comida = []
    while True:
        try:
            l, c = map(int, input('Escolha o movimento(l c): ').split())
        except ValueError:
            print('Digite apenas números para fazer a jogada, lembrando de dar um espaço entre eles.')
        else:
            l = l-1
            c = c-1
            mov = [l, c]
            if l == tam or c == tam or l == -1 or c == -1:
                print('Movimento inválido, fora do tabuleiro.')
            elif m[l][c] == pino_amarelo or m[l][c] == pino_vermelho or m[l][c] == dama_vermelha or m[l][c] == dama_amarela:
                print('Movimento inválido, casa ocupada.')
            elif mov in SE and m[SE[0][0]][SE[0][1]] != quad_preto:
                peca_comida = SE[0]
                break
            elif mov in SD and m[SD[0][0]][SD[0][1]] != quad_preto:
                peca_comida = SD[0]
                break
            elif mov in IE and m[IE[0][0]][IE[0][1]] != quad_preto:
                peca_comida = IE[0]
                break
            elif mov in ID and m[ID[0][0]][ID[0][1]] != quad_preto:
                peca_comida = ID[0]
                break
            else:
                print('Captura obrigatória de uma peça!')

    m[l][c] = m[x][y]
    m[x][y] = quad_preto
    l_c, c_c = map(int, peca_comida)
    m[l_c][c_c] = quad_preto
    SE, SD, IE, ID = map(list, movi_possi_dama(m, l, c))
    cap = dama_possi_captura(m, SE, SD, IE, ID)
    if cap == 1:
        print('Captura obrigatória de mais uma peça, informe o novo movimento.')
        movi_dama_captura(m, l, c)
    return m
