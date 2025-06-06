import pygame
import random
import math
from pygame import mixer

# Inicialização do pygame
pygame.init()

# Definições da tela
tela = pygame.display.set_mode((800, 600))

# Título e ícone
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('IMG/nave.png')
icone = pygame.transform.scale(icone, (32, 32))
pygame.display.set_icon(icone)

# Fundo
fundo = pygame.image.load('IMG/Fundo.jpeg')
fundo = pygame.transform.scale(fundo, (800, 600))

# Som de fundo
mixer.music.load('Som/thunderbird-game-over-9232.mp3')
mixer.music.play(-1)

# Jogador
img_jogador = pygame.image.load('IMG/nave.png')
img_jogador = pygame.transform.scale(img_jogador, (50, 50))
jogadorX = 370
jogadorY = 480
jogadorX_mudanca = 0

# Inimigos
img_inimigo = []
inimigoX = []
inimigoY = []
inimigoX_mudanca = []
inimigoY_mudanca = []
num_inimigos = 6

for i in range(num_inimigos):
    inimigo_img = pygame.image.load('IMG/inimigo.png')
    inimigo_img = pygame.transform.scale(inimigo_img, (40, 40))
    img_inimigo.append(inimigo_img)
    inimigoX.append(random.randint(0, 735))
    inimigoY.append(random.randint(50, 150))
    inimigoX_mudanca.append(2)
    inimigoY_mudanca.append(30)

# Projetil do jogador
img_projetil = pygame.image.load('IMG/projetil2.jpg')
img_projetil = pygame.transform.scale(img_projetil, (20, 20))
projetilX = 0
projetilY = 480
projetilY_mudanca = 5
projetil_estado = "pronto"

# Tiro dos inimigos
img_tiro_inimigo = pygame.image.load('IMG/projetil2.jpg')
img_tiro_inimigo = pygame.transform.scale(img_tiro_inimigo, (20, 20))
tiros_inimigos = []

# Pontuação e Nível
pontos = 0
nivel = 1
fonte = pygame.font.Font('freesansbold.ttf', 32)
textoX = 10
textoY = 10

# Texto de Game Over
fonte_game_over = pygame.font.Font('freesansbold.ttf', 64)

def mostrar_pontuacao(x, y):
    pontuacao = fonte.render(f"Pontos: {pontos} Nível: {nivel}", True, (255, 255, 255))
    tela.blit(pontuacao, (x, y))

def game_over_text():
    texto = fonte_game_over.render("GAME OVER", True, (255, 0, 0))
    tela.blit(texto, (200, 250))

def jogador(x, y):
    tela.blit(img_jogador, (x, y))

def inimigo(x, y, i):
    tela.blit(img_inimigo[i], (x, y))

def disparar_projetil(x, y):
    global projetil_estado
    projetil_estado = "fogo"
    tela.blit(img_projetil, (x + 16, y + 10))

def disparar_tiro_inimigo(x, y):
    tiros_inimigos.append([x, y])

def colisao(obj1X, obj1Y, obj2X, obj2Y, distancia_minima):
    distancia = math.sqrt((math.pow(obj1X - obj2X, 2)) + (math.pow(obj1Y - obj2Y, 2)))
    return distancia < distancia_minima

def atualizar_nivel():
    global nivel, inimigoX_mudanca
    if pontos >= 20:
        nivel = 5
    elif pontos >= 15:
        nivel = 4
    elif pontos >= 10:
        nivel = 3
    elif pontos >= 5:
        nivel = 2
    
    # Ajuste de velocidade e tiro dos inimigos com base no nível
    for i in range(num_inimigos):
        if nivel >= 2:
            inimigoX_mudanca[i] = 3 if nivel == 2 else 4
        if nivel >= 3 and len(tiros_inimigos) < nivel:
            if random.randint(0, 100) < 2 * (nivel - 2):
                disparar_tiro_inimigo(inimigoX[i], inimigoY[i])

# Controlador de FPS
clock = pygame.time.Clock()

# Variável de controle de Game Over
executando = True
game_over = False
while executando:
    # Controle de FPS (limita a 60 frames por segundo)
    clock.tick(60)
    
    # Fundo e cor de preenchimento
    tela.fill((0, 0, 0))
    tela.blit(fundo, (0, 0))

    # Eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jogadorX_mudanca = -3
            if evento.key == pygame.K_RIGHT:
                jogadorX_mudanca = 3
            if evento.key == pygame.K_SPACE:
                if projetil_estado == "pronto" and not game_over:
                    projetilX = jogadorX
                    disparar_projetil(projetilX, projetilY)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogadorX_mudanca = 0

    # Movimento do jogador
    jogadorX += jogadorX_mudanca
    jogadorX = max(0, min(jogadorX, 736))

    # Atualizar nível e ajustar comportamento
    atualizar_nivel()

    # Movimento dos inimigos e controle de nível
    for i in range(num_inimigos):
        inimigoX[i] += inimigoX_mudanca[i]
        if inimigoX[i] <= 0:
            inimigoX_mudanca[i] = abs(inimigoX_mudanca[i])
            inimigoY[i] += inimigoY_mudanca[i]
        elif inimigoX[i] >= 736:
            inimigoX_mudanca[i] = -abs(inimigoX_mudanca[i])
            inimigoY[i] += inimigoY_mudanca[i]

        # Verifica se o inimigo saiu da tela pela parte inferior
        if inimigoY[i] > 600:
            inimigoY[i] = random.randint(50, 150)

        # Colisão com o jogador
        if colisao(inimigoX[i], inimigoY[i], jogadorX, jogadorY, 50):
            for j in range(num_inimigos):
                inimigoY[j] = 2000
            game_over = True
            break

        # Colisão com o projetil do jogador
        if colisao(inimigoX[i], inimigoY[i], projetilX, projetilY, 27):
            projetilY = 480
            projetil_estado = "pronto"
            pontos += 1
            inimigoX[i] = random.randint(0, 735)
            inimigoY[i] = random.randint(50, 150)

        inimigo(inimigoX[i], inimigoY[i], i)

    # Movimento do projetil do jogador
    if projetil_estado == "fogo":
        disparar_projetil(projetilX, projetilY)
        projetilY -= projetilY_mudanca
    if projetilY <= 0:
        projetilY = 480
        projetil_estado = "pronto"

    # Movimento dos tiros dos inimigos
    for tiro in tiros_inimigos[:]:
        tiro[1] += 5
        tela.blit(img_tiro_inimigo, (tiro[0], tiro[1]))
        if colisao(tiro[0], tiro[1], jogadorX, jogadorY, 30):
            game_over = True
            tiros_inimigos.clear()
            for j in range(num_inimigos):
                inimigoY[j] = 2000
            break
        if tiro[1] > 600:
            tiros_inimigos.remove(tiro)

    # Exibir pontuação e Game Over
    mostrar_pontuacao(textoX, textoY)
    if game_over:
        game_over_text()

    # Desenha o jogador por último para garantir visibilidade
    jogador(jogadorX, jogadorY)

    pygame.display.update()