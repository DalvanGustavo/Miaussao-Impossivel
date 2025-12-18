import pygame

class Coletavel(pygame.sprite.Sprite):
    """
    Classe Coletavel atualizada.
    Usa cache estático para carregar as imagens apenas uma vez.
    Método coletar_generico(contador, indice_contador) espera um LISTA 'contador'
    com a ordem: [la, cama, rato]  (isso mantém compatibilidade com o código principal)
    """
    IMAGENS_CACHE = []

    def __init__(self, x, y, indice_imagem):
        super().__init__()

        # Carrega imagens apenas uma vez
        if not Coletavel.IMAGENS_CACHE:
            try:
                for i in range(1, 4):  # coletavel_1.png .. coletavel_3.png
                    img = pygame.image.load(f'Sprites/coletavel_{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (64, 64))
                    Coletavel.IMAGENS_CACHE.append(img)
            except Exception as e:
                print(f"Erro ao carregar imagens do coletável: {e}")
                # fallback: superfície vermelha de erro
                erro_surf = pygame.Surface((64, 64)).convert_alpha()
                erro_surf.fill((255, 0, 0))
                Coletavel.IMAGENS_CACHE = [erro_surf, erro_surf, erro_surf]

        # proteger índice
        if 0 <= indice_imagem < len(Coletavel.IMAGENS_CACHE):
            self.image = Coletavel.IMAGENS_CACHE[indice_imagem]
        else:
            self.image = Coletavel.IMAGENS_CACHE[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.coletado = False

    def coletar_generico(self, contador, indice_contador):
        """
        contador: lista [la, cama, rato]
        indice_contador: qual índice incrementar (0, 1 ou 2)
        """
        if not self.coletado:
            self.coletado = True
            # segurança: garante tamanho mínimo
            if indice_contador >= len(contador):
                # amplia lista se necessário (não deve acontecer normalmente)
                while len(contador) <= indice_contador:
                    contador.append(0)
            contador[indice_contador] += 1
            self.kill()