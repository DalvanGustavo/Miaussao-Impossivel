import pygame
import time
from sys import exit
from random import randint
from gato import Gato
from coletavel import Coletavel
from obstaculos import Obstaculos
from pygame.locals import *
pygame.init()
# --- Configurações da Tela ---
LARGURA = 1080
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Miaussão Impossível')
# --- Grupos ---
sprites = pygame.sprite.Group()
grupo_obstaculos = pygame.sprite.Group()
grupo_plataformas = pygame.sprite.Group()  # mantido caso o módulo de plataformas exista
relogio = pygame.time.Clock()
# --- Física / Movimento ---
vel_y = 0
velocidade_gato = 10
gravidade = 0.8
chao_y = 500
forca_pulo = -20
# --- Câmera ---
CAMERA_OFFSET_LATERAL = 500  # mantive o valor do arquivo principal (500)
CAMERA_X_INICIAL = 0
# --- Personagem principal ---
gato = Gato()
POSICAO_LIMITE_INICIAL = gato.rect.centerx
# --- Fases / Itens ---
# NOTE: mantive a ordem do contador original do arquivo principal:
# contador[0] = Lã, contador[1] = Cama, contador[2] = Rato
fases_itens = [
    {"nome": "Lã",  "img_idx": 0, "cnt_idx": 0, "meta": 5},  # fase 0: Lã -> contador[0]
    {"nome": "Cama","img_idx": 1, "cnt_idx": 1, "meta": 5},  # fase 1: Cama -> contador[1]
    {"nome": "Rato","img_idx": 2, "cnt_idx": 2, "meta": 5},  # fase 2: Rato -> contador[2]
]
# --- Variáveis de controle (iniciadas no menu; alteradas ao começar o jogo) ---
item_ativo = None
indice_fase = 0
# --- Interface / Fonte ---
font = pygame.font.SysFont(None, 36)
# --- Carregamento das imagens do Placar (HUD) ---
tamanho_hud = (64, 64)
icone_la = pygame.image.load('Sprites/coletavel_1.png').convert_alpha()
icone_la = pygame.transform.scale(icone_la, tamanho_hud)
icone_cama = pygame.image.load('Sprites/coletavel_2.png').convert_alpha()
icone_cama = pygame.transform.scale(icone_cama, tamanho_hud)
icone_rato = pygame.image.load('Sprites/coletavel_3.png').convert_alpha()
icone_rato = pygame.transform.scale(icone_rato, (48, 64))
# --- Carregamento de imagens de telas ---
imagens_tela_inicio = {
    0: pygame.image.load('Telas/tela_inicio_iniciar.png').convert(),
    1: pygame.image.load('Telas/tela_inicio_instrucoes.png').convert(),
    2: pygame.image.load('Telas/tela_inicio_sair.png').convert(),
}
imagens_tela_vitoria = {
    0: pygame.image.load('Telas/tela_vitoria_recomecar.png').convert(),
    1: pygame.image.load('Telas/tela_vitoria_sair.png').convert(),
}
imagens_tela_derrota = {
    0: pygame.image.load('Telas/tela_gameover_recomecar.png').convert(),
    1: pygame.image.load('Telas/tela_gameover_sair.png').convert(),
}
imagem_instrucoes = pygame.image.load('Telas/tela_instrucoes.png').convert()
# --- Evento periódico de criação de obstáculo (a cada 300ms) ---
CRIAR_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(CRIAR_OBSTACULO, 300)
# --- Estado inicial do jogo ---
estado = 'Menu'
opcao = 0
n_opcoes = len(imagens_tela_inicio)
timer_tela_preta = 0
# --- Função auxiliar para (re)iniciar o jogo ---
def iniciar_jogo():
    global sprites, grupo_obstaculos, item_ativo, indice_fase
    global contador, cenario, vidas, camera_x, pos_mundo_fundo, imagem_fundo
    sprites.empty()
    grupo_obstaculos.empty()
    sprites.add(gato)
    # contador seguindo a ordem do arquivo principal: [Lã, Cama, Rato]
    contador = [0, 0, 0]
    indice_fase = 0
    # cria o primeiro item com base na fase 0 (spawn à frente do gato)
    dados_fase = fases_itens[indice_fase]
    item_ativo = Coletavel(randint(gato.rect.centerx + 200, gato.rect.centerx + 700),
                          randint(300, 450),
                          dados_fase["img_idx"])
    sprites.add(item_ativo)
    cenario = 1
    vidas = 3
    # câmera/fundo
    camera_x = CAMERA_X_INICIAL
    pos_mundo_fundo = 0
    imagem_fundo = pygame.image.load(f'Telas/tela{cenario}.png').convert()
# --- Main loop (um só loop, sem while aninhado) ---
running = True
# adiciona gato ao grupo de sprites para menu também (por segurança)
sprites.add(gato)
# variáveis do jogo que existem fora do estado 'Jogo'
camera_x = CAMERA_X_INICIAL
pos_mundo_fundo = 0
imagem_fundo = pygame.Surface((LARGURA, ALTURA))  # superfície vazia até começar
imagem_fundo.fill((135, 206, 235))
em_camera_lenta = False
timer_camera_lenta = 0
duracao_slowmo = 1500  # quanto tempo (ms) dura o efeito (2 segundos)
fps_jogo = 60          # variável para controlar o tick
proximo_estado = ''
while running:
    relogio.tick(fps_jogo)
    if estado == 'Jogo' and em_camera_lenta:
        agora = pygame.time.get_ticks()
        if agora - timer_camera_lenta > duracao_slowmo:
            # 1. Preparação para a cena final
            em_camera_lenta = False
            fps_jogo = 60 # Retorna o FPS ao normal para a animação ser fluida
            estado = 'Final_Caminhada'
            # 2. Setup do Cenário Final
            try:
                imagem_fundo = pygame.image.load('Telas/tela_fim.png').convert()
            except:
                imagem_fundo.fill((50, 50, 50))
            # Reset do Gato para começar fora da tela à esquerda
            gato.rect.x = -100 
            gato.rect.centery = chao_y
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == CRIAR_OBSTACULO and estado == 'Jogo':
            # cria um obstáculo se não houver nenhum (conforme lógica original)
            if len(grupo_obstaculos) == 0:
                novo_obstaculo = Obstaculos()
                novo_obstaculo.rect.x = camera_x + LARGURA + randint(200, 600)
                grupo_obstaculos.add(novo_obstaculo)
                sprites.add(novo_obstaculo)
        if event.type == KEYDOWN:
            # -- Menu --
            if estado == 'Menu':
                n_opcoes = len(imagens_tela_inicio)
            elif estado == 'Vitoria':
                n_opcoes = len(imagens_tela_vitoria)
            elif estado == 'Derrota':
                n_opcoes = len(imagens_tela_derrota)
            else:
                n_opcoes = 1 # Segurança para o estado 'Jogo' ou 'Instrucoes'
            # -- Navegação do Menu e Telas Finais --
            if estado in ('Menu', 'Vitoria', 'Derrota'):
                if event.key in (K_s, K_DOWN):
                    opcao = (opcao + 1) % n_opcoes
                elif event.key in (K_w, K_UP):
                    opcao = (opcao - 1 + n_opcoes) % n_opcoes
                # Confirmação (ENTER)
                elif event.key == K_RETURN:
                    if estado == 'Menu':
                        if opcao == 0: # Iniciar
                            iniciar_jogo()
                            estado = 'Jogo'
                        elif opcao == 1: # Instruções
                            estado = 'Instrucoes'
                        elif opcao == 2: # Sair
                            estado = 'Sair'
                    elif estado in ('Vitoria', 'Derrota'):
                        if opcao == 0: # Recomeçar
                            iniciar_jogo()
                            estado = 'Jogo'
                        elif opcao == 1: # Sair
                            estado = 'Sair'
            # -- Instruções --
            elif estado == 'Instrucoes':
                if event.key == K_ESCAPE:
                    estado = 'Menu'
                    opcao = 1
            # -- Jogo --
            elif estado == 'Jogo':
                if event.key in (K_ESCAPE,):
                    # volta para menu (mantendo a opção "Iniciar" selecionada)
                    estado = 'Menu'
                    opcao = 0
                # pulo tratado abaixo também para manter compatibilidade
                elif event.key in (K_UP, K_w):
                    if gato.rect.centery >= chao_y:
                        vel_y = forca_pulo  # local var; será sobrescrito no loop de movimento
            # -- Vitoria/Derrota: navegação para opções (reusar lógica do menu) --
            elif estado in ('Vitoria', 'Derrota'):
                if event.key in (K_s, K_DOWN):
                    opcao = (opcao + 1) % n_opcoes
                elif event.key in (K_w, K_UP):
                    opcao = (opcao - 1 + n_opcoes) % n_opcoes
                elif event.key == K_RETURN:
                    if opcao == 0:
                        iniciar_jogo()
                        estado = 'Jogo'
                    elif opcao == 1:
                        estado = 'Sair'
    # --- Estado: Sair ---
    if estado == 'Sair':
        running = False
        break
    # --- Render e lógica por estado ---
    tela.fill((0, 0, 0))
    if estado == 'Menu':
        tela.blit(imagens_tela_inicio[opcao], (0, 0))
    elif estado == 'Instrucoes':
        tela.blit(imagem_instrucoes, (0, 0))
    elif estado == 'Vitoria':
        tela.blit(imagens_tela_vitoria[opcao], (0, 0))
    elif estado == 'Derrota':
        tela.blit(imagens_tela_derrota[opcao], (0, 0))
    elif estado == 'Final_Caminhada':
        # 1. Desenha o fundo fixo
        tela.blit(imagem_fundo, (0, 0))
        # 2. Movimentação automática
        gato.rect.x += 5  # Velocidade da caminhada
        gato.andar_direita()
        gato.update()
        # 3. Desenha o gato
        tela.blit(gato.image, (gato.rect.x, gato.rect.y - 10))
        # 4. Condição de Finalização com Pausa
        if gato.rect.left > LARGURA - 500:
            # Mostra o último frame (cenário vazio) antes da pausa
            pygame.display.flip() 
            # Pausa dramática de 500ms (meio segundo)
            pygame.time.delay(500) 
            # Muda para a tela de Vitória
            estado = 'Vitoria'
            opcao = 0
            n_opcoes = len(imagens_tela_vitoria)
    elif estado == 'Jogo':
        # atualizações de movimento / física
        keys = pygame.key.get_pressed()
        # mov horiz
        if keys[K_RIGHT] or keys[K_d] or em_camera_lenta:
            gato.rect.centerx += velocidade_gato
            gato.andar_direita()
        elif keys[K_LEFT] or keys[K_a]:
            gato.rect.centerx -= velocidade_gato
            gato.andar_esquerda()
        else:
            gato.parado()
        # pulo (captura de tecla de pulo contínua opcional)
        if keys[K_UP] or keys[K_w]:
            if gato.rect.centery >= chao_y:
                vel_y = forca_pulo
        # A variável vel_y está sendo atualizada aqui; precisamos manter escopo correto:
        vel_y += gravidade
        gato.rect.centery += vel_y
        if gato.rect.centery >= chao_y:
            gato.rect.centery = chao_y
            vel_y = 0
        # Impede o gato de voltar além do limite inicial
        if gato.rect.centerx < POSICAO_LIMITE_INICIAL:
            gato.rect.centerx = POSICAO_LIMITE_INICIAL
        # câmera side-scrolling
        gato_pos_relativa_a_camera = gato.rect.centerx - camera_x
        DEAD_ZONE_LEFT = CAMERA_OFFSET_LATERAL
        DEAD_ZONE_RIGHT = LARGURA - CAMERA_OFFSET_LATERAL
        if gato.rect.centerx <= POSICAO_LIMITE_INICIAL:
            camera_x = 0
            pos_mundo_fundo = 0
        else:
            if gato_pos_relativa_a_camera > DEAD_ZONE_RIGHT:
                camera_x = gato.rect.centerx - DEAD_ZONE_RIGHT
            elif gato_pos_relativa_a_camera < DEAD_ZONE_LEFT:
                camera_x = gato.rect.centerx - DEAD_ZONE_LEFT
                if camera_x < 0:
                    camera_x = 0
        # atualiza obstaculos
        grupo_obstaculos.update()
        # remove obstaculos que saíram muito à esquerda
        for obs in list(grupo_obstaculos):
            if obs.rect.x < camera_x - 100:
                obs.kill()
        # desenha o fundo (efeito repetido)
        fundo_x_tela = pos_mundo_fundo - camera_x
        tela.blit(imagem_fundo, (fundo_x_tela, 0))
        fundo_x2_tela = pos_mundo_fundo + LARGURA - camera_x
        tela.blit(imagem_fundo, (fundo_x2_tela, 0))
        if fundo_x_tela + LARGURA < 0:
            pos_mundo_fundo += LARGURA
        if fundo_x_tela > 0 and gato.rect.centerx > POSICAO_LIMITE_INICIAL:
            pos_mundo_fundo -= LARGURA
        # desenha sprites com offset de câmera
        sprites.update()
        for sprite in sprites:
            pos_tela_x = sprite.rect.x - camera_x
            pos_tela_y = sprite.rect.y - 10  # camera_y fixo 10 no original
            tela.blit(sprite.image, (pos_tela_x, pos_tela_y))
        # colisões com obstaculos (cada colisão diminui vidas)
        colisoes = pygame.sprite.spritecollide(gato, grupo_obstaculos, True)
        for obstaculo in colisoes:
            vidas -= 1
        # desenha vidas (carregar imagem a cada alteração é ok, mas vamos tentar cache simples)
        if vidas:
            imagem_vidas = pygame.image.load(f'Sprites/vidas{vidas}.png').convert_alpha()
            rect_imagem = imagem_vidas.get_rect()
            rect_imagem.bottomright = (LARGURA - 40, 85)
            tela.blit(imagem_vidas, rect_imagem)
        if vidas <= 0:
            estado = 'Derrota'
            opcao = 0
            n_opcoes = len(imagens_tela_derrota)
            time.sleep(0.5)  # pausa breve antes de mudar de estado
        # --- Lógica de Respawn se o item saiu da tela pela esquerda ---
        if item_ativo and item_ativo.rect.right < camera_x:
            # O item saiu da tela, então removemos ele
            item_ativo.kill()
            # E criamos um novo lá na frente (mesma lógica de quando coleta)
            dados_fase = fases_itens[indice_fase]
            novo_x = gato.rect.x + randint(500, 900) # Cria à frente do gato
            novo_y = randint(250, 450)
            item_ativo = Coletavel(novo_x, novo_y, dados_fase["img_idx"])
            sprites.add(item_ativo)
        # --- Lógica de colisão com o coletável ativo ---
        if item_ativo and gato.rect.colliderect(item_ativo.rect):
            if indice_fase < len(fases_itens):
                dados_fase = fases_itens[indice_fase]
                idx_cnt = dados_fase["cnt_idx"]
                item_ativo.coletar_generico(contador, idx_cnt)
                qtd_atual = contador[idx_cnt]
            if qtd_atual < dados_fase["meta"]:
                # respawn do mesmo tipo um pouco à frente
                novo_x = gato.rect.x + randint(400, 900)
                novo_y = randint(250, 450)
                item_ativo = Coletavel(novo_x, novo_y, dados_fase["img_idx"])
                sprites.add(item_ativo)
            else:
                # fase concluída -> avança
                indice_fase += 1
                if indice_fase < len(fases_itens):
                    dados_fase = fases_itens[indice_fase]
                    novo_x = gato.rect.x + randint(400, 900)
                    novo_y = randint(250, 450)
                    item_ativo = Coletavel(novo_x, novo_y, dados_fase["img_idx"])
                    sprites.add(item_ativo)
                    # muda cenário (indicação: cenario = indice_fase + 1)
                    cenario = indice_fase + 1
                    # tenta carregar o novo fundo (se falhar, mantém o anterior)
                    imagem_fundo = pygame.image.load(f'Telas/tela{cenario}.png').convert()
                else:
                    # vitória completa
                    if not em_camera_lenta:
                        em_camera_lenta = True
                        fps_jogo = 15
                        timer_camera_lenta = pygame.time.get_ticks()
                        proximo_estado = 'Final_Caminhada' 
                        if item_ativo:
                            item_ativo.kill()
                            item_ativo = None
                    
        # textos de HUD 
        tela.blit(icone_la, (10, 10))  
        texto_la = font.render(f"{contador[0]}", True, (0, 0, 0))
        tela.blit(texto_la, (80, 35))
        tela.blit(icone_cama, (135, 10)) # Desenha o ícone
        texto_cama = font.render(f"{contador[1]}", True, (0, 0, 0))
        tela.blit(texto_cama, (210, 35))
        tela.blit(icone_rato, (250, 10)) # Desenha o ícone
        texto_rato = font.render(f"{contador[2]}", True, (0, 0, 0))
        tela.blit(texto_rato, (305, 35))
    # flip final do frame
    pygame.display.flip()
# encerra pygame ao sair do loop principal
pygame.quit()