"""
Esse módulo manipula arquivos de texto.
A interface deve usar essas funções para:
- Verificar se um arquivo existe
- Criar um arquivo
- Adicionar informações importantes nos arquivos
"""


def arquivo_existe(nome):
    '''
    Verifica se o arquivo já existe.
    :param nome: Nome do arquivo
    :return: True se o arquivo existe ou False se não
    '''
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criar_arquivo(nome):
    '''
    Cria o arquivo caso ele não exista.
    :param nome: Nome do arquivo
    '''
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('Houve um erro na criação do arquivo!')
    else:
        print(f'Arquivo {nome} criado com sucesso')


def adicionar_texto(arq, t, j1, j2, cont):
    '''
    Adiciona informações no arquivo de texto.
    :param arq: O arquivo selecionado
    :param t: O último turno
    :param j1: Jogador 1
    :param j2: Jogador 2
    :param cont: O contador de lances
    '''
    try:
        a = open(arq, 'at')
    except:
        print('Houve um erro na arbetura do arquivo!')
    else:
        try:
            a.write(f'{t} ')
            a.write(f'{j1} ')
            a.write(f'{j2} ')
            a.write(f'{cont}')
        except:
            print('Houve um erro na hora de escrever os dados')
        else:
            print('informações salvas.')
            a.close()


def adicionar_tabuleiro(arq, m):
    '''
    Adiciona tabuleiro ao arquivo de texto.
    :param arq: O arquivo selecionado
    :param m: Matriz para o qual irá se basear o tabuleiro
    '''
    try:
        b = open(arq, 'at')
    except:
        print('Houve um erro na arbetura do arquivo!')
    else:
        try:
            for i in range(len(m)):
                for j in range(len(m[i])):
                    if j == len(m[i]) - 1:
                        b.write(f'{m[i][j]}\n')
                    else:
                        b.write(f'{m[i][j]}')

        except:
            print('Houve um erro na hora de escrever os dados')
        else:
            print('Tabuleiro salvo.')
            b.close()
