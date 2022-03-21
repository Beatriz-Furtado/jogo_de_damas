from jog import *
from constantes import *
from arquivo import *

def escolha_pino(m, t, j1, j2):
    '''Onde o usuário irá escolher o pino para
    fazer a jogada, e vai verificar se o pino
    é válido ou não, e ver se há alguma jogada
    possível.'''
    print(f'É a sua vez {t}!', end='')
    print()
    vez = ''
    val = 0
    if t == jog1:
        vez = pino_vermelho
    else:
        vez = pino_amarelo
    casa = movi_obrigatorio(m, vez)

    while True:
        try:
            l, c = map(int, input('Escolha o pino(l c): ').split())
        except ValueError:
            opcao = input('Deseja sair?(S/N) ')
            opcao = opcao.upper()
            if opcao == 'S' or opcao == 'SIM':
                sair(m, t, j1, j2)
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
        movi_simples(m, l, c)
    elif val == 2:
        movi_captura(m, l, c)
    elif val == 3:
        movi_dama_simples(m, l, c)
    elif val == 4:
        movi_dama_captura(m, l, c)

    escreve_matriz(m, tam)
    turno = troca_turno(t, j1, j2)
    escolha_pino(m, turno, j1, j2)


def escreve_matriz(m, n):
    '''Escreve na tale o tabuleiro ao longo do jogo.'''
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


def matriz_inicial(n, p, c1, c2):
    '''Cria a primeira matriz do jogo.'''
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


def sair(m, t, j1, j2):
    '''Sair do jogo, pode também salvar
    o jogo para jogar depois.'''
    opcao = input('Deseja salvar o jogo, para começar depois de onde parou?(S/N) ')
    opcao = opcao.upper()
    if opcao == 'S' or opcao == 'SIM':
        arq_texto = 'jogosalvo.txt'
        arq_tabuleiro = 'tabuleirosalvo.txt'
        if arquivoexiste(arq_texto):
            a = open('jogosalvo.txt', 'w')
            a.close()
        if arquivoexiste(arq_tabuleiro):
            a = open('tabuleirosalvo.txt', 'w')
            a.close()

        criarArquivo(arq_texto)
        adicionar_texto(arq_texto, t, j1, j2)
        criarArquivo(arq_tabuleiro)
        adicionar_tabuleiro(arq_tabuleiro, m)

    print('Volte sempre!')
    exit()


def imprime_inicio(n):
    '''Irá imprimir a chamada do jogo, o título.'''
    print('=' * n)
    print('\033[1;31m  JOGO DE DAMAS  \033[m')
    print('=' * n)
    print()


imprime_inicio(17)
while True:
    '''O menu do jogo, onde irá ter as regras, 
    opção de começar o jogo ou continuar a jogar'''
    opcoes = int(input('Deseja ver as regras, iniciar um novo jogo ou continuar jogando? Regras(1) Iniciar(2) Continuar(3) '))
    if opcoes == 3:
        a = open('jogosalvo.txt', 'r')
        t = a.readline()
        jog1 = a.readline()
        jog2 = a.readline()
        m = []
        b = open('tabuleirosalvo.txt', 'r')
        for i in range(tam):
            for j in range(tam):
                linha = b.readline()
                linha = list(linha)
                l = []
                cont = 0
                for h in linha:
                    if cont < 8:
                        l.append(h)
                    else:
                        break
                    cont += 1

                m.append(l)
                break

        escreve_matriz(m, tam)
        escolha_pino(m, t, jog1, jog2)

    if opcoes == 2:
        break
    print('Regras...')

jog1 = input(f'Nome do jogador 1(cor = \033[1;{c1}mvermelho\033[m): ')#nome do jogador 1
jog2 = input(f'Nome do jogador 2(cor = \033[1;{c2}mamarelo\033[m): ')#nome do jogador 2

turno = jog1
matriz = matriz_inicial(tam, pino, c1, c2)
escreve_matriz(matriz, tam)
escolha_pino(matriz, turno, jog1, jog2)


