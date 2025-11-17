import pygame
import display
import sys
import events

_layers:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_background:pygame.Surface
_renderers:list = []

def addLayer(items:list[tuple[pygame.Surface, pygame.Rect]]):
    global _layers
    _layers.append(items)
    return items
    
def removeLayer(layer:list[tuple[pygame.Surface, pygame.Rect]]):
    global _layers
    _layers.remove(layer)
    
def clear():
    global _layers
    _layers.clear()
    events.clearCollisions()
    
def addRenderer(renderer):
    global _renderers
    if renderer not in _renderers:
        _renderers.append(renderer)
    
def setBackground(background:pygame.Surface):
    global _background
    _background = background
    
def renderDisplay():
    global _layers, _background
    display.screen.blit(_background, (0, 0))
    for layer in _layers:
        for item in layer:
            display.screen.blit(item[0], item[1])
    pygame.display.flip()
            
def rewriteScreen():
    global _renderers, _layers, _background
    _layers.clear()
    events.clearCollisions()
    for renderer in _renderers:
        sys.modules[renderer].render()
    renderDisplay()
    