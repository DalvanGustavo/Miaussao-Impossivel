import pygame
from gato import Gato
from coletavel import Coletavel
from random import randint
pygame.init()
screen = pygame.display.set_mode((600, 400))
x = 100
y = 100
vel_y = 0
gravidade = 0.8
chao_y = 300
forca_pulo = -15
clock = pygame.time.Clock()
running = True
todas_as_sprites = pygame.sprite.Group()
cat = Gato()
#criando os objetos coletáveis.
x_peixe = randint(x*2,600)
y_peixe = randint(250,300)
x_la = randint(x*2+1, 800)
y_la = randint(250, 300)
peixe = Coletavel(x_peixe, y_peixe, 0, 0, 255)
la = Coletavel(x_la, y_la, 255, 0, 0)
font = pygame.font.SysFont(None, 36)
contador = [0,0]

todas_as_sprites.add(cat, peixe, la)

#Configuração do Chão
camera_x_inicial = x - 300
largura_bloco = 400
lista_chaos = []
cor1 = (0, 255, 0)
cor2 = (255, 255, 0)
cor3 = (255, 0, 0)
lista_cores_disponiveis = [cor1, cor2, cor3]

for i in range(4):
    pos_x_real = camera_x_inicial + (i * largura_bloco)
    rect = pygame.Rect(pos_x_real, chao_y + 50, largura_bloco, 600)
    cor_atual = lista_cores_disponiveis[i % 3]
    lista_chaos.append([rect, cor_atual])
#Fim configuração do chão

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y >= chao_y:
                    vel_y = forca_pulo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += 3
        cat.andar_direita()
    elif keys[pygame.K_LEFT]:
        x -= 3
        cat.andar_esquerda()
    else:
        cat.parado()
    vel_y += gravidade
    y += vel_y
    if y >= chao_y:
        y = chao_y
        vel_y = 0
    camera_x = x - 300   
    camera_y = y - 200 
    cat.rect.topleft = (x - camera_x, y - camera_y)
    peixe.rect.topleft = (peixe.x - camera_x, peixe.y - camera_y)
    la.rect.topleft = (la.x - camera_x, la.y - camera_y)

   #colisão coletavel 
    if cat.rect.colliderect(peixe.rect):
        peixe.peixe(contador)
        if contador[0] < 3:
            x_peixe_anterior = x_peixe
            novo_x_min = x_peixe_anterior + 100
            novo_x_max = novo_x_min + 400
            x_peixe = randint(novo_x_min, novo_x_max)
            y_peixe = randint(250, 300)
            peixe = Coletavel(x_peixe, y_peixe, 0, 0, 255)
            todas_as_sprites.add(peixe)
        else:
            peixe.rect.x = -5000 
            peixe.rect.y = -5000
    if cat.rect.colliderect(la.rect):
        la.la(contador)
        if contador[1] < 2:
            x_la_anterior = x_la
            novo_x_min = x_la_anterior + 100
            novo_x_max = novo_x_min + 400
            x_la = randint(novo_x_min, novo_x_max)
            y_la = randint(250, 300)
            la = Coletavel(x_la, y_la, 255, 0, 0)
            todas_as_sprites.add(la)
        else:
            la.rect.x = -5000
            la.rect.y = -5000
    screen.fill((255, 255, 255))

    #Processo de construção do chão
    ultimo_dado = lista_chaos[-1]
    ultimo_rect = ultimo_dado[0]
    ultima_cor = ultimo_dado[1]
    while ultimo_rect.right - camera_x < 800:
        novo_rect = pygame.Rect(ultimo_rect.right, chao_y + 50, largura_bloco, 600)
        indice_atual = lista_cores_disponiveis.index(ultima_cor)
        proximo_indice = (indice_atual + 1) % 3
        nova_cor = lista_cores_disponiveis[proximo_indice]
        novo_dado = [novo_rect, nova_cor]
        lista_chaos.append(novo_dado)
        ultimo_dado = novo_dado
        ultimo_rect = novo_dado[0]
        ultima_cor = novo_dado[1]
    if lista_chaos[0][0].right - camera_x < -400:
        lista_chaos.pop(0)
    for dado in lista_chaos:
        rect = dado[0]
        cor = dado[1]
        pygame.draw.rect(screen, cor, (rect.x - camera_x, rect.y - camera_y, largura_bloco, 600))
    #Fim de construção do chão
     
    texto = font.render(f"Peixes: {contador[0]}", True, (0,0,0))
    screen.blit(texto, (10,10))
    texto2 = font.render(f"Lã: {contador[1]}", True,(0,0,0) )
    screen.blit(texto2,(200,10))
    
    todas_as_sprites.draw(screen)
    todas_as_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()