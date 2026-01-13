import pygame
import sys
import random

pygame.init()

# Ventana
ANCHO = 600
ALTO = 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

# Reloj
reloj = pygame.time.Clock()

# Tamaño del bloque
TAM_BLOQUE = 20

# Fuente
fuente = pygame.font.SysFont(None, 30)
fuente_grande = pygame.font.SysFont(None, 50)

def mostrar_puntaje(puntaje):
    texto = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    ventana.blit(texto, (10, 10))

def game_over(puntaje):
    texto = fuente_grande.render("GAME OVER", True, ROJO)
    ventana.blit(texto, (ANCHO // 2 - 140, ALTO // 2 - 40))
    texto2 = fuente.render("C: continuar  |  Q: salir", True, BLANCO)
    ventana.blit(texto2, (ANCHO // 2 - 150, ALTO // 2 + 10))
    texto3 = fuente.render(f"Puntaje final: {puntaje}", True, BLANCO)
    ventana.blit(texto3, (ANCHO // 2 - 120, ALTO // 2 + 40))
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_c:
                    return

def juego():
    x = ANCHO // 2
    y = ALTO // 2
    vel_x = TAM_BLOQUE
    vel_y = 0

    serpiente = []
    largo = 3
    puntaje = 0

    comida_x = random.randrange(0, ANCHO, TAM_BLOQUE)
    comida_y = random.randrange(0, ALTO, TAM_BLOQUE)

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and vel_y == 0:
                    vel_x = 0
                    vel_y = -TAM_BLOQUE
                elif evento.key == pygame.K_DOWN and vel_y == 0:
                    vel_x = 0
                    vel_y = TAM_BLOQUE
                elif evento.key == pygame.K_LEFT and vel_x == 0:
                    vel_x = -TAM_BLOQUE
                    vel_y = 0
                elif evento.key == pygame.K_RIGHT and vel_x == 0:
                    vel_x = TAM_BLOQUE
                    vel_y = 0

        x += vel_x
        y += vel_y

        # Colisión con paredes
        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO:
            game_over(puntaje)
            return

        cabeza = [x, y]
        serpiente.append(cabeza)
        if len(serpiente) > largo:
            del serpiente[0]

        # Colisión consigo misma
        if cabeza in serpiente[:-1]:
            game_over(puntaje)
            return

        # Comer comida
        if x == comida_x and y == comida_y:
            comida_x = random.randrange(0, ANCHO, TAM_BLOQUE)
            comida_y = random.randrange(0, ALTO, TAM_BLOQUE)
            largo += 1
            puntaje += 1

        ventana.fill(NEGRO)

        for bloque in serpiente:
            pygame.draw.rect(ventana, VERDE, (bloque[0], bloque[1], TAM_BLOQUE, TAM_BLOQUE))

        pygame.draw.rect(ventana, ROJO, (comida_x, comida_y, TAM_BLOQUE, TAM_BLOQUE))

        mostrar_puntaje(puntaje)
        pygame.display.update()
        reloj.tick(10)

# Bucle principal
while True:
    juego()