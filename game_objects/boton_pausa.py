from typing import Any
import pygame
import config
import display
import eventq
import game_objects.menu
import graphics

estado:dict = {}
REINICIAR = "reiniciar"
capa:list[tuple[pygame.Surface, pygame.Rect]] = []
colisiones:list[tuple[pygame.Rect, Any]] = []

def iniciar(reiniciar):
    estado.clear()
    estado[REINICIAR] = reiniciar
    graphics.addRenderer(render, clear)
    render()

def render():
    clear()
    limite = display.construir_limite(0.25, 2, 0)
    borde = display.createGraphic(1, 1, limite)
    borde[0].fill(config.MAINCOLOR)
    #display.align(borde[1], 1, 1, limite)
    capa.append(borde)
    interior = display.createGraphic(1, 1, borde[1].inflate(-10, -10))
    interior[0].fill(config.BACKGROUND)
    #display.align(interior[1], 1, 1, borde[1])
    capa.append(interior)
    texto = config.subtitulo.render("Pausa", True, config.TEXT_COLOR)
    texto = display.encastrar([(texto, texto.get_rect())], interior[1])[0]
    display.align(texto[1], 1, 1, interior[1])
    capa.append(texto)
    
    colisiones.append(eventq.addCollision(texto[1], lambda: game_objects.menu.menu_partida(estado[REINICIAR])))
    graphics.addLayer(capa)
    
def clear():
    graphics.removeLayer(capa)
    capa.clear()
    if len(colisiones) > 0:
        for colision in colisiones:
            eventq.quitar_colision(colision)
        colisiones.clear()