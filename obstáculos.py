import pygame
import random
class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagens = []
        for i in range(1,6):
            img = pygame.image.load(f'Sprites/obstaculo_{i}.png').convert_alpha()
            if i == 3:
                img_redimensionada = pygame.transform.scale(img, (250, 150))
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
            self.velocidade = random.randint(2, 4)
            # bola lançada (voando)
            self.rect.y = random.randint(350, 480)
        else:
            # outros obstáculos
            self.velocidade = 0
        if self.tipo == 0 or self.tipo == 1 or self.tipo == 4:
            self.rect.x = 1080
            self.rect.y = 450
        elif self.tipo == 2:
            self.rect.x = 1080
            self.rect.y = 530
        else:
            self.rect.x = 1080
            self.rect.y = 400
    def update(self):
        # todos vão para a esquerda
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()
