import os
import pygame
import random

image_dir = os.path.join(os.path.dirname(__file__), 'imgs_pipe')

# aumentar a escala da imagem 
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'pipe.png')))

class Pipe():
    distance = 200
    speed = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.base = 0
        self.pipe_top = pygame.transform.flip(imagem_cano, False, True)
        self.pipe_base = imagem_cano
        self.passed = False
        self.set_height()
    

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.base = self.height + self.distance
    

    def move_pipe(self):
        self.x -= self.speed
    

    def draw_pipe(self, tela):
        tela.blit(self.pipe_top, (self.x, self.top))
        tela.blit(self.pipe_base, (self.x, self.base))
    

    #verificar colisoes 
    def clash(self, bird):
        mask_bird = bird.get_mask()
        mask_top = pygame.mask.from_surface(self.pipe_top)
        mask_base = pygame.mask.from_surface(self.pipe_base)


        distance_top = (self.x - bird.x, self.top - round(bird.y))
        distance_base = (self.x - bird.x, self.base - round(bird.y))

        point_top = mask_bird.overlap(mask_top, distance_top)
        point_base = mask_bird.overlap(mask_base, distance_base)

        if point_base or point_top:
            return True
        else:
            return False
