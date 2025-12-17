import pygame
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, indice):
        super().__init__()

        #carregando imagens
        self.imagens = []
        for i in range(3):
            img = pygame.image.load(f'Sprites/coletavel_{i + 1}.png').convert_alpha()
            img = pygame.transform.scale(img, (64, 64))
            self.imagens.append(img)

        #definindo imagem
        self.image = self.imagens[indice]

        #posicionamento
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

    def rato(self, contador):
        if not self.coletado:
            self.coletado = True
            contador[2] += 1  # Incrementa o contador  
            self.kill()