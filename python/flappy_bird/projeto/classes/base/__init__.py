import os
import pygame


image_dir = os.path.join(os.path.dirname(__file__), 'imgs_base')

imagem_base = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'base.png')))

class Base():
    speed = 5
    width = imagem_base.get_width()
    image = imagem_base

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    
    def move_base(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        elif self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
    

    def draw_base(self, tela):
        tela.blit(self.image, (self.x1, self.y))
        tela.blit(self.image, (self.x2, self.y))
