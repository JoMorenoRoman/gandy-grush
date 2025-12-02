from typing import Any
import pygame
import config

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_overlay:list[tuple[pygame.Surface, pygame.Rect]] = []
_clipped:dict[int, pygame.Rect] = {}
_temps:dict[int,list[tuple[pygame.Surface, pygame.Rect]]] = {}
_renderers:dict[str, tuple[Any, Any]] = {}

def addLayer(layer:list[tuple[pygame.Surface, pygame.Rect]], clipped:pygame.Rect|None = None):
    _layers.append(layer)
    if clipped:
        _clipped[len(_layers) - 1] = clipped
    return layer
    
def removeLayer(layer:list[tuple[pygame.Surface, pygame.Rect]]):
    if layer in _layers:
        index = _layers.index(layer)
        _layers.remove(layer)
        if _clipped.get(index):
            _clipped.pop(index)
        for key in sorted(_clipped.keys()):
            if key > index:
                _clipped[key - 1] = _clipped[key]
        
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
            
def add_temp(grafico:tuple[pygame.Surface, pygame.Rect], capa:int|None):
    if not capa:
        capa = -1
    
    if _temps.get(capa):
        _temps[capa].append(grafico)
    else:
        _temps[capa] = [grafico]
    
def reset():
    _layers.clear()
    _clipped.clear()
    _temps.clear()
    _overlay.clear()
    for _, clear in _renderers.values():
        if clear:
            clear()
    _renderers.clear()
    
def addRenderer(ref, render, clear):
    _renderers[ref] = (render, clear)
        
def re_render():
    for render, _ in _renderers.values():
        if render:
            render()
    
def setBackground(background:pygame.Surface):
    config.background = background
    
def renderizar():
    config.screen.blit(config.background, (0, 0))
    for i, layer in enumerate(_layers):
        clip = _clipped.get(i)  
        if clip:
            config.screen.set_clip(clip)
        for (surf, rect) in layer:
            config.screen.blit(surf, rect)
        if _temps.get(i):
            for (surf, rect) in _temps[i]:
                config.screen.blit(surf, rect)
        config.screen.set_clip(None)
    if _temps.get(-1):
        for (surf, rect) in _temps[-1]:
            config.screen.blit(surf, rect)
    _temps.clear()
    pygame.display.flip()
    