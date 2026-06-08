import pygame
from mapa import Mapa, ancho_mapa, alto_mapa, tile_size


color_fondo = (0, 0, 0)
color_pared = (0, 0, 255)
color_punto = (255, 255, 255)
color_power_pellet = (255, 255, 255)
color_pacman = (255, 255, 0)
color_ghost_house = (80, 80, 80)
color_puerta = (255, 150, 255)
color_tunel = (30, 30, 30)
color_texto = (255, 255, 255)

margen_superior = 70
margen_inferior = 60

score = 0
high_score = 0
vidas = 3


def dibujar_texto(pantalla, fuente):
    texto_1up = fuente.render("1UP", True, color_texto)
    texto_high = fuente.render("HIGH SCORE", True, color_texto)
    texto_score = fuente.render(str(score), True, color_texto)
    texto_high_score = fuente.render(str(high_score), True, color_texto)

    pantalla.blit(texto_1up, (70, 10))
    pantalla.blit(texto_score, (85, 35))

    pantalla.blit(texto_high, (220, 10))
    pantalla.blit(texto_high_score, (285, 35))


def dibujar_vidas(pantalla):
    y = margen_superior + alto_mapa * tile_size + 30

    for i in range(vidas):
        x = 30 + i * 35

        pygame.draw.circle(pantalla, color_pacman, (x, y), 12)

        pygame.draw.polygon(pantalla, color_fondo, [(x, y),(x + 14, y - 7),(x + 14, y + 7)])


def dibujar_mapa(pantalla, mapa):
    for fila in range(alto_mapa):
        for columna in range(ancho_mapa):
            caracter = mapa.grilla[fila][columna]

            x = columna * tile_size
            y = fila * tile_size + margen_superior

            if caracter == "X":
                pygame.draw.rect(pantalla, color_pared, (x, y, tile_size, tile_size))

            elif caracter == ".":
                pygame.draw.circle(pantalla, color_punto,(x + tile_size // 2, y + tile_size // 2),3)

            elif caracter == "o":
                pygame.draw.circle(pantalla, color_power_pellet, (x + tile_size // 2, y + tile_size // 2),7)

                pygame.draw.polygon(pantalla,color_fondo,
                        [(x + tile_size // 2, y + tile_size // 2),
                        (x + tile_size, y + 4),
                        (x + tile_size, y + tile_size - 4)])

            elif caracter == "G":
                pygame.draw.rect(pantalla,color_ghost_house,(x, y, tile_size, tile_size) )

            elif caracter == "-":
                pygame.draw.rect(pantalla,color_puerta,(x, y + tile_size // 2 - 2, tile_size, 4))

            elif caracter == "T":
                pygame.draw.rect(pantalla,color_tunel,(x, y, tile_size, tile_size))


pygame.init()

mapa = Mapa("mapa.txt")

ancho_ventana = ancho_mapa * tile_size
alto_ventana = alto_mapa * tile_size + margen_superior + margen_inferior

pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Mapa Pac-Man")

fuente = pygame.font.SysFont("arial", 24, True)
reloj = pygame.time.Clock()

ventana_abierta = True

while ventana_abierta:
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            ventana_abierta = False

    pantalla.fill(color_fondo)

    dibujar_texto(pantalla, fuente)
    dibujar_mapa(pantalla, mapa)
    dibujar_vidas(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()