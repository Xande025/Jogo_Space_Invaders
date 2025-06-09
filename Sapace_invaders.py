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
img_inimigo_vermelho = pygame.image.load('IMG/inimigo.png')
img_inimigo_vermelho = pygame.transform.scale(img_inimigo_vermelho, (40, 40))
num_inimigos = 6
cor_inimigo = ["normal"] * num_inimigos  # Lista para controlar o tipo de inimigo
vida_inimigo = [1] * num_inimigos  # Vida padrão dos inimigos
inimigo_vermelho_ativo = False
inimigoX = []
inimigoY = []
inimigoX_mudanca = []
inimigoY_mudanca = []

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
projetis_ativos = []  # Novo: lista de projeteis ativos

# Tiro dos inimigos
img_tiro_inimigo = pygame.image.load('IMG/projetil2.jpg')
img_tiro_inimigo = pygame.transform.scale(img_tiro_inimigo, (20, 20))
tiros_inimigos = []

# Pontuação e Nível
pontos = 0
nivel = 1
inimigos_mortos = 0  # Novo contador
vidas = 3  # Novo: vidas do jogador
max_disparos = 1  # Novo: quantidade máxima de disparos simultâneos
velocidade_projetil = 5  # Novo: velocidade do projetil
fonte = pygame.font.Font('freesansbold.ttf', 32)
textoX = 10
textoY = 10

# Texto de Game Over
fonte_game_over = pygame.font.Font('freesansbold.ttf', 64)

# Novo: Variáveis para escudo
escudo = 0  # 0 = sem escudo, >0 = escudo ativo
escudo_vida = 0  # Vida do escudo

def mostrar_pontuacao(x, y):
    texto = f"Pontos: {pontos} Nível: {nivel} Vidas: {vidas}"
    if escudo > 0:
        texto += f" Escudo: {escudo_vida}"
    pontuacao = fonte.render(texto, True, (255, 255, 255))
    tela.blit(pontuacao, (x, y))

def game_over_text():
    texto = fonte_game_over.render("GAME OVER", True, (255, 0, 0))
    tela.blit(texto, (200, 250))

def jogador(x, y):
    tela.blit(img_jogador, (x, y))

def inimigo(x, y, i):
    if cor_inimigo[i] == "vermelho":
        pygame.draw.rect(tela, (255, 0, 0), (x, y, 40, 40), 3)  # Borda vermelha
    tela.blit(img_inimigo[i], (x, y))

def disparar_projetil(x, y):
    global projetil_estado
    if nivel < 5:
        projetil_estado = "fogo"
        tela.blit(img_projetil, (x + 16, y + 10))
    elif nivel < 25:
        if len(projetis_ativos) < max_disparos:
            projetis_ativos.append([x, y])
    else:
        # Nível 25+: dispara 2 torpedos por vez
        if len(projetis_ativos) <= max_disparos - 2:
            projetis_ativos.append([x, y])
            projetis_ativos.append([x + 20, y])

def disparar_tiro_inimigo(x, y):
    tiros_inimigos.append([x, y])

def colisao(obj1X, obj1Y, obj2X, obj2Y, distancia_minima):
    distancia = math.sqrt((math.pow(obj1X - obj2X, 2)) + (math.pow(obj1Y - obj2Y, 2)))
    return distancia < distancia_minima

def atualizar_nivel():
    global nivel, inimigoX_mudanca, inimigos_mortos, vidas, max_disparos, velocidade_projetil, projetilY_mudanca, inimigo_vermelho_ativo, escudo, escudo_vida
    # Sobe de nível a cada 5 inimigos mortos
    if inimigos_mortos >= 5:
        nivel += 1
        inimigos_mortos = 0
        vidas += 1
        # Aumenta a velocidade dos inimigos até o nível 7
        if nivel <= 7:
            for i in range(num_inimigos):
                if inimigoX_mudanca[i] > 0:
                    inimigoX_mudanca[i] += 1
                else:
                    inimigoX_mudanca[i] -= 1
        # Nível 8+: inimigos ganham outra habilidade (exemplo: movimento diagonal)
        if nivel == 8:
            for i in range(num_inimigos):
                inimigoY_mudanca[i] += 10  # Ficam mais "agressivos" descendo mais rápido
        # Nível 10: inimigo vermelho aparece
        if nivel == 10 and not inimigo_vermelho_ativo:
            inimigo_vermelho_ativo = True
            cor_inimigo.append("vermelho")
            vida_inimigo.append(2)
            img_inimigo.append(img_inimigo_vermelho)
            inimigoX.append(random.randint(0, 735))
            inimigoY.append(random.randint(50, 150))
            inimigoX_mudanca.append(random.choice([-4, 4]))
            inimigoY_mudanca.append(40)
        # Nível 12: adiciona mais 2 inimigos vermelhos
        if nivel == 12:
            for _ in range(2):
                cor_inimigo.append("vermelho")
                vida_inimigo.append(2)
                img_inimigo.append(img_inimigo_vermelho)
                inimigoX.append(random.randint(0, 735))
                inimigoY.append(random.randint(50, 150))
                inimigoX_mudanca.append(random.choice([-4, 4]))
                inimigoY_mudanca.append(40)
    # A partir do nível 5, inimigos podem atirar
    if nivel >= 5:
        max_disparos = 3  # Pode dar até 3 disparos simultâneos
        velocidade_projetil = 10  # Disparos mais rápidos
        projetilY_mudanca = velocidade_projetil
        for i in range(num_inimigos):
            if len(tiros_inimigos) < nivel and random.randint(0, 100) < 2 * (nivel - 4):
                disparar_tiro_inimigo(inimigoX[i], inimigoY[i])
        # Nível 16+: inimigos vermelhos também disparam
        if nivel >= 16:
            for i in range(num_inimigos, len(inimigoX)):
                if len(tiros_inimigos) < nivel and random.randint(0, 100) < 2 * (nivel - 10):
                    disparar_tiro_inimigo(inimigoX[i], inimigoY[i])
    else:
        max_disparos = 1
        velocidade_projetil = 5
        projetilY_mudanca = velocidade_projetil

    if nivel == 15 and escudo == 0:
        escudo = 1
        escudo_vida = 2
    if nivel == 20:
        escudo = 1
        escudo_vida = 5
    if nivel >= 25:
        max_disparos = 6  # Permite até 3 duplas de torpedos simultâneos

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
    for i in range(len(inimigoX)):
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
            for j in range(len(inimigoX)):
                inimigoY[j] = 2000
            if escudo > 0 and escudo_vida > 0:
                escudo_vida -= 1
                if escudo_vida == 0:
                    escudo = 0
            else:
                vidas -= 1
                if vidas <= 0:
                    game_over = True
            break

        # Colisão com o projetil do jogador
        if colisao(inimigoX[i], inimigoY[i], projetilX, projetilY, 27):
            if cor_inimigo[i] == "vermelho":
                vida_inimigo[i] -= 1
                projetilY = 480
                projetil_estado = "pronto"
                if vida_inimigo[i] <= 0:
                    pontos += 2
                    inimigos_mortos += 1
                    inimigoX[i] = random.randint(0, 735)
                    inimigoY[i] = random.randint(50, 150)
                    vida_inimigo[i] = 2
            else:
                projetilY = 480
                projetil_estado = "pronto"
                pontos += 1
                inimigos_mortos += 1
                inimigoX[i] = random.randint(0, 735)
                inimigoY[i] = random.randint(50, 150)
                if inimigoX_mudanca[i] == 0:
                    inimigoX_mudanca[i] = random.choice([-2, 2])

        inimigo(inimigoX[i], inimigoY[i], i)

    # Movimento do projetil do jogador
    if nivel < 5:
        if projetil_estado == "fogo":
            disparar_projetil(projetilX, projetilY)
            projetilY -= projetilY_mudanca
        if projetilY <= 0:
            projetilY = 480
            projetil_estado = "pronto"
    else:
        # Nível 5+: múltiplos projéteis
        for proj in projetis_ativos[:]:
            tela.blit(img_projetil, (proj[0] + 16, proj[1] + 10))
            proj[1] -= projetilY_mudanca
            if proj[1] <= 0:
                projetis_ativos.remove(proj)

    # Colisão dos projéteis extras com inimigos
    if nivel >= 5:
        for proj in projetis_ativos[:]:
            for i in range(len(inimigoX)):
                if colisao(inimigoX[i], inimigoY[i], proj[0], proj[1], 27):
                    if cor_inimigo[i] == "vermelho":
                        vida_inimigo[i] -= 1
                        if proj in projetis_ativos:
                            projetis_ativos.remove(proj)
                        if vida_inimigo[i] <= 0:
                            pontos += 2
                            inimigos_mortos += 1
                            inimigoX[i] = random.randint(0, 735)
                            inimigoY[i] = random.randint(50, 150)
                            vida_inimigo[i] = 2
                    else:
                        pontos += 1
                        inimigos_mortos += 1
                        inimigoX[i] = random.randint(0, 735)
                        inimigoY[i] = random.randint(50, 150)
                        if inimigoX_mudanca[i] == 0:
                            inimigoX_mudanca[i] = random.choice([-2, 2])
                        if proj in projetis_ativos:
                            projetis_ativos.remove(proj)

    # Movimento dos tiros dos inimigos
    for tiro in tiros_inimigos[:]:
        tiro[1] += 5
        tela.blit(img_tiro_inimigo, (tiro[0], tiro[1]))
        if colisao(tiro[0], tiro[1], jogadorX, jogadorY, 30):
            if escudo > 0 and escudo_vida > 0:
                escudo_vida -= 1
                if escudo_vida == 0:
                    escudo = 0
                tiros_inimigos.remove(tiro)
                continue
            vidas -= 1
            tiros_inimigos.clear()
            for j in range(num_inimigos):
                inimigoY[j] = 2000
            if vidas <= 0:
                game_over = True
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