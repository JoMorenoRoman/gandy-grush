from typing import Any
import pygame
import config

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_overlay:list[tuple[pygame.Surface, pygame.Rect]] = []
_clipped:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_temps:dict[int,list[tuple[pygame.Surface, pygame.Rect]]] = {}
_renderers:list[tuple[Any, Any]] = []

def addLayer(layer:list[tuple[pygame.Surface, pygame.Rect]], clipped:bool = False):
    _layers.append(layer)
    if clipped:
        _clipped.append(layer)
    
def removeLayer(layer:list[tuple[pygame.Surface, pygame.Rect]]):
    if layer in _layers:
        _layers.remove(layer)    
    if layer in _clipped:
        _clipped.remove(layer)
        
def buscar_capa(grafico:tuple[pygame.Surface, pygame.Rect]):
    index = None
    for i, capa in enumerate(_layers):
        if grafico in capa:
            index = i
    return index
            
    
def removeGraphic(graphic:tuple[pygame.Surface, pygame.Rect]):
    for layer in _layers:
        if graphic in layer:
            layer.remove(graphic)
            return layer
    return None
            
def add_temp(grafico:tuple[pygame.Surface, pygame.Rect], capa:int):
    if _temps.get(capa):
        _temps[capa].append(grafico)
    else:
        _temps[capa] = [grafico]
    
def reset():
    _layers.clear()
    _clipped.clear()
    _temps.clear()
    _overlay.clear()
    for _, clear in _renderers:
        if clear:
            clear()
    _renderers.clear()
    
def addRenderer(render, clear):
    _renderers.append((render, clear))
        
def re_render():
    for render, _ in _renderers:
        if render:
            render()
    
def setBackground(background:pygame.Surface):
    config.background = background
    
def renderizar():
    config.screen.blit(config.background, (0, 0))
    for i, layer in enumerate(_layers):
        if layer in _clipped:
            config.screen.set_clip(_layers[i - 1][0][1])
        for (surf, rect) in layer:
            config.screen.blit(surf, rect)
        if _temps.get(i):
            for (surf, rect) in _temps[i]:
                config.screen.blit(surf, rect)
        config.screen.set_clip(None)
    _temps.clear()
    pygame.display.flip()
    