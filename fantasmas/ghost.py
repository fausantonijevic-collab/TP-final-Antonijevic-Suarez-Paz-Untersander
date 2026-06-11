import pygame
from setting import *

direcciones = {
    "derecha": (1, 0),
    "izquierda": (-1, 0),
    "arriba": (0, -1),
    "abajo": (0, 1)
}

opuesta = {
    "derecha": "izquierda",
    "izquierda": "derecha",
    "arriba": "abajo",
    "abajo": "arriba"
}

ESTADO_NORMAL = "normal"
ESTADO_ASUSTADO = "asustado"
ESTADO_OJOS = "ojos"
ESTADO_SALIENDO = "saliendo"

class Ghost:

    def __init__(self, mapa, color):


        col, fila = mapa.obtener_posicion_fantasma()

        self.x = col * tile_size + tile_size / 2
        self.y = fila * tile_size + tile_size / 2

        self.inicial_x = self.x
        self.inicial_y = self.y

        self.direccion = "izquierda"

        self.velocidad = vel_fantasma_normal

        self.estado = ESTADO_SALIENDO

        self.tiempo_asustado = 0

        self.sprite_asustado_azul = pygame.transform.scale(
            pygame.image.load(
                "imagenes/blue_asustado.png"
            ).convert_alpha(),
            (tile_size * 2, tile_size * 2)
        )

        self.sprite_asustado_blanco = pygame.transform.scale(
            pygame.image.load(
                "imagenes/white_asustado.png"
            ).convert_alpha(),
            (tile_size * 2, tile_size * 2)
        )

        self.sprite_ojos = pygame.transform.scale(
            pygame.image.load(
                "imagenes/ojos.png"
            ).convert_alpha(),
            (tile_size * 2, tile_size * 2)
        )

        self.sprites = {
            "derecha": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_derecha.png"
                ).convert_alpha(),
                (tile_size * 2, tile_size * 2)
            ),

            "izquierda": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_izquierda.png"
                ).convert_alpha(),
                (tile_size * 2, tile_size * 2)
            ),

            "arriba": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_arriba.png"
                ).convert_alpha(),
                (tile_size * 2, tile_size * 2)
            ),

            "abajo": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_abajo.png"
                ).convert_alpha(),
                (tile_size * 2, tile_size * 2)
            )
        }


    def col(self):
        return int(self.x) // tile_size

    def fila(self):
        return int(self.y) // tile_size

    def centrado(self, margen=4):

        cx = self.col() * tile_size + tile_size / 2
        cy = self.fila() * tile_size + tile_size / 2

        return (
            abs(self.x - cx) <= margen and
            abs(self.y - cy) <= margen
        )
    
    def direcciones_validas(self, mapa):

        validas = []

        for nombre, (dc, df) in direcciones.items():

            col = self.col() + dc
            fila = self.fila() + df

            if mapa.es_pared((col, fila)):
                continue

            tile = mapa.obtener_tile(col, fila)

            if self.estado != ESTADO_OJOS:

                if tile == "G":
                    continue

                if tile == "-":
                    continue

            validas.append(nombre)

        return validas

    def elegir_direccion(self, mapa, target_col, target_fila):

        opciones = self.direcciones_validas(mapa)

        if len(opciones) == 0:
            return

        if (
            opuesta[self.direccion] in opciones
            and len(opciones) > 1
        ):
            opciones.remove(opuesta[self.direccion])

        mejor = None
        mejor_dist = float("inf")

        for direccion in opciones:

            dc, df = direcciones[direccion]

            col = self.col() + dc
            fila = self.fila() + df

            dist = (
                (col - target_col) ** 2 +
                (fila - target_fila) ** 2
            )

            if dist < mejor_dist:

                mejor_dist = dist
                mejor = direccion

        self.direccion = mejor

    def alinear_al_tile(self):

        self.x = self.col() * tile_size + tile_size / 2
        self.y = self.fila() * tile_size + tile_size / 2

    def asustar(self):

        if self.estado != ESTADO_NORMAL:
            return

        self.estado = ESTADO_ASUSTADO

        self.tiempo_asustado = 0

        self.velocidad = vel_fantasma_asustado


    def morir(self):

        self.estado = ESTADO_OJOS
        self.velocidad = vel_fantasma_ojos
        self.tiempo_asustado = 0


    def actualizar_estado(self, dt):

        if self.estado != ESTADO_ASUSTADO:
            return

        self.tiempo_asustado += dt

        if self.tiempo_asustado >= duracion_asustado:
            self.estado = ESTADO_NORMAL
            self.velocidad = vel_fantasma_normal
            self.tiempo_asustado = 0
            

    def mover(self, dt):

        dc, df = direcciones[self.direccion]

        self.x += dc * self.velocidad * dt
        self.y += df * self.velocidad * dt


    def actualizar(self, dt, mapa, pacman):

        self.comio_power_pellet = False
        self.actualizar_estado(dt)

        # Fantasma saliendo de la ghost house
        if self.estado == ESTADO_SALIENDO:

            puerta_fila = 12

            if self.fila() <= puerta_fila:
                print("SALE DE CASA:", self.estado)

                self.estado = ESTADO_NORMAL
                return

            else:

                self.direccion = "arriba"
                self.mover(dt)

            return

        # Ojos que vuelven a la casa
        if self.estado == ESTADO_OJOS:

            if self.col() == 13 and self.fila() == 14:

                print("LLEGO A CASA:", self.estado)

                self.estado = ESTADO_SALIENDO

                self.velocidad = vel_fantasma_normal

                self.tiempo_asustado = 0

                self.direccion = "arriba"

                return

        if self.centrado():

            if self.estado == ESTADO_OJOS:

                target_col = 13
                target_fila = 14

            else:

                target_col, target_fila = self.get_target(pacman)

            direccion_anterior = self.direccion

            self.elegir_direccion(
                mapa,
                target_col,
                target_fila
            )

            if self.direccion != direccion_anterior:
                self.alinear_al_tile()

        self.mover(dt)


    def resetear(self):

        self.x = self.inicial_x
        self.y = self.inicial_y

        self.estado = ESTADO_SALIENDO

        self.velocidad = vel_fantasma_normal

        self.direccion = "izquierda"

        self.tiempo_asustado = 0

    def dibujar(self, pantalla, offset_y=0):


        sprite = self.sprites[self.direccion]

        if self.estado == ESTADO_ASUSTADO:

            tiempo_restante = (
                duracion_asustado -
                self.tiempo_asustado
            )

            if tiempo_restante <= duracion_parpadeo:

                if int(self.tiempo_asustado * 8) % 2 == 0:
                    sprite = self.sprite_asustado_azul
                else:
                    sprite = self.sprite_asustado_blanco

            else:

                sprite = self.sprite_asustado_azul

        elif self.estado == ESTADO_OJOS:

            sprite = self.sprite_ojos

        offset_x = 0
        offset_y_sprite = 0

        if self.direccion == "arriba":
            offset_x = 1

        elif self.direccion == "abajo":
            offset_x = -1

        elif self.direccion == "izquierda":
            offset_y_sprite = 2

        pantalla.blit(
            sprite,
            (
                self.x - sprite.get_width() / 2 + offset_x,
                self.y - sprite.get_height() / 2 + offset_y + offset_y_sprite
            )
        )

        print("DIBUJAR:", self.estado)
j