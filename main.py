import pygame
from gato import Gato       # Importa a classe Gato (presumivelmente o personagem principal)
from coletavel import Coletavel # Importa a classe Coletavel (itens como peixes e lã)
from pygame.locals import * # Importa constantes do Pygame (K_UP, K_DOWN, QUIT, etc.)
from sys import exit        # Para sair do programa
from random import randint  # Para gerar números aleatórios (posições de itens)
pygame.init() # Inicializa todos os módulos do Pygame
# --- Configurações da Tela ---
largura = 1080
altura = 720 
tela = pygame.display.set_mode((largura, altura)) # Cria a janela do jogo
sprites = pygame.sprite.Group() # Cria um grupo para gerenciar todos os objetos visuais
relogio = pygame.time.Clock()   # Objeto para controlar a taxa de quadros (FPS)
# --- Variáveis de Física e Movimento ---
vel_y = 0               # Velocidade vertical atual (usada para pulo e gravidade)
velocidade_gato = 10    # Velocidade horizontal do Gato
gravidade = 0.8         # Aceleração vertical aplicada a cada frame
chao_y = 500            # Coordenada Y que representa o chão (onde o gato para de cair)
forca_pulo = -20        # Força aplicada ao pular (valor negativo para ir para cima)
# --- Variáveis de Câmera e Posição Inicial ---
CAMERA_OFFSET_LATERAL = 200 # Distância da borda onde a câmera começa a seguir (zona morta)
CAMERA_X_INICIAL = 0        # Posição X inicial da câmera
gato = Gato()               # Cria a instância do personagem principal
POSICAO_LIMITE_INICIAL = gato.rect.centerx # Limite esquerdo para o gato não andar para trás
# --- Criação dos Coletáveis Iniciais ---
# Calcula posições iniciais aleatórias para o Peixe
x_peixe = randint(gato.rect.centerx*2, 1080)
y_peixe = randint(400, 450)
peixe = Coletavel(x_peixe, y_peixe, 1) #MUDEI AQUIIII AAAAA
# Calcula posições iniciais aleatórias para a Lã
x_la = randint(gato.rect.centerx*2+1, 1080)
y_la = randint(400, 450)
la = Coletavel(x_la, y_la, 0) #MUDEI AQUIIII AAAAA
x_rato = randint(gato.rect.centerx*2+2, 1080)
y_rato = randint(400, 450)
rato = Coletavel(x_rato, y_rato, 2) #MUDEI AQUIIII AAAAA
# --- Variáveis de Interface e Pontuação ---
font = pygame.font.SysFont(None, 36) # Define a fonte para textos
contador = [0, 0, 0] # Contador: [0] para Peixes, [1] para Lãs
sprites.add(gato, peixe, la, rato) # Adiciona todos os objetos visuais ao grupo de sprites
pygame.display.set_caption('Miaussão Impossível') # Define o título da janela
# --- Configuração das Telas de Estado (Menu) ---
imagens_tela_inicio = {
    0: pygame.image.load('Telas/tela_inicio_iniciar.png').convert(),    # Opção 0: Iniciar
    1: pygame.image.load('Telas/tela_inicio_instrucoes.png').convert(), # Opção 1: Instruções
    2: pygame.image.load('Telas/tela_inicio_sair.png').convert(),       # Opção 2: Sair
}
imagem_instrucoes = pygame.image.load('Telas/tela_instrucoes.png').convert() 
estado = 'Menu' # Define o estado inicial do jogo
opcao = 0       # Opção selecionada no menu
n_opcoes = len(imagens_tela_inicio) # Número total de opções no menu
# --- LOOP PRINCIPAL DO PYGAME (Controla a transição de estados) ---
while True:
    # --- Checagem de Eventos do Sistema (Mouse, Teclado, Fechar) ---
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            # Lógica de navegação no MENU
            if estado == 'Menu':
                if event.key == K_s or event.key == K_DOWN:
                    opcao = (opcao + 1) % n_opcoes # Move para a próxima opção (cíclico)
                elif event.key == K_w or event.key == K_UP:
                    opcao = (opcao - 1 + n_opcoes) % n_opcoes # Move para a opção anterior (cíclico)
                elif event.key == K_RETURN:
                    if opcao == 0: 
                        estado = 'Jogo' # Inicia o jogo
                    elif opcao == 1: 
                        estado = 'Instruções' # Vai para a tela de instruções
                    elif opcao == 2: 
                        estado = "Sair" # Prepara para fechar
            # Lógica para sair das INSTRUÇÕES
            elif estado == 'Instruções':
                if event.key == K_ESCAPE:
                    estado = 'Menu' # Volta para o menu
                    opcao = 1       # Define a opção "Instruções" como selecionada ao retornar
            # Lógica para Pausar/Sair do JOGO
            elif estado == 'Jogo':
                 if event.key == K_ESCAPE:
                    estado = 'MENU' # Volta para o menu (CUIDADO: 'MENU' vs 'Menu')
                    opcao = 0       # Define a opção "Iniciar" como selecionada ao retornar
    # --- RENDERIZAÇÃO E TRANSIÇÃO DE TELA (Desenha a tela com base no estado) ---
    tela.fill((0, 0, 0)) # Limpa a tela com preto a cada frame
    if estado == 'Menu':
        # Desenha a tela de menu com a opção atualmente selecionada
        imagem_atual = imagens_tela_inicio[opcao]
        tela.blit(imagem_atual, (0, 0))
    elif estado == 'Instruções':
        # Desenha a tela de instruções
        tela.blit(imagem_instrucoes, (0, 0))
    elif estado == 'Jogo':
        # --- Configurações de Estado ao ENTRAR no Jogo (Problema: Essas variáveis resetam a cada frame!) ---
        cenario = 1
        vidas = 3
        las = 0
        camas = 0
        ratos = 0
        cenario1 = True 
        cenario2 = False
        cenario3 = False 
        # Variáveis de fundo e câmera
        largura_fundo = largura
        pos_mundo_fundo = 0
        camera_x = CAMERA_X_INICIAL
        DEAD_ZONE_LEFT = CAMERA_OFFSET_LATERAL
        DEAD_ZONE_RIGHT = largura - CAMERA_OFFSET_LATERAL
        # Carrega a imagem de fundo (CUIDADO: Carrega a imagem a cada frame se estiver no loop interno!)
        imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
        # --- LOOP INTERNO DE JOGABILIDADE (O "while True" aninhado é o problema estrutural) ---
        while True:
            relogio.tick(60) # Limita a 60 FPS
            # --- Checagem de Eventos REPETIDA (Necessária devido ao loop interno) ---
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    # Lógica de Pulo
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if gato.rect.centery >= chao_y:
                            vel_y = forca_pulo
            # --- Movimento Contínuo (Mover para Esquerda/Direita) ---
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                gato.rect.centerx += velocidade_gato
                gato.andar_direita()
            elif pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                gato.rect.centerx -= velocidade_gato
                gato.andar_esquerda()
            else:
                gato.parado()
            # Impede o gato de voltar além do limite inicial
            if gato.rect.centerx < POSICAO_LIMITE_INICIAL:
                gato.rect.centerx = POSICAO_LIMITE_INICIAL
            # --- Aplicação da Gravidade e Chão ---
            vel_y += gravidade
            gato.rect.centery += vel_y
            if gato.rect.centery >= chao_y:
                gato.rect.centery = chao_y
                vel_y = 0
            camera_y = 10 # Offset vertical da câmera (fixo)
            # --- Lógica da Câmera Side-Scrolling ---
            if gato.rect.centerx <= POSICAO_LIMITE_INICIAL:
                # Se o gato estiver no início, a câmera fica travada
                camera_x = 0
                pos_mundo_fundo = 0 
            else:
                # Calcula a posição relativa do gato na janela
                gato_pos_relativa_a_camera = gato.rect.centerx - camera_x
                # Se o gato sair da "zona morta" à direita, move a câmera
                if gato_pos_relativa_a_camera > DEAD_ZONE_RIGHT:
                    camera_x = gato.rect.centerx - DEAD_ZONE_RIGHT
                # Se o gato tentar voltar para a "zona morta" à esquerda, move a câmera
                elif gato_pos_relativa_a_camera < DEAD_ZONE_LEFT:
                    camera_x = gato.rect.centerx - DEAD_ZONE_LEFT
                    if camera_x < 0:
                        camera_x = 0 # Trava a câmera na posição zero
            # --- Desenho do Fundo (Efeito de Fundo Infinito) ---
            # Calcula a posição do fundo na tela, subtraindo o offset da câmera
            fundo_x_tela = pos_mundo_fundo - camera_x
            tela.blit(imagem_fundo, (fundo_x_tela, 0))
            # Desenha uma segunda imagem para criar o loop do fundo
            fundo_x2_tela = pos_mundo_fundo + largura_fundo - camera_x
            tela.blit(imagem_fundo, (fundo_x2_tela, 0)) 
            # Lógica para mover o ponto de referência do fundo quando o primeiro bloco sai da tela
            if fundo_x_tela + largura_fundo < 0:
                pos_mundo_fundo += largura_fundo
            # Lógica para mover o ponto de referência do fundo quando o fundo "volta" (raro em side-scrolling)
            if fundo_x_tela > 0 and gato.rect.centerx > POSICAO_LIMITE_INICIAL: 
                pos_mundo_fundo -= largura_fundo
            sprites.update() # Chama o método .update() de todos os sprites (para animação)
            # --- Desenho dos Sprites ---
            for sprite in sprites:
                # Ajusta a posição de desenho de cada sprite com base no offset da câmera
                pos_tela_x = sprite.rect.x - camera_x
                pos_tela_y = sprite.rect.y - camera_y
                tela.blit(sprite.image, (pos_tela_x, pos_tela_y))
            # --- Lógica de Colisão (Peixe) ---
            if gato.rect.colliderect(peixe.rect):
                peixe.peixe(contador) # Chama método que incrementa a contagem de peixes
                # Lógica de respawn do Peixe (até 3)
                if contador[0] < 3:
                    x_peixe_anterior = x_peixe
                    novo_x_min = x_peixe_anterior + 100
                    novo_x_max = novo_x_min + 400
                    x_peixe = randint(novo_x_min, novo_x_max)
                    y_peixe = randint(250, 300)
                    # Cria um NOVO objeto peixe e o adiciona
                    peixe = Coletavel(x_peixe, y_peixe, 1) #MUDEI AQUIIII AAAAA
                    sprites.add(peixe)
                else:
                    # Se 3 peixes foram coletados, move o sprite para fora da tela
                    peixe.rect.x = -5000 
                    peixe.rect.y = -5000
            # --- Lógica de Colisão (Lã) ---
            if gato.rect.colliderect(la.rect):
                la.la(contador) # Chama método que incrementa a contagem de lãs
                # Lógica de respawn da Lã (até 2)
                if contador[1] < 2:
                    x_la_anterior = x_la
                    novo_x_min = x_la_anterior + 100
                    novo_x_max = novo_x_min + 400
                    x_la = randint(novo_x_min, novo_x_max)
                    y_la = randint(250, 300)
                    # Cria um NOVO objeto lã e o adiciona
                    la = Coletavel(x_la, y_la, 0) #MUDEI AQUIIII AAAAA
                    sprites.add(la)
                else:
                    # Se 2 lãs foram coletadas, move o sprite para fora da tela
                    la.rect.x = -5000
                    la.rect.y = -5000
            if gato.rect.colliderect(rato.rect):
                rato.rato(contador) # Chama método que incrementa a contagem de lãs
                # Lógica de respawn da Lã (até 2)
                if contador[2] < 2:
                    x_rato_anterior = x_rato
                    novo_x_min = x_rato_anterior + 100
                    novo_x_max = novo_x_min + 400
                    x_rato = randint(novo_x_min, novo_x_max)
                    y_rato = randint(250, 300)
                    # Cria um NOVO objeto lã e o adiciona
                    
                    rato = Coletavel(x_rato, y_rato, 2) #MUDEI AQUIIII AAAAA
                    sprites.add(rato)
                else:
                    # Se 2 lãs foram coletadas, move o sprite para fora da tela
                    rato.rect.x = -5000
                    rato.rect.y = -5000
            # --- Lógica de Mudança de Fase (Cenário) ---
            if cenario1 and las == 3: # Se o cenario1 estiver ativo e las (lãs) for 3
                cenario = 2
                vidas = 3
                # Carrega o novo fundo (com novas vidas)
                imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
                cenario2 = True 
            if cenario2 and camas == 3: # Lógica para ir para o cenário 3
                cenario = 3
                vidas = 3
                imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
                cenario3 = True
            # --- Lógica de Fim de Jogo / Vitória ---
            if ratos == 3: # Se o contador de "ratos" (vitória) for 3
                imagens_tela_vitoria = { # Define as opções de vitória
                    0: pygame.image.load('Telas/tela_vitoria_recomecar.png').convert(),    
                    1: pygame.image.load('Telas/tela_vitoria_sair.png').convert(),  
                }
                estado = 'Menu' # Tenta retornar ao estado de menu
                opcao = 0 
                n_opcoes = len(imagens_tela_vitoria)
                # REPETIÇÃO DE EVENTOS para a tela de vitória (Problema de Loop Aninhado)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if estado == 'Menu':
                            # Lógica para navegação no menu de vitória
                            if event.key == K_s or event.key == K_DOWN:
                                opcao = (opcao + 1) % n_opcoes
                            elif event.key == K_w or event.key == K_UP:
                                opcao = (opcao - 1 + n_opcoes) % n_opcoes
                            elif event.key == K_RETURN:
                                if opcao == 0:
                                    estado = 'Jogo'
                                elif opcao == 1:
                                    estado = 'Sair'
            texto = font.render(f"Peixes: {contador[0]}", True, (0,0,0))
            tela.blit(texto, (10,10))
            texto2 = font.render(f"Lã: {contador[1]}", True,(0,0,0) )
            tela.blit(texto2,(200,10))
            texto3 = font.render(f"Rato: {contador[2]}", True,(0,0,0) )
            tela.blit(texto3,(350,10))
            sprites.update() # Atualiza os sprites (Novamente, antes do flip)
            pygame.display.flip() # Atualiza a tela (dentro do loop interno)
    # Lógica para SAIR do programa (Se o estado for 'Sair' no loop externo)
    elif estado == 'Sair':
        pygame.quit()
        exit()
    pygame.display.flip() # Atualiza a tela (no loop externo, desenha Menu/Instruções)
