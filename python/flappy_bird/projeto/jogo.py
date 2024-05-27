from classes.principal.class_principal import *
import os

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    j = Jogo()
    modo = j.menu_inicial()
    j.run_game(caminho_config, modo)
