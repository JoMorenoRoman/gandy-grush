from typing import Callable
import pygame
import events
import config
import display
import pantallas.juego
import graphics

_opciones:list[tuple[str,Callable]]
_layer:list[tuple[pygame.Surface, pygame.Rect]] = []
_borde = 20

def iniciar(options:list[tuple[str,Callable]]):
    global _opciones, _layer
    _opciones = options
    if len(_layer) > 0:
        graphics.removeLayer(_layer)
        _layer = []
    render()
    graphics.addRenderer(__name__)
    
def render():
    global _opciones
    height = display.text_height() * (len(_opciones) * 2 + 1)
    max = 0
    for item in _opciones:
        if len(item) > max:
            max = len(item)
    width = max + (display.text_height() * 3)
    rect = pygame.Rect(0, 0, width, height)
    display.align(rect, 1, 1)
    surf = pygame.Surface((rect.w, rect.h))
    surf.fill(config.MENU_BG)
    surf.convert()
    global _layer
    _layer = graphics.addLayer([(surf, rect)])
    font = config.font
    for i in range(len(_opciones)):
        text = font.render(_opciones[i][0], True, config.TEXT_COLOR)
        pos = text.get_rect(centerx = rect.centerx, y = rect.y + _borde + (display.text_height() * (i * 2 + 1)))
        _layer.append((text, pos))
        events.addCollision(pos, _opciones[i][1])
    return

def menu_inicio():
    opciones = [
        ("Inicio", pantallas.juego.iniciar),
        ("Cambiar Resolucion", menu_resoluciones),
        ("Cerrar Juego", events.quit),
    ]
    iniciar(opciones)
    
def menu_resoluciones():
    opciones = [
        ("800x600", lambda: display.set_screen(800, 600)),
        ("1200x800", lambda:display.set_screen(1200, 800)),
        ("1920x1080", lambda: display.set_screen(1920, 1080)),
        ("volver", menu_inicio)
    ]
    iniciar(opciones)
    
def menu_partida():
    opciones = [
        ("Continuar", ),
        ("Abandonar")
    ]
    iniciar(opciones)