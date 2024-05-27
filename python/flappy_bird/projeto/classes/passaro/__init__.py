import os
import pygame


image_dir = os.path.join(os.path.dirname(__file__), 'imgs_birds')

# aumentar a escala da imagem 
image_birds = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bird3.png'))),
]

class Bird():
    imgs = image_birds
    #rotation_animation 
    max_rotation = 25
    rotation_speed = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.imgs[0]

    def jump_bird(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y
    
    def move_bird(self):
        self.time +=1

        #calcular o deslocamento
        displacement = 1.5 * (self.time**2) + self.speed * self.time
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2
        self.y += displacement

        #ajustar a animação
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.max_rotation:
                self.angle = self.max_rotation
        elif self.angle > -90:
            self.angle -= self.rotation_speed
    
    
    def draw_bird(self, tela):
        # escolher a imagem do passaro
        self.image_count += 1
        if self.image_count < self.animation_time:
            self.image = self.imgs[0]
        elif self.image_count < self.animation_time*2:
            self.image = self.imgs[1]
        elif self.image_count < self.animation_time*3:
            self.image = self.imgs[2]
        elif self.image_count < self.animation_time*4:
            self.image = self.imgs[1]
        elif self.image_count >= self.animation_time*4+1:
            self.image = self.imgs[0]
            self.image_count = 0
        
        #desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center= image_center)
        tela.blit(rotated_image, rectangle.topleft)
    

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
