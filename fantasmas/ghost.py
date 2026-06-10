import pygame
import math
import random
from setting import *

class Ghost:

    def __init__(self, id, x, y, objetivo_scatter, color):
        self.id = id

        # posición en tiles
        self.tile_x = x
        self.tile_y = y

        # posición en píxeles
        self.pixel_x = x * tile_size
        self.pixel_y = y * tile_size

        # movimiento
        self.direccion = (1, 0)
        self.velocidad = vel_fantasma_normal

        # modo
        self.modo = "house"
        self.objetivo_scatter = objetivo_scatter

        # parpadeo modo asustado
        self.parpadeando = False
        self.timer_parpadeo = 0
        self.mostrar_blanco = False

        # imagen según dirección
        self.imagen_derecha = pygame.image.load(f"imagenes/{color}_ghost_derecha.png")
        self.imagen_derecha = pygame.transform.scale(self.imagen_derecha, (int(tile_size * 1.5), int(tile_size * 1.5)))

        self.imagen_izquierda = pygame.image.load(f"imagenes/{color}_ghost_izquierda.png")
        self.imagen_izquierda = pygame.transform.scale(self.imagen_izquierda, (int(tile_size * 1.5), int(tile_size * 1.5)))

        self.imagen_arriba = pygame.image.load(f"imagenes/{color}_ghost_arriba.png")
        self.imagen_arriba = pygame.transform.scale(self.imagen_arriba, (int(tile_size * 1.5), int(tile_size * 1.5)))

        self.imagen_abajo = pygame.image.load(f"imagenes/{color}_ghost_abajo.png")
        self.imagen_abajo = pygame.transform.scale(self.imagen_abajo, (int(tile_size * 1.5), int(tile_size * 1.5)))

        # imágenes modo asustado y ojos
        self.imagen_asustado_azul = pygame.image.load("imagenes/blue_asustado.png")
        self.imagen_asustado_azul = pygame.transform.scale(self.imagen_asustado_azul, (int(tile_size * 1.5), int(tile_size * 1.5)))

        self.imagen_asustado_blanco = pygame.image.load("imagenes/white_asustado.png")
        self.imagen_asustado_blanco = pygame.transform.scale(self.imagen_asustado_blanco, (int(tile_size * 1.5), int(tile_size * 1.5)))

        self.imagen_ojos = pygame.image.load("imagenes/ojos.png")
        self.imagen_ojos = pygame.transform.scale(self.imagen_ojos, (int(tile_size * 1.5), int(tile_size * 1.5)))

    # ---- cada subclase define su propio objetivo de chase ----
    def obtener_objetivo_chase(self, pacman, mapa):
        raise NotImplementedError("Cada fantasma define su propio objetivo de chase")

    # ---- objetivo según modo actual ----
    def obtener_objetivo(self, pacman, mapa):
        if self.modo == "chase":
            return self.obtener_objetivo_chase(pacman, mapa)
        elif self.modo == "scatter":
            return self.objetivo_scatter
        elif self.modo == "frightened":
            return None
        elif self.modo == "eaten":
            return (13, 14)  # ghost house

    # ---- distancia euclidiana entre dos tiles ----
    def distancia(self, tile_a, tile_b):
        return math.sqrt((tile_a[0] - tile_b[0])**2 +
                         (tile_a[1] - tile_b[1])**2)

    # ---- elegir dirección en intersección ----
    def elegir_direccion(self, pacman, mapa):
        objetivo = self.obtener_objetivo(pacman, mapa)

        direcciones = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # arriba, izq, abajo, der
        opuesto = (-self.direccion[0], -self.direccion[1])

        if self.modo == "frightened":
            opciones = [d for d in direcciones
                        if d != opuesto and
                        not mapa.es_pared((self.tile_x + d[0], self.tile_y + d[1]))]
            if opciones:
                self.direccion = random.choice(opciones)
            return

        mejor_dir = None
        menor_dist = float('inf')

        print(
        f"{self.id} | tile=({self.tile_x},{self.tile_y}) "
        f"pixel=({self.pixel_x:.2f},{self.pixel_y:.2f})")

        for d in direcciones:
            if d == opuesto:
                continue
            tile_siguiente = (self.tile_x + d[0], self.tile_y + d[1])
            if mapa.es_pared(tile_siguiente):
                continue
            dist = self.distancia(tile_siguiente, objetivo)
            if dist < menor_dist:
                menor_dist = dist
                mejor_dir = d

        if mejor_dir:
            self.direccion = mejor_dir

    # ---- detectar si está en el centro de un tile ----
    def en_centro_tile(self):
        resto_x = self.pixel_x % tile_size
        resto_y = self.pixel_y % tile_size

        tolerancia = 2

        centrado_x = (
            resto_x < tolerancia
            or resto_x > tile_size - tolerancia
        )

        centrado_y = (
            resto_y < tolerancia
            or resto_y > tile_size - tolerancia
        )

        return centrado_x and centrado_y

    # ---- actualizar velocidad según modo y posición ----
    def actualizar_velocidad(self, mapa):
        if self.modo == "eaten":
            self.velocidad = vel_fantasma_ojos
        elif self.modo == "frightened":
            self.velocidad = vel_fantasma_asustado
        elif mapa.es_tunel(self.tile_x, self.tile_y):
            self.velocidad = vel_fantasma_tunel
        else:
            self.velocidad = vel_fantasma_normal

    # ---- cambiar modo ----
    def cambiar_modo(self, nuevo_modo):
        if nuevo_modo != self.modo:
            self.direccion = (-self.direccion[0], -self.direccion[1])
            self.modo = nuevo_modo

    # ---- actualizar posición ----
    def actualizar(self, dt, pacman, mapa):

        if self.modo == "house":
            return

        # actualizar tile SIEMPRE
        self.tile_x = round(self.pixel_x / tile_size)
        self.tile_y = round(self.pixel_y / tile_size)

        self.actualizar_velocidad(mapa)

        if self.en_centro_tile():

            self.tile_x = round(self.pixel_x / tile_size)
            self.tile_y = round(self.pixel_y / tile_size)

            self.elegir_direccion(pacman, mapa)

        self.pixel_x += self.direccion[0] * self.velocidad * dt
        self.pixel_y += self.direccion[1] * self.velocidad * dt

        self.tile_x = round(self.pixel_x / tile_size)
        self.tile_y = round(self.pixel_y / tile_size)

        self.tile_x, self.tile_y, self.pixel_x, self.pixel_y = mapa.teletransportar(
            self.tile_x,
            self.tile_y,
            self.pixel_x,
            self.pixel_y
        )

        if self.parpadeando:
            self.timer_parpadeo += dt

            if self.timer_parpadeo >= 0.2:
                self.timer_parpadeo = 0
                self.mostrar_blanco = not self.mostrar_blanco

    def obtener_imagen_direccion(self):
        if self.direccion == (1, 0):
            return self.imagen_derecha
        elif self.direccion == (-1, 0):
            return self.imagen_izquierda
        elif self.direccion == (0, -1):
            return self.imagen_arriba
        elif self.direccion == (0, 1):
            return self.imagen_abajo
        else:
            return self.imagen_derecha
    
    def dibujar(self, pantalla, margen_superior):
        ancho_img = self.imagen_derecha.get_width()
        alto_img = self.imagen_derecha.get_height()
        desplazamiento_x = (tile_size - ancho_img) // 2
        desplazamiento_y = (tile_size - alto_img) // 2

        pos_x = self.pixel_x + desplazamiento_x
        pos_y = self.pixel_y + desplazamiento_y + margen_superior

        if self.modo == "frightened":
            if self.parpadeando and self.mostrar_blanco:
                pantalla.blit(self.imagen_asustado_blanco, (pos_x, pos_y))
            else:
                pantalla.blit(self.imagen_asustado_azul, (pos_x, pos_y))
        elif self.modo == "eaten":
            pantalla.blit(self.imagen_ojos, (pos_x, pos_y))
        else:
            pantalla.blit(self.obtener_imagen_direccion(), (pos_x, pos_y))