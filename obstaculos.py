import pygame
import random
from utils import resource_path
class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagens = []
        for i in range(1,6):
            img = pygame.image.load(resource_path(f'Sprites/obstaculo_{i}.png')).convert_alpha()
            if i == 3:
                img_redimensionada = pygame.transform.scale(img, (250, 150))
            elif i == 4:
                img_redimensionada = pygame.transform.scale(img, (60, 60))
            else:
                img_redimensionada = pygame.transform.scale(img, (150, 150))
            self.imagens.append(img_redimensionada)
        # tipo do obstáculo (0 a 4)
        self.tipo = random.randint(0, 4)
        self.image = self.imagens[self.tipo]
        self.rect = self.image.get_rect()
        # comportamento por tipo
        if self.tipo == 3:
            # bola lançada
            self.velocidade = random.randint(4, 6)
            # bola lançada (voando)
            self.rect.y = random.randint(350, 480)
        else:
            # outros obstaculos
            self.velocidade = 0
        self.rect.x = 1080
        if self.tipo == 0 or self.tipo == 1 or self.tipo == 4:
            self.rect.y = 450
        elif self.tipo == 2:
            self.rect.y = 530
    def update(self):
        # todos vão para a esquerda
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()
