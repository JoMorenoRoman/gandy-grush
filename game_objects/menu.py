from typing import Any, Callable
import pygame
import display
import config
import events
import pantallas.juego

_opciones:list[tuple[str,Callable]]
_borde = 20

def iniciar(options:list[tuple[str,Callable]]):
    global _opciones
    _opciones = options
    render()
    
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
    font = config.font
    for i in range(len(_opciones)):
        text = font.render(_opciones[i][0], True, config.TEXT_COLOR)
        pos = text.get_rect(centerx = rect.centerx, y = rect.y + _borde + (display.text_height() * (i * 2 + 1)))
        display.screen.blit(text, pos)
        events.addCollision(pos, _opciones[i][1])
    return

def menu_inicio():
    opciones = [
        ("Inicio", pantallas.juego.iniciar()),
        ("Cambiar Resolucion", menu_resoluciones),
        ("Cerrar Juego", events.quit),
    ]
    iniciar(opciones)
    
def menu_resoluciones():
    opciones = [
        ("800x600", lambda: display.set_screen(600, 800)),
        ("1200x800", lambda:display.set_screen(800, 1200)),
        ("1920x1080", lambda: display.set_screen(1080, 1920)),
        ("volver", menu_inicio)
    ]
    iniciar(opciones)