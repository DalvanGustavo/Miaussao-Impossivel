import pygame
from gato import Gato
from coletavel import Coletavel
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
peixe = Coletavel(500, 300, 0, 0, 255)
peixe2 = Coletavel(800, 250, 0, 0, 255)
la = Coletavel(850, 300, 255, 0, 0)
font = pygame.font.SysFont(None, 36)
contador = [0,0]

todas_as_sprites.add(cat, peixe, peixe2, la)
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
    peixe2.rect.topleft = (peixe2.x - camera_x, peixe2.y - camera_y)
    la.rect.topleft = (la.x - camera_x, la.y - camera_y)

   #colisão coletavel 
    if cat.rect.colliderect(peixe.rect):
        peixe.peixe(contador)
    if cat.rect.colliderect(peixe2.rect):
        peixe2.peixe(contador)
    if cat.rect.colliderect(la.rect):
        la.la(contador) 

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), (0 - camera_x, chao_y + 50 - camera_y, 1200, 100))  

    texto = font.render(f"Peixes: {contador[0]}", True, (0,0,0))
    screen.blit(texto, (10,10))
    texto2 = font.render(f"Lã: {contador[1]}", True,(0,0,0) )
    screen.blit(texto2,(200,10))
    
    todas_as_sprites.draw(screen)
    todas_as_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()