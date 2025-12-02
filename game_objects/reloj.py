import time
import pygame
import config
import display
import eventq
import graphics
import texto
import timer

estado= {}
layer = []
DURACION = "duracion"
COMIENZO = "comienzo"
CALLBACK = "callback"

def iniciar(segundos:int, callback):
    estado.clear()
    estado[DURACION] = segundos
    estado[COMIENZO] = time.time()
    estado[CALLBACK] = callback
    graphics.addRenderer(None, clear)
    
def clear():
    layer.clear()
    graphics.removeLayer(layer)
    
def render(tablero:pygame.Rect):
    clear()
    graphics.addLayer(layer)
    borde = display.createGraphic(1/9, 1/9, color=config.MAINCOLOR)
    pantalla = config.screen.get_rect()
    display.centrar_entre(borde[1], (pantalla.left, pantalla.centery), (tablero.left, pantalla.centery))
    display.alinear_en(borde, tablero, posicion=display.PRINCIPIO)
    layer.append(borde)
    interior = display.createGraphic(0.95, 0.95, borde[1], color=config.BACKGROUND)
    layer.append(interior)
    eventq.add_frame_func(texto_reloj, True, timer.seconds(0.1), timer.seconds(0.1))
    texto_reloj()
        
def texto_reloj():
    if len(layer) == 0:
        return
    
    elapsed = time.time() - estado[COMIENZO]
    remaining = max(0, int(estado[DURACION] - elapsed))

    text = f"{remaining:02}"
    
    surf_text, rect_text = texto.subtitulo(text)
    if len(layer) < 3:
        borde = display.createRect(0.9, 0.9, layer[-1][1])
        tupla = (surf_text, rect_text)
        tupla = display.encastrar([tupla], borde)[0]
        display.align(rect_text, 1, 1, layer[-2][1])
        layer.append(tupla)
    else:
        existente = layer[-1]
        surf_text = pygame.transform.smoothscale(surf_text, (existente[1].w, existente[1].h))
        rect_text = surf_text.get_rect()
        display.align(rect_text, 1, 1, layer[-2][1])
        layer[-1] = (surf_text, rect_text)
        
    if remaining <= 0:
        estado[CALLBACK]()