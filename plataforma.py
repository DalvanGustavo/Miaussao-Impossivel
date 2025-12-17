import pygame
import random

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, largura_tela):
        super().__init__()

        self.image = pygame.image.load(
            'Sprites/plataforma.png'
        ).convert_alpha()

        self.rect = self.image.get_rect()

        # nasce fora da tela (direita)
        self.rect.x = largura_tela + random.randint(0, 300)

        # altura aleatória (ajuste conforme seu cenário)
        self.rect.y = random.randint(300, 450)

        # velocidade (opcionalmente variável)
        self.velocidade = random.randint(4, 7)

    def update(self):
        # anda para a esquerda
        self.rect.x -= self.velocidade

        # remove quando sair da tela
        if self.rect.right < 0:
            self.kill()
