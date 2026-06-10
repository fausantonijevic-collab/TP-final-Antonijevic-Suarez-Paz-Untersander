import pygame
from mapa import Mapa, ancho_mapa, alto_mapa, tile_size
from pacman import pacman
from ver_mapa import dibujar_mapa, dibujar_texto, dibujar_vidas, margen_superior, margen_inferior
from fantasmas.ghost import *
from fantasmas.blinky import Blinky

pygame.init()

mapa = Mapa("mapa.txt")

ancho_ventana = ancho_mapa * tile_size
alto_ventana  = alto_mapa  * tile_size + margen_superior + margen_inferior

pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Pac-Man")

fuente = pygame.font.SysFont("arial", 24, True)
reloj  = pygame.time.Clock()

jugador = pacman(mapa)
blinky = Blinky(mapa)

score = 0
ventana_abierta = True
pausa_reinicio = 0

while ventana_abierta:
    dt = reloj.tick(60) / 1000.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ventana_abierta = False
        jugador.manejar_evento(evento)

    if pausa_reinicio > 0:
        pausa_reinicio -= dt

    else:

        score += jugador.actualizar(dt, mapa)

        if jugador.comio_power_pellet:
            blinky.asustar()

        blinky.actualizar(dt, mapa, jugador)

        if jugador.colisiona_con(blinky):
            if blinky.estado == ESTADO_ASUSTADO:
                blinky.morir()

            elif blinky.estado == ESTADO_NORMAL:

                jugador.resetear()
                blinky.resetear()
                pausa_reinicio = 2.0

    pantalla.fill((0, 0, 0))
    dibujar_texto(pantalla, fuente)
    dibujar_mapa(pantalla, mapa)
    dibujar_vidas(pantalla)
    jugador.dibujar(pantalla, offset_y=margen_superior)
    blinky.dibujar(pantalla, margen_superior)

    pygame.display.flip()

pygame.quit()