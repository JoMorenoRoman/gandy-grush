import pygame
import animations
import display
import eventq
from game_objects import boton_pausa, reloj, scoretable
import graphics
import config
import game_objects.tokens as tokens
import game_objects.tablero as tablero
import pantallas.inicio
import timer

_tablero:dict = {}
_funcs:list[dict] = []
_capas:list[list[tuple[pygame.Surface, pygame.Rect]]] = []

def iniciar():
    eventq.full_reset()
    _tablero.clear()
    _tablero[tablero.MATRIX] = []
    _tablero[tablero.BUSY] = False
    _tablero[tablero.ANIM_SPEED] = 0.5
    _tablero[tablero.PUNTAJE] = 0
    _tablero["capa"] = []
    tablero.iniciar(_tablero[tablero.MATRIX], config.ROWS, config.COLUMNS)
    graphics.addRenderer(render, clear)
    reloj.iniciar(60, lambda: pantallas.inicio.iniciar())
    boton_pausa.iniciar()
    render()
    
def render():
    _funcs.clear()
    outer = display.createRect(0, 2/3)
    outer = display.square(outer)
    outer = display.createGraphic(1, 1, outer)
    outer[0].fill(config.MAINCOLOR)
    display.align(outer[1], 1, 1)
    capa = [outer]
    graphics.addLayer(capa)
    _capas.append(capa)
    
    inner = display.createRect(1, 1, outer[1].inflate(-10, -10))
    display.make_multiple(inner, config.COLUMNS, config.ROWS)
    inner = display.createGraphic(1, 1, inner)
    inner[0].fill(config.BACKGROUND)
    display.align(inner[1], 1, 1)
    capa = [inner]
    graphics.addLayer(capa)
    _capas.append(capa)
    
    token_rect = display.createRect(1/config.ROWS, 1/config.COLUMNS, inner[1])
    tokens.render(token_rect.size)
    tablero.render(_tablero, inner[1], token_rect)
    scoretable.iniciar(capa[0][1])
    _funcs.append(eventq.add_frame_func(lambda: scoretable.cambiarPuntaje(_tablero[tablero.PUNTAJE]), False, 15, 15))
    _funcs.append(eventq.add_frame_func(lambda: tablero.buscar_matches(_tablero)))
    _funcs.append(eventq.add_frame_func(lambda: tablero.fill_empty(_tablero, _tablero["capa"], inner[1], token_rect)))
    duracion = timer.seconds(0.35)
    _funcs.append(eventq.add_frame_func(lambda: titilar(_tablero[tablero.MATRIX], 0.35), True, duracion, duracion))
    
def titilar(matrix:list[list[dict]], duracion:float):
    for row in matrix:
        for token in row:
            if token and token[tablero.STATE] == tokens.HIGHLIGHT:
                animations.titilar(token[tablero.GRAPHIC], duracion, 240)
    
def clear():
    if _capas:
        for capa in _capas:
            graphics.removeLayer(capa)
    if _tablero.get("capa", None):
        graphics.removeLayer(_tablero["capa"])
    if _funcs:
        for func in _funcs:
            eventq.quitar_frame_func(func)
    _tablero.clear()
    _funcs.clear()