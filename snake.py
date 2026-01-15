import pygame
import sys
import random
import json
import os

pygame.init()
pygame.mixer.init()

# --------------------
# Configuración general
# --------------------
ANCHO = 600
ALTO = 400
TAM_BLOQUE = 20

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake")

# Colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)

# Reloj
reloj = pygame.time.Clock()

# --------------------
# Fuentes
# --------------------
try:
    fuente_pequena = pygame.font.Font("fuentes/arcade.ttf", 16)
    fuente = pygame.font.Font("fuentes/arcade.ttf", 22)
    fuente_grande = pygame.font.Font("fuentes/arcade.ttf", 36)
except:
    fuente_pequena = pygame.font.SysFont(None, 20)
    fuente = pygame.font.SysFont(None, 28)
    fuente_grande = pygame.font.SysFont(None, 36)

# --------------------
# Sonidos
# --------------------
sonido_comer = pygame.mixer.Sound("sonidos/comer.wav")
sonido_gameover = pygame.mixer.Sound("sonidos/gameover.wav")
sonido_pausa = pygame.mixer.Sound("sonidos/pausa.wav")

pygame.mixer.music.load("sonidos/menu_music.wav")

# --------------------
# Configuración (opciones)
# --------------------
CONFIG_FILE = "config.json"

config = {
    "musica": True,
    "sonido": True,
    "grilla": True
}

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))


def guardar_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


if config["musica"]:
    pygame.mixer.music.play(-1)

# --------------------
# Funciones auxiliares
# --------------------
def leer_record():
    try:
        with open("record.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def guardar_record(nuevo):
    with open("record.txt", "w") as f:
        f.write(str(nuevo))


def mostrar_puntaje(puntaje, record, nivel):
    texto = fuente_pequena.render(
        f"Puntaje: {puntaje}  Récord: {record}  Nivel: {nivel}",
        True, BLANCO
    )

    fondo = texto.get_rect(topleft=(10, 10))
    fondo.inflate_ip(10, 6)  # margen interno

    pygame.draw.rect(ventana, NEGRO, fondo)
    ventana.blit(texto, (10, 10))


def dibujar_grilla():
    if not config["grilla"]:
        return
    for x in range(0, ANCHO, TAM_BLOQUE):
        pygame.draw.line(ventana, GRIS, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TAM_BLOQUE):
        pygame.draw.line(ventana, GRIS, (0, y), (ANCHO, y))

def fade(ventana, color=(0, 0, 0), velocidad=10):
    fade_surface = pygame.Surface((ANCHO, ALTO))
    fade_surface.fill(color)

    for alpha in range(0, 255, velocidad):
        fade_surface.set_alpha(alpha)
        ventana.blit(fade_surface, (0, 0))
        pygame.display.update()
        reloj.tick(60)

# --------------------
# Game Over
# --------------------
def game_over(puntaje):
    fade(ventana)
    ventana.fill(NEGRO)

    texto = fuente_grande.render("GAME OVER", True, ROJO)
    rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
    ventana.blit(texto, rect)

    texto2 = fuente_pequena.render("R: reiniciar  |  Q: salir", True, BLANCO)
    rect2 = texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 10))
    ventana.blit(texto2, rect2)

    texto3 = fuente_pequena.render(f"Puntaje final: {puntaje}", True, BLANCO)
    rect3 = texto3.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
    ventana.blit(texto3, rect3)

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "reiniciar"
                if evento.key == pygame.K_q:
                    return "salir"


# --------------------
# Menú de opciones
# --------------------
def menu_opciones():
    seleccion = 0
    opciones = ["MÚSICA", "SONIDO", "GRILLA", "VOLVER"]

    while True:
        ventana.fill(NEGRO)

        titulo = fuente_grande.render("OPCIONES", True, VERDE)
        ventana.blit(titulo, (ANCHO // 2 - 120, 60))

        for i, opcion in enumerate(opciones):
            y = 150 + i * 40
            color = BLANCO if i == seleccion else (120, 120, 120)

            estado = ""
            if opcion == "MÚSICA":
                estado = "ON" if config["musica"] else "OFF"
            elif opcion == "SONIDO":
                estado = "ON" if config["sonido"] else "OFF"
            elif opcion == "GRILLA":
                estado = "ON" if config["grilla"] else "OFF"

            texto = fuente.render(f"{opcion} {estado}", True, color)
            ventana.blit(texto, (ANCHO // 2 - 140, y))

            if i == seleccion:
                flecha = fuente.render(">", True, VERDE)
                ventana.blit(flecha, (ANCHO // 2 - 180, y))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "MÚSICA":
                        config["musica"] = not config["musica"]
                        if config["musica"]:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif opciones[seleccion] == "SONIDO":
                        config["sonido"] = not config["sonido"]
                    elif opciones[seleccion] == "GRILLA":
                        config["grilla"] = not config["grilla"]
                    elif opciones[seleccion] == "VOLVER":
                        guardar_config()
                        return


# --------------------
# Menú principal
# --------------------
def menu():
    seleccion = 0
    opciones = ["JUGAR", "OPCIONES", "AYUDA", "SALIR"]

    while True:
        ventana.fill(NEGRO)

        titulo = fuente_grande.render("SNAKE", True, VERDE)
        ventana.blit(titulo, (ANCHO // 2 - 80, 80))

        for i, opcion in enumerate(opciones):
            y = 180 + i * 40
            color = BLANCO if i == seleccion else (120, 120, 120)

            texto = fuente.render(opcion, True, color)
            ventana.blit(texto, (ANCHO // 2 - 20, y))

            if i == seleccion:
                flecha = fuente.render(">", True, VERDE)
                ventana.blit(flecha, (ANCHO // 2 - 60, y))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "JUGAR":
                        return
                    elif opciones[seleccion] == "OPCIONES":
                        menu_opciones()
                    elif opciones[seleccion] == "AYUDA":
                        pantalla_ayuda()
                    else:
                        pygame.quit()
                        sys.exit()

# --------------------
# Pantalla de Ayuda
# --------------------
def pantalla_ayuda():
    while True:
        ventana.fill(NEGRO)

        titulo = fuente_grande.render("AYUDA", True, VERDE)
        ventana.blit(titulo, (ANCHO // 2 - 80, 50))

        instrucciones = [
            "CONTROLES",
            "",
            "↑ ↓ ← →   Mover la serpiente",
            "P         Pausar / Reanudar",
            "",
            "OBJETIVO",
            "",
            "Come la comida",
            "No choques con las paredes",
            "Ni con tu propio cuerpo",
            "",
            "ESC o ENTER para volver"
        ]

        y = 120
        for linea in instrucciones:
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(
                texto,
                (ANCHO // 2 - texto.get_width() // 2, y)
            )
            y += 22

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return

        reloj.tick(30)
# --------------------
# Juego principal
# --------------------
def juego():
    fade(ventana)
    x = ANCHO // 2
    y = ALTO // 2
    vel_x = TAM_BLOQUE
    vel_y = 0

    direccion = "RIGHT"
    direccion_pendiente = direccion

    serpiente = []
    largo = 3
    puntaje = 0

    nivel = 1
    record = leer_record()
    velocidad = 10
    pausado = False

    # Animación de nivel
    mostrar_nivel = False
    nivel_alpha = 0
    nivel_estado = "in"   # in → hold → out
    nivel_timer = 0


    comida_x = random.randrange(0, ANCHO, TAM_BLOQUE)
    comida_y = random.randrange(0, ALTO, TAM_BLOQUE)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direccion != "DOWN":
                    direccion_pendiente = "UP"
                elif evento.key == pygame.K_DOWN and direccion != "UP":
                    direccion_pendiente = "DOWN"
                elif evento.key == pygame.K_LEFT and direccion != "RIGHT":
                    direccion_pendiente = "LEFT"
                elif evento.key == pygame.K_RIGHT and direccion != "LEFT":
                    direccion_pendiente = "RIGHT"
                elif evento.key == pygame.K_p:
                    pausado = not pausado
                    if config["sonido"]:
                        sonido_pausa.play()


        direccion = direccion_pendiente
        

        if direccion == "UP":
            vel_x, vel_y = 0, -TAM_BLOQUE
        elif direccion == "DOWN":
            vel_x, vel_y = 0, TAM_BLOQUE
        elif direccion == "LEFT":
            vel_x, vel_y = -TAM_BLOQUE, 0
        elif direccion == "RIGHT":
            vel_x, vel_y = TAM_BLOQUE, 0

        # --- PAUSA ---
        if pausado:
            ventana.fill(NEGRO)
            dibujar_grilla()

            for i, bloque in enumerate(serpiente):
                if i == len(serpiente) - 1:  # cabeza
                    pygame.draw.rect(
                        ventana, (0, 200, 0),
                        (bloque[0], bloque[1], TAM_BLOQUE, TAM_BLOQUE),
                        border_radius=6
                    )
                else:
                    pygame.draw.rect(
                        ventana, VERDE,
                        (bloque[0], bloque[1], TAM_BLOQUE, TAM_BLOQUE),
                        border_radius=4
                    )

            pygame.draw.circle(
                ventana,
                ROJO,
                (comida_x + TAM_BLOQUE // 2, comida_y + TAM_BLOQUE // 2),
                TAM_BLOQUE // 2
            )

            mostrar_puntaje(puntaje, record, nivel)

            texto_pausa = fuente_grande.render("PAUSA", True, BLANCO)
            ventana.blit(
                texto_pausa,
                (
                    ANCHO // 2 - texto_pausa.get_width() // 2,
                    ALTO // 2 - texto_pausa.get_height() // 2
                )
            )

            pygame.display.update()
            reloj.tick(10)
            continue
        # --- FIN PAUSA ---

        x += vel_x
        y += vel_y

        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO:
            if config["sonido"]:
                sonido_gameover.play()
            if puntaje > record:
                guardar_record(puntaje)
            return game_over(puntaje)

        cabeza = [x, y]
        serpiente.append(cabeza)

        if len(serpiente) > largo:
            serpiente.pop(0)

        if cabeza in serpiente[:-1]:
            if config["sonido"]:
                sonido_gameover.play()
            if puntaje > record:
                guardar_record(puntaje)
            return game_over(puntaje)

        if x == comida_x and y == comida_y:
            pygame.draw.rect(
                ventana,
                BLANCO,
                (x, y, TAM_BLOQUE, TAM_BLOQUE),
                2
            )

            if config["sonido"]:
                sonido_comer.play()
            comida_x = random.randrange(0, ANCHO, TAM_BLOQUE)
            comida_y = random.randrange(0, ALTO, TAM_BLOQUE)
            largo += 1
            puntaje += 1
            nuevo_nivel = puntaje // 5 + 1

            if nuevo_nivel > nivel:
                nivel = nuevo_nivel
                mostrar_nivel = True
                nivel_alpha = 0
                nivel_estado = "in"
                nivel_timer = 30
            else:
                nivel = nuevo_nivel


            velocidad = min(10 + nivel, 25)

        ventana.fill(NEGRO)
        dibujar_grilla()

        for i, bloque in enumerate(serpiente):
            if i == len(serpiente) - 1:  # cabeza
                pygame.draw.rect(
                    ventana, (0, 200, 0),
                    (bloque[0], bloque[1], TAM_BLOQUE, TAM_BLOQUE),
                    border_radius=6
                )
            else:
                pygame.draw.rect(
                    ventana, VERDE,
                    (bloque[0], bloque[1], TAM_BLOQUE, TAM_BLOQUE),
                    border_radius=4
                )

        pygame.draw.circle(
            ventana,
            ROJO,
            (comida_x + TAM_BLOQUE // 2, comida_y + TAM_BLOQUE // 2),
            TAM_BLOQUE // 2
        )

        mostrar_puntaje(puntaje, record, nivel)
        # ---- ANIMACIÓN NIVEL ----
        if mostrar_nivel:
            texto_nivel = fuente_grande.render(f"NIVEL {nivel}", True, BLANCO)
            texto_nivel.set_alpha(nivel_alpha)

            rect = texto_nivel.get_rect(
                center=(ANCHO // 2, ALTO // 2)
            )
            ventana.blit(texto_nivel, rect)

            if nivel_estado == "in":
                nivel_alpha += 10
                if nivel_alpha >= 255:
                    nivel_alpha = 255
                    nivel_estado = "hold"

            elif nivel_estado == "hold":
                nivel_timer -= 1
                if nivel_timer <= 0:
                    nivel_estado = "out"

            elif nivel_estado == "out":
                nivel_alpha -= 10
                if nivel_alpha <= 0:
                    mostrar_nivel = False
        # ---- FIN ANIMACIÓN ----


        pygame.display.update()
        reloj.tick(velocidad)


# --------------------
# Bucle principal
# --------------------
menu()

while True:
    resultado = juego()
    if resultado == "reiniciar":
        continue
    fade(ventana)
    menu()

pygame.quit()
