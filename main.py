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
clock = pygame.time.Clock()
running = True
todas_as_sprites = pygame.sprite.Group()
cat = Gato()
#criando os objetos coletáveis.
peixe = Coletavel(500, 300)
peixe2 = Coletavel(800, 250)
la = Coletavel(850, 300)


todas_as_sprites.add(cat)
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
    camera_x = x - 300   
    camera_y = y - 200   
    cat.rect.topleft = (x - camera_x, y - camera_y)
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), (0 - camera_x, chao_y + 50 - camera_y, 1200, 100))  
    todas_as_sprites.draw(screen)
    todas_as_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()