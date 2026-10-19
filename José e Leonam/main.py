import pygame  # Permite utilizar os comandos da biblioteca pygame
from pygame.locals import *  # Importa as funções do pygame local
from sys import exit  # Importa a função exit

pygame.init()  # Função que inicia o jogo

# --- SISTEMA DE PONTUAÇÃO E FONTE ---
Pontos = 0
nome_da_fonte = pygame.font.SysFont("arial", 40, True, False)
fonte_game_over = pygame.font.SysFont("arial", 80, True, False)

largura = 1920  # Varíavel com a largura(x) da tela
altura = 1080  # Varíavel com a altura(y) da tela

# --- SISTEMA DE FASES E FÍSICA ---
Fase = 1
gravidade = 1       
Gravidade_Y = 0

# --- CARREGAMENTO DE AUDIO ---
# Evita erro caso o arquivo de música não esteja na pasta durante testes
try:
    Musica_de_fundo = pygame.mixer.music.load("What Went Wrong.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Aviso: Música 'What Went Wrong.mp3' não encontrada.")
    
try:
    Som_Pulo = pygame.mixer.Sound("Jump.mp3")
    Som_Pulo.set_volume(0.3)
except:
    print("Aviso: Som 'Jump.mp3' não encontrado.")
    Som_Pulo = None

try:
    Som_Morte = pygame.mixer.Sound("weird-route-jingle.mp3")
    Som_Morte.set_volume(0.4)
except:
    print("Aviso: Som 'weird-route-jingle.mp3' não encontrado.")
    Som_Morte = None

try:
    Som_Door = pygame.mixer.Sound("abandon-weird-route (1).mp3")
    Som_Door.set_volume(0.4)
except:
    print("Aviso: Som 'abandon-weird-route (1).mp3' não encontrado.")
    Som_Door = None

try:
    Som_GameOver = pygame.mixer.Sound("Deltarune-Chapter-5-Weird-Route-OST-Monologue.mp3")
    Som_GameOver.set_volume(0.5)
except:
    print("Aviso: Som 'game-over.mp3' não encontrado.")
    Som_GameOver = None

# Propriedades do player
Player_X = 100
Player_Y = 900
Velocidade_Player_X = 10  
jogador_rect = pygame.Rect(Player_X - 80, Player_Y - 80, 160, 160)

# Propriedades bases da Porta
Door_X = 100
Door_Y = 200
Door_Pos_X = 1600
Door_Pos_Y = 40

Plataforma = []
Plataforma_Mortal = []

# --- FUNÇÃO GERADORA DE MAPAS PADRONIZADOS ---
def carregar_fase(numero_da_fase):
    global Plataforma_Mortal, Plataforma, Door_Pos_X, Door_Pos_Y, gravidade, Player_X, Player_Y
    
    Plataforma = [] 
    Plataforma_Mortal = []

    if numero_da_fase == 1:
        gravidade = 1 
        Player_X = 100
        Player_Y = 900
        Door_Pos_X = 1600
        Door_Pos_Y = 110 
        
        plat_x = 400
        plat_y = 890 
        Plataforma_Mortal.append(pygame.Rect(500,980,1420,100))
        for i in range(4):
            novo_bloco = pygame.Rect(plat_x, plat_y, 100, 40)
            Plataforma.append(novo_bloco)
            plat_x += 300  
            plat_y -= 150   

    elif numero_da_fase == 2:
        gravidade = 0.25 
        Player_X = 100
        Player_Y = 900
        Door_Pos_X = 1750
        Door_Pos_Y = 700
        Plataforma.append(pygame.Rect(350, 750, 250, 40))
        Plataforma_Mortal.append(pygame.Rect(800, 600, 250, 40))
        Plataforma_Mortal.append(pygame.Rect(1300, 500, 1420, 40))
        Plataforma_Mortal.append(pygame.Rect(800, 600, 50, 380))
        Plataforma_Mortal.append(pygame.Rect(1300, 100, 50, 400))

    elif numero_da_fase == 3:
        gravidade = 2.5 
        Player_X = 100
        Player_Y = 900
        Door_Pos_X = 910
        Door_Pos_Y = 250
        Plataforma.append(pygame.Rect(300, 890, 200, 40))
        Plataforma.append(pygame.Rect(600, 790, 200, 40))
        Plataforma.append(pygame.Rect(900, 690, 120, 40))  
        Plataforma.append(pygame.Rect(1200, 790, 200, 40))
        Plataforma.append(pygame.Rect(1500, 890, 200, 40))
        
    elif numero_da_fase == 4:
        gravidade = -1 
        Player_X = 100
        Player_Y = 180
        Door_Pos_X = 1600
        Door_Pos_Y = 730
        
        plat_x = 400
        plat_y = 100  
        for i in range(7):
            novo_bloco = pygame.Rect(plat_x, plat_y, 100, 40)
            Plataforma.append(novo_bloco)
            plat_x += 200  
            plat_y += 100   

    elif numero_da_fase == 5:
        gravidade = -2.5
        Player_X = 100
        Player_Y = 180
        
        Door_Pos_X = 1700
        Door_Pos_Y = 400
        
        Plataforma.append(pygame.Rect(300, 150, 200, 40))
        Plataforma.append(pygame.Rect(600, 220, 200, 40))
        Plataforma.append(pygame.Rect(900, 300, 200, 40))
        Plataforma.append(pygame.Rect(1200, 380, 200, 40))
        Plataforma.append(pygame.Rect(1450, 450, 200, 40))

    elif numero_da_fase == 6:
        gravidade = -0.25
        Player_X = 1840
        Player_Y = 180
        
        Door_Pos_X = 200
        Door_Pos_Y = 730
        
        Plataforma.append(pygame.Rect(400, 350, 300, 40))
        Plataforma.append(pygame.Rect(900, 500, 300, 40))
        Plataforma.append(pygame.Rect(1400, 650, 300, 40))
# --- FUNÇÃO DE TELA DE GAME OVER ---
def gerenciar_game_over():
    global Pontos, Fase, Gravidade_Y
    if Som_GameOver: Som_GameOver.play()
    
    while True:
        tela.fill((0, 0, 0))
        
        # Renderiza os textos do placar de fim de jogo
        texto_go = fonte_game_over.render("GAME OVER", True, (255, 0, 0))
        texto_instrucao = nome_da_fonte.render("Pressione ESPAÇO para reiniciar ou ESC para sair", True, (255, 255, 255))
        
        # Cola os textos centralizados
        tela.blit(texto_go, (largura // 2 - texto_go.get_width() // 2, altura // 2 - 100))
        tela.blit(texto_instrucao, (largura // 2 - texto_instrucao.get_width() // 2, altura // 2 + 50))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:  # Reseta o jogo por completo
                    Pontos = 0
                    Fase = 1
                    Gravidade_Y = 0
                    carregar_fase(Fase)
                    return  # Sai da tela de game over e volta ao while principal
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Inicializa o mapa da Fase 1 antes de entrar no while
carregar_fase(Fase)

tela = pygame.display.set_mode((largura, altura))  # Função que define o tamanho da tela
pygame.display.set_caption("Space Galaxy")  # Nome do programa
relogio = pygame.time.Clock()  # criação de FPS

while True:  # Loop principal que faz o jogo rodar
    relogio.tick(60)  # limita o FPS do jogo
    tela.fill((0, 0, 0))

    for event in pygame.event.get():  # Verifica se algum evento ocorreu
        if event.type == QUIT:
            pygame.quit()
            exit()

    #MOVIMENTAÇÃO HORIZONTAL
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        Player_X += Velocidade_Player_X
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        Player_X -= Velocidade_Player_X

    if Player_X < 80:
        Player_X = 80  # Trava o jogador na parede esquerda
    if Player_X > 1840:
        Player_X = 1840  # Trava o jogador na parede direita (1920 - 80)

    # Atualiza a posição X do Rect antes de checar colisões laterais
    jogador_rect.centerx = Player_X

    # Checa colisão horizontal nas plataformas (Paredes laterais)
    for i in range(len(Plataforma)):
        if jogador_rect.colliderect(Plataforma[i]):
            if (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]):
                jogador_rect.right = Plataforma[i].left
            if (teclas[pygame.K_a] or teclas[pygame.K_LEFT]):
                jogador_rect.left = Plataforma[i].right
            Player_X = jogador_rect.centerx

    # MOVIMENTAÇÃO VERTICAL (FÍSICA ADAPTATIVA)
    if gravidade > 0:
        no_chao = Player_Y >= 900  
        if not no_chao:
            for plat in Plataforma:
                if (
                    jogador_rect.bottom == plat.top
                    and jogador_rect.right > plat.left
                    and jogador_rect.left < plat.right
                ):
                    no_chao = True
                    break
        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and no_chao:
            if Som_Pulo: Som_Pulo.play()
            if gravidade > 2:
                Gravidade_Y = -35  
            else:
                Gravidade_Y = -20  
    else:
        no_teto = Player_Y <= 180  
        if not no_teto:
            for plat in Plataforma:
                if (
                    jogador_rect.top == plat.bottom
                    and jogador_rect.right > plat.left
                    and jogador_rect.left < plat.right
                ):
                    no_teto = True
                    break
        if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and no_teto:
            if Som_Pulo: Som_Pulo.play()
            if gravidade < -2:
                Gravidade_Y = 35  
            else:
                Gravidade_Y = 20  

    # Aplicação contínua da gravidade
    Gravidade_Y += gravidade
    Player_Y += Gravidade_Y

    # Trava para impedir atravessar o teto nas fases de gravidade normal
    if Player_Y <= 180 and gravidade > 0:
        Player_Y = 180
        Gravidade_Y = 0

    # Atualiza a posição Y do Rect antes de checar colisões verticais
    jogador_rect.centery = Player_Y

    # Checa colisão vertical nas plataformas normais
    for i in range(len(Plataforma)):
        if jogador_rect.colliderect(Plataforma[i]):
            if gravidade > 0:
                if Gravidade_Y > 0:  
                    jogador_rect.bottom = Plataforma[i].top
                    Gravidade_Y = 0
                elif Gravidade_Y < 0:  
                    jogador_rect.top = Plataforma[i].bottom
                    Gravidade_Y = 0
            else:
                if Gravidade_Y < 0:  
                    jogador_rect.top = Plataforma[i].bottom
                    Gravidade_Y = 0
                elif Gravidade_Y > 0:  
                    jogador_rect.bottom = Plataforma[i].top
                    Gravidade_Y = 0
            Player_Y = jogador_rect.centery

    # --- SISTEMA DE COLISÃO FATAL COM AS PLATAFORMAS MORTAIS ---
    for bloco_mortal in Plataforma_Mortal:
        if jogador_rect.colliderect(bloco_mortal):
            if Som_Morte: Som_Morte.play()
            
            if gravidade > 0:
                Player_X = 80
                Player_Y = 900
            else:
                Player_X = 100
                Player_Y = 180
                
            Gravidade_Y = 0
            Pontos = Pontos - 50

    # CONDICIONAL DE GAME OVER SE OS PONTOS FICAREM NEGATIVOS
    if Pontos < 0:
        gerenciar_game_over()

    # Limitação das Bordas Superior e Inferior do Cenário
    if gravidade > 0:
        if Player_Y >= 900:
            Player_Y = 900
            Gravidade_Y = 0
            jogador_rect.centery = Player_Y
    else:
        if Player_Y <= 180:
            Player_Y = 180
            Gravidade_Y = 0
            jogador_rect.centery = Player_Y

    # 3. DESENHOS NA TELA
    if gravidade > 0:
        pygame.draw.line(tela, (255, 255, 255), (0, 1030), (1920, 1030), 100) # Linha do Chão
    else:
        pygame.draw.line(tela, (255, 255, 255), (0, 50), (1920, 50), 100)   # Linha do Teto

    # Desenha as plataformas seguras (Azul)
    for i in range(len(Plataforma)):
        pygame.draw.rect(tela, (0, 0, 255), Plataforma[i])

    # Desenha as plataformas mortais (Vermelho)
    for i in range(len(Plataforma_Mortal)):
        pygame.draw.rect(tela, (255, 0, 0), Plataforma_Mortal[i])

    # Desenha o jogador (círculo) na posição corrigida
    pygame.draw.circle(tela, (255, 0, 255), (Player_X, Player_Y), 80)

    # Desenha a Porta com as coordenadas da fase atual
    Door = pygame.draw.rect(tela, (255, 255, 0), (Door_Pos_X, Door_Pos_Y, Door_X, Door_Y))

    # Transição de fases
    if jogador_rect.colliderect(Door):
        if Som_Door: Som_Door.play()
        Fase += 1
        if Fase > 6:
            Fase = 1
            
        Pontos += 100
        Gravidade_Y = 0
        carregar_fase(Fase)
    
    # Exibe placar de Pontos e Fases adaptativo
    if gravidade > 0:
        texto_formatado = nome_da_fonte.render(f"Fase: {Fase}  |  Pontos: {Pontos}", True, (255, 255, 255))
        tela.blit(texto_formatado, (50, 50))
    else:
        texto_formatado = nome_da_fonte.render(f"Fase: {Fase}  |  Pontos: {Pontos}", True, (255, 255, 255))
        tela.blit(texto_formatado, (50, 115))
        
    pygame.display.update()
