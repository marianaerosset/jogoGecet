import pygame
import random
import json

# 1. Inicialização do Pygame
pygame.init()
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo GECET")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 32, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 24)

# 2. Configuração das Categorias
categorias = [
    {"nome": "Arte", "cor": (255, 100, 100)},
    {"nome": "Ciência", "cor": (100, 255, 100)},
    {"nome": "Esportes", "cor": (100, 150, 255)},
    {"nome": "Entretenimento", "cor": (255, 200, 100)},
    {"nome": "Geografia", "cor": (100, 255, 255)},
    {"nome": "História", "cor": (255, 255, 100)}
]

# JSON
with open('perguntas.json', 'r', encoding='utf-8') as arq:
    banco_perguntas = json.load(arq)

# 3. Variáveis da Roleta Linear
LARGURA_BLOCO = 200
ALTURA_BLOCO = 120
LARGURA_TOTAL = LARGURA_BLOCO * len(categorias) # O tamanho total da "fita"

deslocamento_x = 0
velocidade = 0
atrito = 0.15
girando = False
categoria_selecionada = None

# Loop principal
rodando = True
while rodando:
    # --- GERENCIAMENTO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Aperte ESPAÇO para girar a roleta
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not girando:
                girando = True
                categoria_selecionada = None
                # Dá um impulso aleatório inicial para não cair sempre na mesma
                velocidade = random.uniform(30, 45) 

    # --- LÓGICA DO JOGO ---
    if girando:
        deslocamento_x += velocidade
        velocidade -= atrito # A roleta vai perdendo força
        
        if velocidade <= 0:
            velocidade = 0
            girando = False
            
            # Quando para, calculamos quem está no meio (x = 400)
            for i, cat in enumerate(categorias):
                x_virtual = (deslocamento_x + i * LARGURA_BLOCO) % LARGURA_TOTAL
                # A agulha fica no x = 400. Vemos se o bloco 'i' cobre esse ponto
                if x_virtual <= LARGURA_TELA/2 < x_virtual + LARGURA_BLOCO:
                    categoria_selecionada = cat["nome"]
                # Caso o bloco esteja quebrado na borda esquerda e a agulha estivesse lá
                elif x_virtual - LARGURA_TOTAL <= LARGURA_TELA/2 < x_virtual - LARGURA_TOTAL + LARGURA_BLOCO:
                    categoria_selecionada = cat["nome"]

    # --- DESENHO NA TELA ---
    tela.fill((40, 40, 50)) # Cor de fundo (cinza escuro)

    # 1. Desenhando a "Fita" da Roleta
    y_roleta = ALTURA_TELA // 2 - ALTURA_BLOCO // 2
    
    for i, cat in enumerate(categorias):
        # O truque do % (módulo) cria o loop infinito da roleta
        x = (deslocamento_x + i * LARGURA_BLOCO) % LARGURA_TOTAL
        
        # Desenhando o bloco
        retangulo = pygame.Rect(x, y_roleta, LARGURA_BLOCO, ALTURA_BLOCO)
        pygame.draw.rect(tela, cat["cor"], retangulo)
        pygame.draw.rect(tela, (255, 255, 255), retangulo, 3) # Borda branca
        
        # Texto do bloco
        texto = fonte_pequena.render(cat["nome"], True, (0, 0, 0))
        tela.blit(texto, (x + 20, y_roleta + 45))

        # Truque: desenhar um "fantasma" do bloco do lado esquerdo para manter a ilusão de fita contínua
        if x > LARGURA_TOTAL - LARGURA_BLOCO:
            ret_fantasma = pygame.Rect(x - LARGURA_TOTAL, y_roleta, LARGURA_BLOCO, ALTURA_BLOCO)
            pygame.draw.rect(tela, cat["cor"], ret_fantasma)
            pygame.draw.rect(tela, (255, 255, 255), ret_fantasma, 3)
            tela.blit(texto, (x - LARGURA_TOTAL + 20, y_roleta + 45))

    # 2. Desenhando o "Seletor" (A agulha central)
    meio_x = LARGURA_TELA // 2
    pygame.draw.line(tela, (255, 0, 0), (meio_x, y_roleta - 20), (meio_x, y_roleta + ALTURA_BLOCO + 20), 5)

    # 3. Textos de interface
    texto_instrucao = fonte_pequena.render("Pressione ESPAÇO para girar a roleta", True, (200, 200, 200))
    tela.blit(texto_instrucao, (220, 50))

    if categoria_selecionada and not girando:
        texto_resultado = fonte.render(f"Categoria: {categoria_selecionada}!", True, (255, 255, 255))
        tela.blit(texto_resultado, (meio_x - texto_resultado.get_width()//2, 400))
        
        texto_pergunta = fonte_pequena.render(banco_perguntas[categoria_selecionada], True, (255, 255, 0))
        tela.blit(texto_pergunta, (meio_x - texto_pergunta.get_width()//2, 450))

    # Atualiza a tela
    pygame.display.flip()
    relogio.tick(60) # Roda a 60 FPS

pygame.quit()