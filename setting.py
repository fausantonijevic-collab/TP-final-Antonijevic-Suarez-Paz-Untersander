#tamaño de tiles y mapa
tile_size= 24
map_col = 28
map_filas= 31

#ventana y FPS
ancho = tile_size * map_col
alto = tile_size* map_filas + 60

fps = 60

#velocidades
vel_max = 7.5 *tile_size
vel_pacman_normal = vel_max * 0.80
vel_pacman_power = vel_max * 0.90

#power pellet
duracion_asustado = 6.0
duracion_parpadeo= 2.0

#puntos y vidas
vidas_iniciales= 3
punto_dot=10
puntos_power_pellet= 50

#Colores
color_fondo= (0,0,0)
color_pared =(28,42,237)
color_dot = (255,255,255)
color_pacman=  (255,255,0)
color_infojuego = (255,255,255)