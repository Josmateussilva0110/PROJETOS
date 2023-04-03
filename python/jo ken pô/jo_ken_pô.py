from PAC.tipos.apresentar import *
from PAC.tipos.cadastrar import *
from random import randint
from os import system 

aux = False
while True:
    opcoes = ('PEDRA', 'PAPEL', 'TESOURA')
    cabeçalho('\033[1;31mJOGO DO PEDRA PAPEL E TESOURA\033[m')
    computador = randint(0, 2)
    if aux == False:
        nome = ler_nome('digite seu nome: ')
    opc = menu(['PEDRA', 'PAPEL', 'TESOURA'])
    animacao()
    print(f'\033[4;34m{linha()}\033[m')
    print(f'COMPUTADOR JOGOU \033[1;30;41m{opcoes[computador]}\033[m')
    print(f'JOGADOR(A) \033[1;30;43m{nome}\033[m JOGOU \033[1;30;42m{opcoes[opc]}\033[m')
    print(f'\033[4;34m{linha()}\033[m')
    juiz(computador, opc, nome)
    continuar = ler_int('deseja continuar (1- sim/2- não): ')
    if continuar == 2:
        break
    else:
        opc2 = ler_int('deseja trocar de nome (1- sim/2-não): ')
        if opc2 == 1:
            novo = ler_nome('novo nome: ')
            aux = True
        system('cls')
