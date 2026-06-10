from fantasmas.ghost import Ghost


class Blinky(Ghost):

    def __init__(self, mapa):

        super().__init__(mapa, "red")

    def get_target(self, pacman):

        return (
            pacman.col(),
            pacman.fila()
        )