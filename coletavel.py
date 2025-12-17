import pygame

class Coletavel(pygame.sprite.Sprite):
    # Lista estática para guardar as imagens carregadas apenas uma vez
    IMAGENS_CACHE = []

    def __init__(self, x, y, indice_imagem):
        super().__init__()

        # --- CORREÇÃO: Carrega as imagens SOMENTE se a lista estiver vazia ---
        if not Coletavel.IMAGENS_CACHE:
            try:
                for i in range(1, 4): # Tenta carregar coletavel_1, coletavel_2, coletavel_3
                    img = pygame.image.load(f'Sprites/coletavel_{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (64, 64))
                    Coletavel.IMAGENS_CACHE.append(img)
            except Exception as e:
                print(f"Erro ao carregar imagens do coletável: {e}")
                # Cria um quadrado vermelho de erro caso não ache a imagem
                erro_surf = pygame.Surface((64, 64))
                erro_surf.fill((255, 0, 0))
                Coletavel.IMAGENS_CACHE = [erro_surf, erro_surf, erro_surf]

        # --- evitar erro de índice ---
        if 0 <= indice_imagem < len(Coletavel.IMAGENS_CACHE):
            self.image = Coletavel.IMAGENS_CACHE[indice_imagem]
        else:
            self.image = Coletavel.IMAGENS_CACHE[0]

        # Posicionamento
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.coletado = False

    def coletar_generico(self, contador, indice_contador):
        # Verifica se já foi coletado para evitar contagem dupla num mesmo frame
        if not self.coletado:
            self.coletado = True
            contador[indice_contador] += 1
            self.kill() # Remove este objeto dos grupos de sprites