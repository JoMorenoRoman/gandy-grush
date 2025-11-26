from typing import Any
import pygame
import config

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_clipped:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_temps:list[tuple[pygame.Surface, pygame.Rect]] = []
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
    
def removeGraphic(graphic:tuple[pygame.Surface, pygame.Rect]):
    for layer in _layers:
        if graphic in layer:
            layer.remove(graphic)
            
def add_temp(graphic:tuple[pygame.Surface, pygame.Rect]):
    _temps.append(graphic)
    
def reset():
    _layers.clear()
    _clipped.clear()
    _temps.clear()
    _renderers.clear()
    
def addRenderer(render, clear):
    _renderers.append((render, clear))
        
def clearRenderers():
    for render, clear in _renderers:
        if clear:
            clear()
    _renderers.clear()
    
def re_render():
    for render, clear in _renderers:
        if render:
            render()
    
def setBackground(background:pygame.Surface):
    config.background = background
    
def renderDisplay():
    config.screen.blit(config.background, (0, 0))
    for i in range(len(_layers)):
        layer = _layers[i]
        if layer in _clipped:
            config.screen.set_clip(_layers[i - 1][0][1])
        for item in layer:
            config.screen.blit(item[0], item[1])
        config.screen.set_clip(None)
    for item in _temps:
        config.screen.blit(item[0], item[1])
    _temps.clear()
    pygame.display.flip()
    