from operator import indexOf
import pygame
import config
import sys
import eventq

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_clipped:set[int] = set()
_temps:list[tuple[pygame.Surface, pygame.Rect]] = []
_renderers:list = []

def addLayer(items:list[tuple[pygame.Surface, pygame.Rect]], clipped:bool = False):
    _layers.append(items)
    if clipped:
        _clipped.add(_layers.index(items))
    return items
    
def removeLayer(layer:list[tuple[pygame.Surface, pygame.Rect]]):
    i = _layers.index(layer)
    if layer in _layers:
        i = _layers.index(layer)
        if i in _clipped:
            _clipped.remove(i)
        _layers.remove(layer)
    
def removeGraphic(graphic:tuple[pygame.Surface, pygame.Rect]):
    for layer in _layers:
        if graphic in layer:
            layer.remove(graphic)
            
def add_temp(graphic:tuple[pygame.Surface, pygame.Rect]):
    _temps.append(graphic)
    
def clear():
    _layers.clear()
    eventq.clearCollisions()
    
def addRenderer(renderer):
    if renderer not in _renderers:
        _renderers.append(renderer)
    
def setBackground(background:pygame.Surface):
    config.background = background
    
def renderDisplay():
    config.screen.blit(config.background, (0, 0))
    for i in range(len(_layers)):
        layer = _layers[i]
        if i in _clipped:
            config.screen.set_clip(_layers[i - 1][0][1])
        for item in layer:
            config.screen.blit(item[0], item[1])
        config.screen.set_clip(None)
    for item in _temps:
        config.screen.blit(item[0], item[1])
    _temps.clear()
    pygame.display.flip()
            
def rewriteScreen():
    _layers.clear()
    eventq.clearCollisions()
    for renderer in _renderers:
        sys.modules[renderer].render()
    renderDisplay()
    