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

# --- CONFIGURAÇÃO DA ORDEM DAS FASES ---
# Dicionário mapeando a lógica: 
# "img_idx": qual imagem usar (0=Lã, 1=Cama, 2=Rato)
# "cnt_idx": qual índice do contador aumentar (0=Cama, 1=Lã, 2=Rato)
# "meta": quantos precisa pegar para passar de fase
fases_itens = [
    {"nome": "Lã",   "img_idx": 0, "cnt_idx": 1, "meta": 5}, # Fase 0: Lã
    {"nome": "Cama","img_idx": 1, "cnt_idx": 0, "meta": 3}, # Fase 1: Cama
    {"nome": "Rato", "img_idx": 2, "cnt_idx": 2, "meta": 3}  # Fase 2: Rato
]

# Variáveis globais de controle
item_ativo = None 
indice_fase = 0

# --- Variáveis de Interface e Pontuação ---
font = pygame.font.SysFont(None, 36) # Define a fonte para textos
contador = [0, 0, 0] # Contador: [0] para Peixes, [1] para Lãs
pygame.display.set_caption('Miaussão Impossível') # Define o título da janela

# --- Configuração das Telas de Estado (Menu) ---
imagens_tela_inicio = {
    0: pygame.image.load('Telas/tela_inicio_iniciar.png').convert(),    # Opção 0: Iniciar
    1: pygame.image.load('Telas/tela_inicio_instrucoes.png').convert(), # Opção 1: Instruções
    2: pygame.image.load('Telas/tela_inicio_sair.png').convert(),       # Opção 2: Sair
}

imagens_tela_vitoria = {
    0: pygame.image.load('Telas/tela_vitoria_recomecar.png').convert(),    
    1: pygame.image.load('Telas/tela_vitoria_sair.png').convert(),  
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
        # RESET DE VARIÁVEIS (Importante: resetar tudo ao iniciar o jogo)
        sprites.empty() # Limpa sprites antigos
        sprites.add(gato)
        
        contador = [0, 0, 0] # Zera pontuação
        indice_fase = 0      # Começa na fase 0 (Lã)
        
        # Cria o PRIMEIRO item do jogo
        dados_fase = fases_itens[indice_fase]
        # Spawna um pouco à frente do gato
        item_ativo = Coletavel(randint(400, 800), randint(300, 450), dados_fase["img_idx"])
        sprites.add(item_ativo)

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
            # --- LÓGICA DE COLISÃO UNIFICADA COM MUDANÇA DE CENÁRIO ---
            if item_ativo and gato.rect.colliderect(item_ativo.rect):
                # 1. Identifica a fase atual
                dados_fase = fases_itens[indice_fase]
                
                # 2. Coleta o item
                item_ativo.coletar_generico(contador, dados_fase["cnt_idx"])
                
                # 3. Verifica se bateu a meta
                qtd_atual = contador[dados_fase["cnt_idx"]]
                
                if qtd_atual < dados_fase["meta"]:
                    # --- AINDA NA MESMA FASE: RESPAWN ---
                    novo_x = gato.rect.x + randint(400, 900)
                    novo_y = randint(300, 450)
                    item_ativo = Coletavel(novo_x, novo_y, dados_fase["img_idx"])
                    sprites.add(item_ativo)
                    
                else:
                    # --- FASE CONCLUÍDA: MUDANÇA DE FASE E CENÁRIO ---
                    indice_fase += 1 # Avança o índice (ex: de 0 vai para 1)
                    
                    if indice_fase < len(fases_itens):
                        # A. Carrega o item da nova fase
                        dados_fase = fases_itens[indice_fase]
                        novo_x = gato.rect.x + randint(400, 900)
                        novo_y = randint(300, 450)
                        item_ativo = Coletavel(novo_x, novo_y, dados_fase["img_idx"])
                        sprites.add(item_ativo)
                        
                        # B. MUDANÇA DE CENÁRIO (O que você pediu!)
                        # Se indice_fase agora é 1 (segunda fase), o cenario deve ser 2.
                        cenario = indice_fase + 1 
                        vidas = 3 # Reseta as vidas ao mudar de fase (opcional)
                        
                        # Carrega o novo fundo
                        print(f"Mudando para Cenário {cenario}!")
                        imagem_fundo = pygame.image.load(f'Telas/tela{cenario}_vidas{vidas}.png').convert()
                        
                        # Reseta posições se necessário (ex: tirar gato de buraco)
                        # gato.rect.y = 400 

                    else:
                        # --- VITÓRIA (O JOGO ACABOU) ---
                        print("VOCÊ GANHOU!")
                        estado = 'Menu' # Tenta retornar ao estado de menu
                        opcao = 0
                        break
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
    
    elif estado == 'Vitoria':
        # Desenha a tela de vitória
        imagem_atual = imagens_tela_vitoria[opcao]
        tela.blit(imagem_atual, (0, 0))
    # Lógica para SAIR do programa (Se o estado for 'Sair' no loop externo)
    elif estado == 'Sair':
        pygame.quit()
        exit()
    pygame.display.flip() # Atualiza a tela (no loop externo, desenha Menu/Instruções)