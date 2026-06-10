from fantasmas.ghost import Ghost
import random

class Blinky(Ghost):

    def __init__(self, x, y, objetivo_scatter):
        super().__init__(
            id="blinky",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="red"
        )

    def obtener_objetivo_chase(self, pacman, mapa):
        return (pacman.tile_x, pacman.tile_y)
    

class Pinky(Ghost):

    def __init__(self, x, y, objetivo_scatter):
        super().__init__(
            id="pinky",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="pink"
        )

    def obtener_objetivo_chase(self, pacman, mapa):
        dx, dy = pacman.direccion
        objetivo_x = pacman.tile_x + dx * 4
        objetivo_y = pacman.tile_y + dy * 4

        # bug del original: mirando arriba también se desplaza 4 a la izquierda
        if (dx, dy) == (0, -1):
            objetivo_x -= 4

        return (objetivo_x, objetivo_y)
    

class Inky(Ghost):

    def __init__(self, x, y, objetivo_scatter, blinky, otros_fantasmas):
        super().__init__(
            id="inky",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="cyan"
        )
        self.blinky = blinky  # puede ser None si Blinky no fue elegido
        self.otros_fantasmas = otros_fantasmas  # lista con los otros fantasmas activos

    def obtener_objetivo_chase(self, pacman, mapa):
        # punto intermedio: 2 tiles adelante de Pac-Man
        dx, dy = pacman.direccion
        medio_x = pacman.tile_x + dx * 2
        medio_y = pacman.tile_y + dy * 2

        # referencia: Blinky o un fantasma al azar si Blinky no está
        if self.blinky is not None:
            referencia = self.blinky
        else:
            referencia = random.choice(self.otros_fantasmas)

        # vector desde la referencia hasta el punto intermedio, duplicado
        objetivo_x = medio_x + (medio_x - referencia.tile_x)
        objetivo_y = medio_y + (medio_y - referencia.tile_y)

        return (objetivo_x, objetivo_y)


class Clyde(Ghost):

    def __init__(self, x, y, objetivo_scatter):
        super().__init__(
            id="clyde",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="orange"
        )

    def obtener_objetivo_chase(self, pacman, mapa):
        # si está lejos de Pac-Man, lo persigue
        # si está cerca, se va a su esquina
        if self.distancia((self.tile_x, self.tile_y), (pacman.tile_x, pacman.tile_y)) > 8:
            return (pacman.tile_x, pacman.tile_y)
        else:
            return self.objetivo_scatter
        

class Facu(Ghost):

    def __init__(self, x, y, objetivo_scatter):
        super().__init__(
            id="facu",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="facu"
        )

    def obtener_objetivo_chase(self, pacman, mapa):
        # inverso a Clyde: dormido lejos, agresivo cerca
        if self.distancia((self.tile_x, self.tile_y), (pacman.tile_x, pacman.tile_y)) < 8:
            return (pacman.tile_x, pacman.tile_y)
        else:
            return self.objetivo_scatter
        

class Picky(Ghost):

    def __init__(self, x, y, objetivo_scatter):
        super().__init__(
            id="picky",
            x=x,
            y=y,
            objetivo_scatter=objetivo_scatter,
            color="picky"
        )

    def obtener_objetivo_chase(self, pacman, mapa):
        pellets = mapa.obtener_power_pellets()  # lista de tiles con power pellets
        if not pellets:
            return (pacman.tile_x, pacman.tile_y)  # fallback: persigue a Pac-Man
        return min(pellets, key=lambda p: self.distancia(p, (self.tile_x, self.tile_y)))