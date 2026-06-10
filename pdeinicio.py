import pygame
import sys

pygame.init()
 

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PAC-MAN")
 

NEGRO        = (0, 0, 0)
AMARILLO     = (255, 255, 0)
BLANCO       = (255, 255, 255)
GRIS         = (150, 150, 150)
GRIS_OSCURO  = (60, 60, 60)
AZUL_OSCURO  = (0, 0, 180)
 

fuente_grande  = pygame.font.SysFont("monospace", 72, bold=True)
fuente_mediana = pygame.font.SysFont("monospace", 32, bold=True)
fuente_chica   = pygame.font.SysFont("monospace", 22)
fuente_mini    = pygame.font.SysFont("monospace", 18)
 

fantasmas_disponibles = [
    {"nombre": "Blinky", "color": (230, 30,  30),  "desc": "El perseguidor. Siempre te sigue."},
    {"nombre": "Pinky",  "color": (255, 180, 220), "desc": "La emboscadora. Te corta el paso."},
    {"nombre": "Inky",   "color": (0,   220, 230), "desc": "El flanqueador. Impredecible."},
    {"nombre": "Clyde",  "color": (230, 140, 0),   "desc": "El timido. Huye si te acercas."},
    {"nombre": "Facu",   "color": (50,  200, 120), "desc": "El nuevo. Verde y traicionero."},
    {"nombre": "Picky",  "color": (180, 120, 230), "desc": "La lila. Muy veloz y caprichosa."},
]
 

nombres_esquinas = [
    "Superior izquierda",
    "Superior derecha",
    "Inferior izquierda",
    "Inferior derecha",
]
 
clock = pygame.time.Clock()
 
 

def dibujar_inicio(tick,high_score):
    print("estoy dibujando el inicio")
    pantalla.fill(NEGRO)

    texto_hs    = fuente_chica.render("HIGH SCORE", True, BLANCO)
    texto_pts = fuente_mediana.render(str(high_score), True, AMARILLO)
    pantalla.blit(texto_hs,  (ANCHO // 2 - texto_hs.get_width()  // 2, 40))
    pantalla.blit(texto_pts, (ANCHO // 2 - texto_pts.get_width() // 2, 70))

    titulo = fuente_grande.render("PAC-MAN", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 180))
 
    if (tick // 30) % 2 == 0:
        msg = fuente_mediana.render("Presiona ENTER para jugar", True, BLANCO)
        pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, 420))
 
 
def dibujar_seleccion(seleccionados):
  
    pantalla.fill(NEGRO)
 
    titulo = fuente_mediana.render("ELEGÍ 4 FANTASMAS", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))
 
    contador = fuente_chica.render(
        f"Seleccionados: {len(seleccionados)}/4  |  Presioná 1-6 para elegir",
        True, BLANCO
    )
    pantalla.blit(contador, (ANCHO // 2 - contador.get_width() // 2, 65))
 
    y_base = 120
    for i, fantasma in enumerate(fantasmas_disponibles):
        y = y_base + i * 72
        elegido = i in seleccionados

        if elegido:
            pygame.draw.rect(pantalla, GRIS_OSCURO, (60, y - 6, ANCHO - 120, 62), border_radius=8)
            pygame.draw.rect(pantalla, AMARILLO,    (60, y - 6, ANCHO - 120, 62), 2, border_radius=8)
 
        num_txt = fuente_mediana.render(str(i + 1), True, AMARILLO)
        pantalla.blit(num_txt, (75, y + 8))
 
        pygame.draw.circle(pantalla, fantasma["color"], (140, y + 22), 20)
 
        nombre_txt = fuente_mediana.render(fantasma["nombre"], True, fantasma["color"])
        pantalla.blit(nombre_txt, (175, y + 2))
 
        desc_txt = fuente_mini.render(fantasma["desc"], True, GRIS)
        pantalla.blit(desc_txt, (175, y + 34))
 
        if elegido:
            check = fuente_mediana.render("✓", True, AMARILLO)
            pantalla.blit(check, (ANCHO - 90, y + 10))
 
    if len(seleccionados) == 4:
        msg = fuente_chica.render("Presiona ENTER para continuar", True, AMARILLO)
    else:
        msg = fuente_chica.render("Necesitas elegir exactamente 4", True, GRIS)
    pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, ALTO - 38))
 
 
def dibujar_asignacion(fantasmas_elegidos, indice_actual, esquinas_asignadas):
    pantalla.fill(NEGRO)
    fantasma = fantasmas_elegidos[indice_actual]
 
    titulo = fuente_mediana.render("ASIGNÁ UNA ESQUINA", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 25))
 
    prog = fuente_chica.render(
        f"Fantasma {indice_actual + 1} de {len(fantasmas_elegidos)}",
        True, GRIS
    )
    pantalla.blit(prog, (ANCHO // 2 - prog.get_width() // 2, 70))

    pygame.draw.circle(pantalla, fantasma["color"], (ANCHO // 2, 170), 38)
 
    nombre_txt = fuente_mediana.render(fantasma["nombre"], True, fantasma["color"])
    pantalla.blit(nombre_txt, (ANCHO // 2 - nombre_txt.get_width() // 2, 218))
 
    pregunta = fuente_chica.render("¿A qué esquina va este fantasma?", True, BLANCO)
    pantalla.blit(pregunta, (ANCHO // 2 - pregunta.get_width() // 2, 268))
 
    y_base = 320
    for i, nombre_esq in enumerate(nombres_esquinas):
        y = y_base + i * 52

        ya_usada = i in esquinas_asignadas.values()
 
        if ya_usada:
            color_txt  = GRIS_OSCURO
            color_num  = GRIS_OSCURO
            fondo_rect = GRIS_OSCURO
        else:
            color_txt  = BLANCO
            color_num  = AMARILLO
            fondo_rect = GRIS_OSCURO
 

        pygame.draw.rect(pantalla, fondo_rect, (160, y, ANCHO - 320, 40), border_radius=6)
        if not ya_usada:
            pygame.draw.rect(pantalla, AMARILLO, (160, y, ANCHO - 320, 40), 1, border_radius=6)
 

        num = fuente_mediana.render(str(i + 1), True, color_num)
        pantalla.blit(num, (175, y + 4))
 

        esq_txt = fuente_chica.render(nombre_esq, True, color_txt)
        pantalla.blit(esq_txt, (220, y + 8))

        if ya_usada:
            for fant_nombre, esq_idx in esquinas_asignadas.items():
                if esq_idx == i:
                    ocupada = fuente_mini.render(f"(Asignada a {fant_nombre})", True, GRIS)

            rect_ocupada = ocupada.get_rect()
            rect_ocupada.center = (ANCHO // 2, y + 20)

            pantalla.blit(ocupada, rect_ocupada)
 
 
def dibujar_resumen(fantasmas_elegidos, esquinas_asignadas):
    
    pantalla.fill(NEGRO)
 
    titulo = fuente_grande.render("LISTOS!", True, AMARILLO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))
 
    subtitulo = fuente_chica.render("Configuración del juego", True, GRIS)
    pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 110))
 
    pygame.draw.line(pantalla, AMARILLO, (100, 140), (ANCHO - 100, 140), 1)
 
    y_base = 165
    for i, fantasma in enumerate(fantasmas_elegidos):
        y = y_base + i * 80
 
        pygame.draw.circle(pantalla, fantasma["color"], (140, y + 22), 22)
 
        nombre_txt = fuente_mediana.render(fantasma["nombre"], True, fantasma["color"])
        pantalla.blit(nombre_txt, (180, y + 4))
 
        esq_idx  = esquinas_asignadas[fantasma["nombre"]]
        esq_nombre = nombres_esquinas[esq_idx]
        flecha   = fuente_chica.render(f"→  {esq_nombre}", True, BLANCO)
        pantalla.blit(flecha, (180, y + 38))
 
    pygame.draw.line(pantalla, AMARILLO, (100, ALTO - 80), (ANCHO - 100, ALTO - 80), 1)
 
    msg = fuente_mediana.render("Presiona ENTER para comenzar la partida", True, AMARILLO)
    pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, ALTO - 55))

def pantalla_inicio(high_score):
 
    estado = "inicio"         
 
    seleccionados      = []   
    fantasmas_elegidos = []    
    esquinas_asignadas = {}   
    indice_asignacion  = 0     
    tick               = 0     
    while True:
        tick += 1
 
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
 
               
                if estado == "inicio":
                    if event.key == pygame.K_RETURN:
                        estado = "seleccion"
 
               
                elif estado == "seleccion":
                    teclas_num = {
                        pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
                        pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
                    }
                    if event.key in teclas_num:
                        idx = teclas_num[event.key]
                        if idx in seleccionados:
                            seleccionados.remove(idx)       
                        elif len(seleccionados) < 4:
                            seleccionados.append(idx)      
 
                    if event.key == pygame.K_RETURN and len(seleccionados) == 4:
                       
                        fantasmas_elegidos = [fantasmas_disponibles[i] for i in seleccionados]
                        estado = "asignacion"
                        indice_asignacion = 0
 
                elif estado == "asignacion":
                    teclas_esq = {
                        pygame.K_1: 0, pygame.K_2: 1,
                        pygame.K_3: 2, pygame.K_4: 3,
                    }
                    if event.key in teclas_esq:
                        esq_idx = teclas_esq[event.key]
                        
                        if esq_idx not in esquinas_asignadas.values():
                            nombre_actual = fantasmas_elegidos[indice_asignacion]["nombre"]
                            esquinas_asignadas[nombre_actual] = esq_idx
                            indice_asignacion += 1
                            if indice_asignacion >= len(fantasmas_elegidos):
                                estado = "resumen"
 
                
                elif estado == "resumen":
                    if event.key == pygame.K_RETURN:
                        
                        return fantasmas_elegidos, esquinas_asignadas
 
        
        if estado == "inicio":
            dibujar_inicio(tick, high_score)
 
        elif estado == "seleccion":
            dibujar_seleccion(seleccionados)
 
        elif estado == "asignacion":
            dibujar_asignacion(fantasmas_elegidos, indice_asignacion, esquinas_asignadas)
 
        elif estado == "resumen":
            dibujar_resumen(fantasmas_elegidos, esquinas_asignadas)
 
        pygame.display.flip()
        clock.tick(60)
 
 
if __name__ == "__main__":
    resultado = pantalla_inicio(0)
 
    fantasmas, esquinas = resultado
 
    print("\n--- Configuración elegida ---")
    for f in fantasmas:
        esq = esquinas[f["nombre"]]
        print(f"  {f['nombre']}  →  {nombres_esquinas[esq]}")
 
    pygame.quit()
    sys.exit()
 