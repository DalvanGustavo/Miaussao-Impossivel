import pygame
from utils import resource_path
class Gato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_sprites = []
        for i in range(1,3):
            self.walk_sprites.append(pygame.image.load(resource_path(f'Sprites/gato_{i}.png')))
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.flip = False
        self.image = self.walk_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 500
    def andar_direita(self):
        self.flip = False
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.walk_sprites):
            self.current_sprite = 0
        self.image = self.walk_sprites[int(self.current_sprite)]
    def andar_esquerda(self):
        self.flip = True
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.walk_sprites):
            self.current_sprite = 0
        self.image = pygame.transform.flip(self.walk_sprites[int(self.current_sprite)], True, False)
    def parado(self):
        if self.flip:
            self.image = pygame.transform.flip(self.walk_sprites[0], True, False)
        else:
            self.image = self.walk_sprites[0]