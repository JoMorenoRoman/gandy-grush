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
    graphics.addRenderer(__name__)
    render()

def render():
    reset()
    tercio = display.construir_limite(0, 2, 0)
    limite = display.combinar_limites(display.construir_limite(0, 0, 1, tercio), display.construir_limite(0, 2, 2, tercio))
    borde = display.createGraphic(1, 1, limite)
    borde[0].fill(config.MAINCOLOR)
    display.align(borde[1], 1, 1, limite)
    capa.append(borde)
    interior = display.createGraphic(1, 1, limite.inflate(-10, -10))
    interior[0].fill(config.BACKGROUND)
    display.align(interior[1], 1, 1, borde[1])
    capa.append(interior)
    texto = config.subtitulo.render("Pausa", True, config.TEXT_COLOR)
    texto = display.encastrar([(texto, texto.get_rect())], display.createRect(0.9, 0.9, interior[1]))[0]
    capa.append(texto)
    colisiones.append(eventq.addCollision(interior[1], lambda: game_objects.menu.menu_partida(estado[REINICIAR]) ))
    
def reset():
    graphics.removeLayer(capa)
    capa.clear()
    if len(colisiones) > 0:
        for colision in colisiones:
            eventq.quitar_colision(colision)
        colisiones.clear()