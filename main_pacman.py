import pygame
from mapa import Mapa, ancho_mapa, alto_mapa, tile_size
from pacman import pacman
from ver_mapa import dibujar_mapa, dibujar_texto, dibujar_vidas, margen_superior, margen_inferior

pygame.init()

mapa = Mapa("mapa.txt")

ancho_ventana = ancho_mapa * tile_size
alto_ventana  = alto_mapa  * tile_size + margen_superior + margen_inferior

pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Pac-Man")

fuente = pygame.font.SysFont("arial", 24, True)
reloj  = pygame.time.Clock()

jugador = pacman(mapa)

score = 0
ventana_abierta = True

while ventana_abierta:
    dt = reloj.tick(60) / 1000.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ventana_abierta = False
        jugador.manejar_evento(evento)

    score += jugador.actualizar(dt, mapa)

    pantalla.fill((0, 0, 0))
    dibujar_texto(pantalla, fuente)
    dibujar_mapa(pantalla, mapa)
    dibujar_vidas(pantalla)
    jugador.dibujar(pantalla, offset_y=margen_superior)

    pygame.display.flip()

pygame.quit()