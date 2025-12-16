import pygame
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, r, g, b):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (r, g, b), (15, 15), 15)
        self.x = x            
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x # Coordenada de MUNDO X (fixa)
        self.y = y # Coordenada de MUNDO Y (fixa)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # Inicializa o rect na posição de mundo
        self.coletado = False  # flag para evitar print repetido
    def peixe(self, contador):
        if not self.coletado:
            self.coletado = True
            contador[0] += 1  # Incrementa o contador 
            self.kill()
    def la(self, contador):
        if not self.coletado:
            self.coletado = True
            contador[1] += 1  # Incrementa o contador  
            self.kill()