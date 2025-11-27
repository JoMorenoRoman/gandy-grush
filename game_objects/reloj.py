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
CALLBACK = "callback"
COMIENZO = "comienzo"

def iniciar(duration_sec:int, on_timeout):
    estado.clear()
    clear()
    estado[DURACION] = duration_sec
    estado[CALLBACK] = on_timeout
    estado[COMIENZO] = time.time()
    graphics.addRenderer(render, clear)
    render()
    
def clear():
    layer.clear()
    graphics.removeLayer(layer)
    
def render():
    layer.clear()
    graphics.addLayer(layer)
    limite = display.construir_limite(0.3, 0, 0)
    borde = display.createGraphic(0.7, 0.7, limite)
    display.align(borde[1], 1, 1, limite)
    borde[0].fill(config.MAINCOLOR)
    layer.append(borde)
    interior = display.createGraphic(1, 1, borde[1].inflate(-10, -10))
    display.align(interior[1], 0, 0)
    interior[0].fill(config.BACKGROUND)
    layer.append(interior)
    eventq.add_frame_func(texto_reloj, True, timer.seconds(2), timer.seconds(0.3))
    texto_reloj()
        
def texto_reloj():
    if len(layer) == 0:
        return
    elapsed = time.time() - estado[COMIENZO]
    remaining = max(0, int(estado[DURACION] - elapsed))

    mins = remaining // 60
    secs = remaining % 60
    text = f"{mins:02}:{secs:02}"
    
    surf_text, rect_text = texto.subtitulo(text)
    if len(layer) < 3:
        borde = display.createRect(0.9, 0.9, layer[-1][1])
        tupla = (surf_text, rect_text)
        tupla = display.encastrar([tupla], borde)[0]
        display.align(tupla[1], 0, 0)
        layer.append(tupla)
    else:
        existente = layer[-1]
        surf_text = pygame.transform.smoothscale(surf_text, (existente[1].w, existente[1].h))
        rect_text = surf_text.get_rect()
        display.align(rect_text, 1, 1, layer[-2][1])
        layer[-1] = (surf_text, rect_text)
        
    if remaining <= 0:
        estado[CALLBACK]()