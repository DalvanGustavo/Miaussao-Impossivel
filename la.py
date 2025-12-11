import pygame

class coletavel2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 0), (15, 15), 15)
        self.x = x            
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.coletado = False  # ← flag para evitar print repetido

    def collect(self, contador_la):
        if not self.coletado:
            self.coletado = True
            contador_la[0] += 1  # Incrementa o contador
            print(f"Peixe coletado! {contador_la[0]}")  
            self.kill()

        

