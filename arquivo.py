def arquivoexiste(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criarArquivo(nome):
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('Houve um erro na criação do arquivo!')
    else:
        print(f'Arquivo {nome} criado com sucesso')


def adicionar_texto(arq, t='', j1='', j2=''):
    try:
        a = open(arq, 'at')
    except:
        print('Houve um erro na arbetura do arquivo!')
    else:
        try:
            a.write(f'{t}\n{j1}\n{j2}\n')
        except:
            print('Houve um erro na hora de escrever os dados')
        else:
            print('informações salvas.')
            a.close()


def adicionar_tabuleiro(arq, m):
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

