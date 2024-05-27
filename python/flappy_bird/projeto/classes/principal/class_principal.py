import neat.config
import pygame
import os
from classes.passaro import *
from classes.cano import *
from classes.base import *
import neat
import pygame.image


largura_tela = 500
altura_tela = 800


pygame.font.init()

class Jogo():
    def __init__(self):
        self.ai_jogando = True
        self.fonte_mensagem = pygame.font.SysFont('arial', 30)
        self.fonte_pontos = pygame.font.SysFont('arial', 40)
        self.imagem_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
        self.generation = 0
        self.points = 0
    
    def draw_menu(self, tela):
        tela.blit(self.imagem_fundo, (0, 0))
        titulo = self.fonte_pontos.render('Flappy Bird', 1, (255, 255, 255))
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, altura_tela // 4))
        
        texto_jogador = self.fonte_mensagem.render('Pressione J para jogar como jogador', 1, (255, 255, 255))
        tela.blit(texto_jogador, (largura_tela // 2 - texto_jogador.get_width() // 2, altura_tela // 2))
        
        texto_ia = self.fonte_mensagem.render('Pressione I para a IA jogar', 1, (255, 255, 255))
        tela.blit(texto_ia, (largura_tela // 2 - texto_ia.get_width() // 2, altura_tela // 2 + 50))
        
        pygame.display.update()
    

    def show_message(self, tela, message):
        texto = self.fonte_mensagem.render(message, 1, (255, 0, 0))
        tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
        pygame.display.update()

        waiting = True
        while waiting:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_y: 
                        return True
                    elif evento.key == pygame.K_n: 
                        return False
    
    def draw_tela(self, tela, birds, pipes, base, points):
        tela.blit(self.imagem_fundo, (0, 0))
        for bird in birds:
            bird.draw_bird(tela)

        for pipe in pipes:
            pipe.draw_pipe(tela)
        
        text = self.fonte_pontos.render(f'Pontuação: {points}', 1, (255, 255, 255))
        tela.blit(text, (largura_tela - 10 - text.get_width(), 10))

        if self.ai_jogando:
            texto = self.fonte_pontos.render(f"Geração: {self.generation}", 1, (255, 255, 255))
            tela.blit(texto, (10, 10))
        base.draw_base(tela)
        pygame.display.update()
    

    def menu_inicial(self):
        tela = pygame.display.set_mode((largura_tela, altura_tela))
        rodando = True
        while rodando:
            self.draw_menu(tela)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_j:
                        self.ai_jogando = False
                        return 1
                    if evento.key == pygame.K_i:
                        self.ai_jogando = True
                        return 2
    

    def main(self, genomas, config):
        self.generation +=1
        if self.ai_jogando:
            redes = []
            lista_genomas = []
            passaros = []
            for _, genoma in genomas:
                rede = neat.nn.FeedForwardNetwork.create(genoma, config)
                redes.append(rede)
                genoma.fitness = 0
                lista_genomas.append(genoma)
                passaros.append(Bird(230, 350))
        else:
            passaros = [Bird(230, 350)]
        chao = Base(730)
        canos = [Pipe(700)]
        tela = pygame.display.set_mode((largura_tela, altura_tela))
        clock = pygame.time.Clock()
        valid = True
        while valid:
            clock.tick(30)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    valid = False
                    pygame.quit()
                    quit()
                
                if not self.ai_jogando:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_k:
                            for passaro in passaros:
                                passaro.jump_bird()
            
            index_pipe = 0
            if len(passaros) > 0:
                if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].pipe_top.get_width()):
                    index_pipe = 1
            else:
                valid = False
                break
            
            for i, passaro in enumerate(passaros):
                passaro.move_bird()
                if self.ai_jogando:
                    lista_genomas[i].fitness += 0.1
                    output = redes[i].activate((passaro.y,
                                        abs(passaro.y - canos[index_pipe].height),
                                        abs(passaro.y - canos[index_pipe].base)))
                    if output[0] > 0.5:
                        passaro.jump_bird()
            
            chao.move_base()
            add_pipe = False
            remove_pipe = list()
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.clash(passaro):
                        self.points = 0
                        passaros.pop(i)
                        if self.ai_jogando:
                            lista_genomas[i].fitness -= 1
                            lista_genomas.pop(i)
                            redes.pop(i)
                        else:
                            if not self.show_message(tela, "Você perdeu! Continuar? (Y/N)"):
                                valid = False
                                pygame.quit()
                                quit()
                            else:
                                self.main(None, None)
                        
                    if not cano.passed and passaro.x > cano.x:
                        cano.passed = True
                        add_pipe = True
                cano.move_pipe()
                if cano.x + cano.pipe_top.get_width() < 0:
                    remove_pipe.append(cano)
            
            if add_pipe:
                self.points +=1
                canos.append(Pipe(600))
                if self.ai_jogando:
                    for genoma in lista_genomas:
                        genoma.fitness += 5
            for cano in remove_pipe:
                canos.remove(cano)
            
            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.image.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
                    self.points = 0
                    if self.ai_jogando:
                        lista_genomas.pop(i)
                        redes.pop(i)
                    else:
                        if not self.show_message(tela, "Você perdeu! Continuar? (Y/N)"):
                            valid = False
                            pygame.quit()
                            quit()
                        else:
                            self.main(None, None)

            
            self.draw_tela(tela, passaros, canos, chao, self.points)

    def run_game(self, config, flag):
        if flag == 1:
            self.main(None, None)
        else:
            self.ai_jogando = True
            input = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config)

            populacao = neat.Population(input)
            populacao.add_reporter(neat.StdOutReporter(True))
            populacao.add_reporter(neat.StatisticsReporter())
            populacao.run(self.main, 50)
