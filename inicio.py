"""
Módulo que faz a interface com o usuário
"""


from jog import *
from constantes import *
from arquivo import *


def jogar(m, t, j1, j2, cont):
    '''
    Começar a jogada.
    - Recebe pino escolhido
    - verifica se é válido
    - Encaminha para o movimento possível
    :param m: Matriz que representa o tabuleiro
    :param t: O turno
    :param j1: Jogador 1
    :param j2: Jogador 2
    :param cont: Contador de lances
    '''
    print(f'É a sua vez {t}!', end='')
    print()
    vez = ''
    val = 0
    if t == jog1:
        vez = 'V'
    else:
        vez = 'A'
    casa = movi_obrigatorio(m, vez)

    while True:
        try:
            l, c = map(int, input('Escolha o pino(l c): ').split())
        except ValueError:
            opcao = input('Deseja sair?(S/N) ')
            opcao = opcao.upper()
            if opcao == 'S' or opcao == 'SIM':
                sair(m, t, j1, j2, cont)
            else:
                print('Digite apenas números para fazer a jogada, lembrando de dar um espaço entre eles.')
        else:
            l = l-1
            c = c-1

            if m[l][c] != pino_vermelho and m[l][c] != pino_amarelo and m[l][c] != dama_vermelha and m[l][c] != dama_amarela:
                print('Nessa casa não existe pino.')
            elif t == jog1 and m[l][c] != pino_vermelho and m[l][c] != dama_vermelha:
                print('Pino inválido, sua cor é o vermelho.')
            elif t == jog2 and m[l][c] != pino_amarelo and m[l][c] != dama_amarela:
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
                elif m[l][c] == pino_vermelho or m[l][c] == pino_amarelo:
                    val = 2
                    break
                elif m[l][c] == dama_vermelha or m[l][c] == dama_amarela:
                    val = 4
                    break
            else:
                val = movi_possiveis(m, l, c)
                if val == 0:
                    print('Pino inválido, sem movimentos possivéis.')
                else:
                    break

    if val == 1:
        movi_peao_simples(m, l, c)
    elif val == 2:
        movi_peao_captura(m, l, c)
    elif val == 3:
        movi_dama_simples(m, l, c)
    elif val == 4:
        movi_dama_captura(m, l, c)

    escreve_tabuleiro(m, tam)
    cont = cont_lances(val, cont)
    turno = troca_turno(t, j1, j2)
    jogar(m, turno, j1, j2, cont)


def cont_lances(val, cont):
    '''
    Conta os lances para a condição de empate.
    :param val: Valor que indica o movimento realizado
    :param cont: O valor do contador
    :return: Valor do contador
    '''
    if val == 3:
        cont += 1
    elif val != 3:
        cont = 0
    if cont == 20:
        final_jogo('E')
    return cont


def escreve_tabuleiro(m, n):
    '''
    Escreve na tale o tabuleiro ao longo do jogo.
    :param m: Matriz que representa o tabuleiro
    :param n: O tamanho da matriz
    '''
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
            elif m[i][j] == dama_vermelha:
                print('\033[1;31;40m * \033[m', end='')
            elif m[i][j] == dama_amarela:
                print('\033[1;33;40m * \033[m', end='')
        print()
    print()
    verifica_vencedor(m)


def verifica_vencedor(m):
    '''
    Verifica se há algum vencedor a cada jogada.
    :param m: Matriz que representa o tabuleiro atual
    '''
    dv = 0
    pv = 0
    da = 0
    pa = 0
    possi_ver = 0
    possi_ama = 0
    v = ''
    for i in range(len(m)):
        dv += m[i].count(dama_vermelha)
        pv += m[i].count(pino_vermelho)
        da += m[i].count(dama_amarela)
        pa += m[i].count(pino_amarelo)

    if (dv > 0 or pv > 0) and da == 0 and pa == 0:
        v = 'V'
    elif dv == 0 and pv == 0 and (da > 0 or pa > 0):
        v = 'A'
    elif dv == 1 and pv == 0 and da == 1 and pa == 0:
        v = 'E'
    elif (dv > 0 or pv > 0) and (da > 0 or pa > 0):
        for i in range(tam):
            for j in range(tam):
                if m[i][j] == dama_vermelha or m[i][j] == pino_vermelho:
                    possi = movi_possiveis(m, i, j)
                    if possi != 0:
                        possi_ver += 1
                elif m[i][j] == dama_amarela or m[i][j] == pino_amarelo:
                    possi = movi_possiveis(m, i, j)
                    if possi != 0:
                        possi_ama += 1

        if possi_ama == 0:
            v = 'V'
        elif possi_ver == 0:
            v = 'A'
    if v != '':
        final_jogo(v)
    return


def sair(m, t, j1, j2, cont):
    '''
    Interrompe o jogo.
    :param m: Matriz que representa o tabuleiro atual
    :param t: O turno do jogo
    :param j1: Jogador 1
    :param j2: Jogador 2
    :param cont: O valor do contador de lances
    '''
    opcao = input('Deseja salvar o jogo, para começar depois de onde parou?(S/N) ')
    opcao = opcao.upper()
    if opcao == 'S' or opcao == 'SIM':
        salvar_jogo(m, t, j1, j2, cont)

    print('Volte sempre!')
    exit()


def salvar_jogo(m, t, j1, j2, cont):
    '''
    Salva o jogo para jogar depois.
    :param m: Matriz que representa o tabuleiro atual
    :param t: O turno do jogo
    :param j1: Jogador 1
    :param j2: Jogador 2
    :param cont: O valor do contador de lances
    '''
    arq_texto = 'jogosalvo.txt'
    arq_tabuleiro = 'tabuleirosalvo.txt'
    if arquivo_existe(arq_texto):
        a = open('jogosalvo.txt', 'w')
        a.close()
    if arquivo_existe(arq_tabuleiro):
        a = open('tabuleirosalvo.txt', 'w')
        a.close()

    criar_arquivo(arq_texto)
    adicionar_texto(arq_texto, t, j1, j2, cont)
    criar_arquivo(arq_tabuleiro)
    adicionar_tabuleiro(arq_tabuleiro, m)


def final_jogo(v):
    '''
    Informa o status final e encerra o jogo.
    - Ganhador
    - Empate
    :param v: Variavél que indica o status do jogo
    '''
    vencedor = ''
    txt = ''
    if v == 'V':
        vencedor = jog1.upper()
        txt = f'{vencedor} VENCEU!'
    elif v == 'A':
        vencedor = jog2.upper()
        txt = f'{vencedor} VENCEU!'
    elif v == 'E':
        txt = 'EMPATE'

    imprime_informacoes(30, txt)
    exit()


def imprime_informacoes(n, txt):
    '''
    Irá imprimir informações importantes
    personalizadas.
    :param n: Tamanho do print
    :param txt: Texto a ser escrito
    '''
    print('=' * n)
    print(f'\033[1;36m{txt.center(n)}\033[m')
    print('=' * n)
    print()

#Inicia o jogo
imprime_informacoes(30, inicio)
while True:
    '''
    O menu do jogo.
    (1) Regras
    (2) começar jogo
    (3) continuar com o jogo salvo
    '''
    opcoes = int(input('Deseja ver as regras, iniciar um novo jogo ou continuar jogando? Regras(1) Iniciar(2) Continuar(3) '))
    if opcoes == 3:
        a = open('jogosalvo.txt', 'r')
        t, jog1, jog2, cont = map(str, a.readline().split())
        m = []
        b = open('tabuleirosalvo.txt', 'r')
        for i in range(tam):
            for j in range(tam):
                linha = b.readline()
                linha = list(linha)
                l = []
                v = 0
                for h in linha:
                    if v < 8:
                        l.append(h)
                    else:
                        break
                    v += 1

                m.append(l)
                break

        escreve_tabuleiro(m, tam)
        jogar(m, t, jog1, jog2, cont)

    elif opcoes == 2:
        break
    elif opcoes == 1:
        print(regras)
        print()

jog1 = input(f'Nome do jogador 1(cor = \033[1;{c1}mvermelho\033[m): ')#nome do jogador 1
jog2 = input(f'Nome do jogador 2(cor = \033[1;{c2}mamarelo\033[m): ')#nome do jogador 2

turno = jog1
matriz = matriz_inicial(tam)
escreve_tabuleiro(matriz, tam)
cont = 0
jogar(matriz, turno, jog1, jog2, cont)
