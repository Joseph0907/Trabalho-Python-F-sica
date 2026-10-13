import pygame # Permite utilizar os comandos da biblioteca pygame

from pygame.locals import * # Importa as funções do pygame local

from sys import exit # Importa a função exit

pygame.init() # Função que inicia o jogo

Musica_de_fundo = pygame.mixer.music.load("What Went Wrong.mp3") # cria a função com a música
pygame.mixer.music.play(-1) # Toca a música (o -1 é para a musica tocar toda vez que acabar)

largura = 1920 # Varíavel com a largura(x) da tela
altura = 1080 # Varíavel com a altura(y) da tela
gravidade = 1
Gravidade_X = 0
Gravidade_Y = 0
colisão = 0
trajetória = 0
aceleração = 0
f = 0

#Propiedades do player

Player_X= 80 # largura do jogador
Player_Y= 800 # altura do jogador
Velocidade_Player_X = 20 # Quantos pixels o jogador se movimentara horizontalmente
Velocidade_Player_Y = 0 # Quantos pixels o jogador se movimentara verticalmente


tela = pygame.display.set_mode((largura,altura)) # Função que define o tamanho da tela
pygame.display.set_caption("Trabaio de Python") # Nome do programa
relogio = pygame.time.Clock() # criação de FPS

while True: # Loop principal que faz o jogo rodar
    relogio.tick(60) # limita o FPS do jogo
    tela.fill((0,0,0)) # Recolore a tela com a cor dentro do ()
    for event in pygame.event.get():  # Verifica se algum evento ocorreu ou ocorrerá
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: 
            Player_X = Player_X + Velocidade_Player_X
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            Player_X = Player_X - Velocidade_Player_X
        #if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            #Player_Y = Player_Y + 100
        if teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_SPACE]:
            if Player_Y >= 800:
                Gravidade_Y = -20

    Gravidade_Y += gravidade
    Player_Y += Gravidade_Y

    if Player_Y >= 800:
        Player_Y = 800
        Gravidade_Y = 0

    pygame.draw.rect(tela, (0,255,0), (1620,680,100,200)) # Desenha um retângulo(rect) na tela (aonde sera desenhado, (cor), (posição,largura,altura))
    ret_object = pygame.draw.rect(tela, (255,0,0), (520,f,100,200))
    if f >= altura-400: # impede que o retangulo va para baixo da tela
        f = 0
    f = f + 3
    ret_player = pygame.draw.circle(tela, (255,0,255), (Player_X,Player_Y), (80))
    pygame.draw.line(tela, (255,255,255), (0,980), (1920,980), 200) # desenha uma linha(line) na tela (aonde sera desenhado, (cor), (posição inicial), (posição final), expessura)
    #A posição do retangulo é referenciada ao canto superior esquerdo do objeto e não o meio diferente do circulo

    if ret_player.colliderect(ret_object):
        print("colidiu")
    pygame.display.update() # A cada atualização do while principal essa função ira atualizar o jogo







    # pygame.draw.circle(tela, (0,255,0), (1670,680), (100)) Desenha um circulo(cicle) na tela (aonde sera desenhado, (cor), (posição), (raio))