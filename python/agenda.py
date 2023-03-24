from FUNÇÕES.tipos.dados import *
from os import system


while True:
    print()
    opcao = menu(['cadastrar', 'alterar', 'apagar', 'listar', 'gravar', 'sair'])
    system('cls')
    if opcao == 6:
        break
    escolha(opcao)
