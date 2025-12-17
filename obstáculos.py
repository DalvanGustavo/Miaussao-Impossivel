import pygame
import random

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.imagens = []
        for i in range(5):
            img = pygame.image.load(
                f'Sprites/obstaculo_{i}.png'
            ).convert_alpha()
            self.imagens.append(img)

        # tipo do obstáculo (0 a 4)
        self.tipo = random.randint(0, 4)
        
        self.image = self.imagens[self.tipo]
        self.rect = self.image.get_rect()

        # nasce fora da tela
        self.rect.x = 1100
        self.rect.y = 500

        # comportamento por tipo
        if self.tipo == 4:
            # bola lançada
            self.velocidade = random.randint(10, 14)
            # bola lançada (voando)
            self.rect.y = random.randint(350, 480)

    def update(self):
        # todos vão para a esquerda
        self.rect.x -= self.velocidade

        if self.rect.right < 0:
            self.kill()
