import pygame
from gato import Gato
from peixe import coletavel1
from peixe import coletavel2


pygame.init()
screen = pygame.display.set_mode((600, 400))
x = 100
y = 100
vel_y = 0
gravidade = 0.8
chao_y = 300
clock = pygame.time.Clock()
running = True
todas_as_sprites = pygame.sprite.Group()
cat = Gato()
peixe = coletavel1(500, 300) #posição do peixe 1
peixe2 = coletavel1(800, 250) #posição do peixe 2
la = coletavel2(850, 300) #teste do coletável 2


todas_as_sprites.add(cat, peixe, peixe2, la)


contador = [0]  # Usando uma lista para permitir mutabilidade dentro do método collect
contador_la = [0]


font = pygame.font.SysFont(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += 3
        cat.andar_direita()
    elif keys[pygame.K_LEFT]:
        x -= 3
        cat.andar_esquerda()
    elif keys[pygame.K_UP]:
        y -= 15
    else:
        cat.parado()
    vel_y += gravidade
    y += vel_y
    if y >= chao_y:
        y = chao_y
        vel_y = 0


    # Camera follow
    camera_x = x - 300   
    camera_y = y - 200   
    cat.rect.topleft = (x - camera_x, y - camera_y)
    peixe.rect.topleft = (peixe.x - camera_x, peixe.y - camera_y)
    peixe2.rect.topleft = (peixe2.x - camera_x, peixe2.y - camera_y)
    la.rect.topleft = (la.x - camera_x, la.y - camera_y)

   #colisão coletavel 
    if cat.rect.colliderect(peixe.rect):
        peixe.collect(contador)
    if cat.rect.colliderect(peixe2.rect):
        peixe2.collect(contador)
    if cat.rect.colliderect(la.rect):
        la.collect(contador_la)



    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), (0 - camera_x, chao_y + 50 - camera_y, 1200, 100))  
    todas_as_sprites.draw(screen)
    todas_as_sprites.update()


    #HUD:

    texto = font.render(f"Peixes: {contador[0]}", True, (0,0,0))
    screen.blit(texto, (10,10))
    texto2 = font.render(f"Lã: {contador_la[0]}", True,(0,0,0) )
    screen.blit(texto2,(200,10))
    clock.tick(60)

    pygame.display.flip()

pygame.quit()