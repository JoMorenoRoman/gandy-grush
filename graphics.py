import pygame
import config
import sys
import eventq

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_renderers:list = []

def addLayer(items:list[tuple[pygame.Surface, pygame.Rect]]):
    _layers.append(items)
    return items
    
def removeLayer(layer:list[tuple[pygame.Surface, pygame.Rect]]):
    _layers.remove(layer)
    
def removeGraphic(graphic:tuple[pygame.Surface, pygame.Rect]):
    for layer in _layers:
        if graphic in layer:
            layer.remove(graphic)
    
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
    for layer in _layers:
        for item in layer:
            config.screen.blit(item[0], item[1])
    pygame.display.flip()
            
def rewriteScreen():
    _layers.clear()
    eventq.clearCollisions()
    for renderer in _renderers:
        sys.modules[renderer].render()
    renderDisplay()
    