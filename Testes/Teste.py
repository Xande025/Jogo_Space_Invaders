# import pygame
# import random
# import math
# from pygame import mixer

# # Inicialização do pygame
# pygame.init()

# # Definições da tela
# tela = pygame.display.set_mode((800, 600))

# # Título e ícone
# pygame.display.set_caption("Space Invaders")
# icone = pygame.image.load('IMG/nave.png')
# icone = pygame.transform.scale(icone, (32, 32))
# pygame.display.set_icon(icone)

# # Fundo
# fundo = pygame.image.load('IMG/Fundo.jpeg')
# fundo = pygame.transform.scale(fundo, (800, 600))

# # Som de fundo
# mixer.music.load('Som/thunderbird-game-over-9232.mp3')
# mixer.music.play(-1)

# # Jogador
# img_jogador = pygame.image.load('IMG/nave.png')
# img_jogador = pygame.transform.scale(img_jogador, (50, 50))
# jogadorX = 370
# jogadorY = 480
# jogadorX_mudanca = 3  # Ajuste de velocidade do jogador (mais lento)

# # Inimigo
# img_inimigo = []
# inimigoX = []
# inimigoY = []
# inimigoX_mudanca = []
# inimigoY_mudanca = []
# num_inimigos = 6

# for i in range(num_inimigos):
#     inimigo_img = pygame.image.load('IMG/inimigo.png')
#     inimigo_img = pygame.transform.scale(inimigo_img, (40, 40))
#     img_inimigo.append(inimigo_img)
#     inimigoX.append(random.randint(0, 735))
#     inimigoY.append(random.randint(50, 150))
#     inimigoX_mudanca.append(2)  # Velocidade mais lenta dos inimigos
#     inimigoY_mudanca.append(30)

# # Projetil
# img_projetil = pygame.image.load('IMG/projetil2.jpg')
# img_projetil = pygame.transform.scale(img_projetil, (20, 20))
# projetilX = 0
# projetilY = 480
# projetilY_mudanca = 5  # Ajuste de velocidade do projetil (mais lento)
# projetil_estado = "pronto"

# # Pontuação
# pontos = 0
# fonte = pygame.font.Font('freesansbold.ttf', 32)
# textoX = 10
# textoY = 10

# # Texto de Game Over
# fonte_game_over = pygame.font.Font('freesansbold.ttf', 64)

# def mostrar_pontuacao(x, y):
#     pontuacao = fonte.render("Pontos: " + str(pontos), True, (255, 255, 255))
#     tela.blit(pontuacao, (x, y))

# def game_over_text():
#     texto = fonte_game_over.render("GAME OVER", True, (255, 0, 0))
#     tela.blit(texto, (200, 250))

# def jogador(x, y):
#     tela.blit(img_jogador, (x, y))

# def inimigo(x, y, i):
#     tela.blit(img_inimigo[i], (x, y))

# def disparar_projetil(x, y):
#     global projetil_estado
#     projetil_estado = "fogo"
#     tela.blit(img_projetil, (x + 16, y + 10))

# def colisao(inimigoX, inimigoY, projetilX, projetilY):
#     distancia = math.sqrt((math.pow(inimigoX - projetilX, 2)) + (math.pow(inimigoY - projetilY, 2)))
#     return distancia < 27

# def colisao_com_jogador(inimigoX, inimigoY, jogadorX, jogadorY):
#     distancia = math.sqrt((math.pow(inimigoX - jogadorX, 2)) + (math.pow(inimigoY - jogadorY, 2)))
#     return distancia < 50

# # Controlador de FPS
# clock = pygame.time.Clock()

# # Loop principal
# executando = True
# game_over = False
# while executando:
#     # Controle de FPS (limita a 60 frames por segundo)
#     clock.tick(60)
    
#     # Fundo e cor de preenchimento
#     tela.fill((0, 0, 0))
#     tela.blit(fundo, (0, 0))

#     # Eventos do jogo
#     for evento in pygame.event.get():
#         if evento.type == pygame.QUIT:
#             executando = False

#         if evento.type == pygame.KEYDOWN:
#             if evento.key == pygame.K_LEFT:
#                 jogadorX_mudanca = -3  # Jogador se move mais devagar
#             if evento.key == pygame.K_RIGHT:
#                 jogadorX_mudanca = 3
#             if evento.key == pygame.K_SPACE:
#                 if projetil_estado == "pronto" and not game_over:
#                     projetilX = jogadorX
#                     disparar_projetil(projetilX, projetilY)

#         if evento.type == pygame.KEYUP:
#             if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
#                 jogadorX_mudanca = 0

#     # Movimento do jogador
#     jogadorX += jogadorX_mudanca
#     jogadorX = max(0, min(jogadorX, 736))

#     # Movimento do inimigo
#     for i in range(num_inimigos):
#         inimigoX[i] += inimigoX_mudanca[i]
#         if inimigoX[i] <= 0 or inimigoX[i] >= 736:
#             inimigoX_mudanca[i] *= -1
#             inimigoY[i] += inimigoY_mudanca[i]

#         # Verificar colisão com o jogador (Game Over)
#         if colisao_com_jogador(inimigoX[i], inimigoY[i], jogadorX, jogadorY):
#             for j in range(num_inimigos):
#                 inimigoY[j] = 2000  # Move todos os inimigos para fora da tela
#             game_over = True
#             break  # Sai do loop de inimigos se o jogo acabar

#         # Colisão com o projetil
#         if colisao(inimigoX[i], inimigoY[i], projetilX, projetilY):
#             projetilY = 480
#             projetil_estado = "pronto"
#             pontos += 1
#             inimigoX[i] = random.randint(0, 735)
#             inimigoY[i] = random.randint(50, 150)

#         # Desenha o inimigo na tela
#         inimigo(inimigoX[i], inimigoY[i], i)

#     # Movimento do projetil
#     if projetil_estado == "fogo":
#         disparar_projetil(projetilX, projetilY)
#         projetilY -= projetilY_mudanca

#     if projetilY <= 0:
#         projetilY = 480
#         projetil_estado = "pronto"

#     # Desenha o jogador
#     jogador(jogadorX, jogadorY)

#     # Exibir pontuação
#     mostrar_pontuacao(textoX, textoY)

#     # Exibir Game Over
#     if game_over:
#         game_over_text()

#     # Atualiza a tela
#     pygame.display.update()


