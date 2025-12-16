import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 1080
altura = 720 

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Miaussão Impossível')

imagens_tela_inicio = {
    0: pygame.image.load('Telas/tela_inicio_iniciar.png').convert(),    
    1: pygame.image.load('Telas/tela_inicio_instrucoes.png').convert(), 
    2: pygame.image.load('Telas/tela_inicio_sair.png').convert(),       
}
imagem_instrucoes = pygame.image.load('Telas/tela_instrucoes.png').convert() 

estado = 'Menu'  
opcao = 0
n_opcoes = len(imagens_tela_inicio)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if estado == 'Menu':
                if event.key == K_s or event.key == K_DOWN:
                    opcao = (opcao + 1) % n_opcoes
                
                elif event.key == K_w or event.key == K_UP:
                    opcao = (opcao - 1 + n_opcoes) % n_opcoes

                elif event.key == K_RETURN:
                    if opcao == 0: 
                        estado = 'Jogo'
                    elif opcao == 1: 
                        estado = 'Instruções'
                    elif opcao == 2: 
                        estado = "Sair"
                        
            elif estado == 'Instruções':
                if event.key == K_ESCAPE:
                    estado = 'Menu'
                    opcao = 1 

            elif estado == 'Jogo':
                 if event.key == K_ESCAPE:
                    estado = 'MENU'
                    opcao = 0 

    tela.fill((0, 0 , 0))

    if estado == 'Menu':
        imagem_atual = imagens_tela_inicio[opcao]
        tela.blit(imagem_atual, (0, 0))

    elif estado == 'Instruções':
        tela.blit(imagem_instrucoes, (0, 0))
    
    elif estado == 'Jogo':
        cenario = 1
        vidas = 3
        las = 0
        camas = 0
        ratos = 0
        cenario1 = True 
        cenario2 = False
        cenario3 = False 

        imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
        tela.blit(imagem_fundo, (0, 0))

        class Gato(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.walk_sprites = []
                for i in range(1,3):
                    self.walk_sprites.append(pygame.image.load(f'Sprites/gato_{i}.png'))
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

        sprites = pygame.sprite.Group()
        gato = Gato()
        sprites.add(gato)

        relogio = pygame.time.Clock()
        velocidade_gato = 10

        while True:
            relogio.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
    
            tela.blit(imagem_fundo, (0, 0))
            sprites.draw(tela)
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                gato.andar_direita()
                gato.rect.centerx += velocidade_gato
            elif pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                gato.andar_esquerda()
                gato.rect.centerx -= velocidade_gato
            else:
                gato.parado()
            
            if cenario1 and las == 3:
                cenario = 2
                vidas = 3
                imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
                cenario2 = True 

            if cenario2 and camas == 3:
                cenario = 3
                vidas = 3
                imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
                cenario3 = True

            if ratos == 3:
                imagens_tela_vitoria = {
                    0: pygame.image.load('Telas/tela_vitoria_recomecar.png').convert(),    
                    1: pygame.image.load('Telas/tela_vitoria_sair.png').convert(),  
                }

                estado = 'Menu'
                opcao = 0 
                n_opcoes = len(imagens_tela_vitoria)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                    if event.type == KEYDOWN:
                        if estado == 'Menu':
                            if event.key == K_s or event.key == K_DOWN:
                                opcao = (opcao + 1) % n_opcoes
                            
                            elif event.key == K_w or event.key == K_UP:
                                opcao = (opcao - 1 + n_opcoes) % n_opcoes

                            elif event.key == K_RETURN:
                                if opcao == 0:
                                    estado = 'Jogo'
                                elif opcao == 1:
                                    estado = 'Sair'

            sprites.update()
            pygame.display.flip()
    
    elif estado == 'Sair':
        pygame.quit()
        exit()

    pygame.display.flip()