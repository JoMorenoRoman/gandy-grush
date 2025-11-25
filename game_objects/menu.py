from typing import Any
import pygame
import eventq
import config
import display
import pantallas.juego
import graphics

from utils import convertir_csv_a_matriz, leer_archivo_texto

_opciones:list[tuple[str, Any]] = []
_layer:list[tuple[pygame.Surface, pygame.Rect]] = []
_borde = 20

def iniciar(options:list[tuple[str, Any]]):
    _opciones.clear()
    for opt in options:
        _opciones.append(opt)
    if len(_layer) > 0:
        graphics.removeLayer(_layer)
        _layer.clear()
    render()
    graphics.addRenderer(__name__)
    
def render():
    _layer.clear()
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
    _layer.append((surf, rect))
    graphics.addLayer(_layer)
    font = config.font
    for i in range(len(_opciones)):
        text = font.render(_opciones[i][0], True, config.TEXT_COLOR)
        pos = text.get_rect(centerx = rect.centerx, y = rect.y + _borde + (display.text_height() * (i * 2 + 1)))
        _layer.append((text, pos))
        eventq.addCollision(pos, _opciones[i][1])

def menu_inicio():
    opciones = [
        ("Inicio", pantallas.juego.iniciar),
        ("Cambiar Resolucion", menu_resoluciones),
        ("Puntajes Mas Altos", puntajes_mas_altos),
        ("Cerrar Juego", eventq.quit),
    ]
    iniciar(opciones)

def puntajes_mas_altos():
    opciones = []
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz_2 = convertir_csv_a_matriz(datos)
    for row in matriz_2:
        nombre = row[0]
        puntaje = row[1]
        text = f"{nombre}: {puntaje}"
        opciones.append((text, noop))
    opciones.append(("volver", menu_inicio))
    iniciar(opciones)

def noop():
    return

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
        ("Abandonar", pantallas.juego.iniciar)
    ]
    iniciar(opciones)