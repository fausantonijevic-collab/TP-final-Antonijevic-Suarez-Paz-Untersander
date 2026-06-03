import pygame
import math
from setting import (tile_size, vel_pacman_normal, vel_pacman_power,color_pacman,duracion_asustado)

direcciones= {"derecha":(1,0) , "izquierda":(-1,0), "arriba":(0,-1),"abajo":(0,1)}

angulo_base={"derecha":0 , "izquierda":180, "arriba":90,"abajo":270}

tiles_transitables = {"",".","o","P","T","-"}