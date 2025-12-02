from typing import Any
import pygame
import config
import display
import eventq
import game_objects.menu
import graphics
import texto

capa:list[tuple[pygame.Surface, pygame.Rect]] = []
colisiones:list[tuple[pygame.Rect, Any]] = []

def iniciar():
    graphics.addRenderer("boton pausa", render, clear)
    render()

def render():
    clear()
    limite = display.construir_limite(0.3, 2, 0)
    borde = display.createGraphic(1, 1, limite)
    borde[0].fill(config.MAINCOLOR)
    #display.align(borde[1], 1, 1, limite)
    capa.append(borde)
    interior = display.createGraphic(1, 1, borde[1].inflate(-10, -10))
    interior[0].fill(config.BACKGROUND)
    #display.align(interior[1], 1, 1, borde[1])
    capa.append(interior)
    pausa = texto.normal("Pausa")
    pausa = display.encastrar([pausa], interior[1])[0]
    display.align(pausa[1], 1, 1, interior[1])
    
    capa.append(pausa)
    
    colisiones.append(eventq.addCollision(pausa[1], lambda: game_objects.menu.menu_partida()))
    graphics.addLayer(capa)
    
def clear():
    graphics.removeLayer(capa)
    capa.clear()
    if len(colisiones) > 0:
        for colision in colisiones:
            eventq.quitar_colision(colision)
        colisiones.clear()