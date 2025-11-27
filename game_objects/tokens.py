import images
import pygame

types = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (0, 125, 125) 
]
BOMB = "bomb"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
SUPERS = [BOMB, VERTICAL, HORIZONTAL]

_rendered:list[pygame.Surface] = []
_supers:list[pygame.Surface] = []

IDLE = "idle"
SELECT = "select"
HIGHLIGHT = "highlight"

def render(size:tuple[int, int]):
    _rendered.clear()
    _supers.clear()
    image = images.load_png("token.png", size)
    for i in range(len(types)):
        color = types[i]
        _rendered.append(images.colorear_png(image, color))
    for super in SUPERS:
        image = images.load_png(super + ".png", size)
        image.set_alpha(200)
        _supers.append(image)

def graficar_token(type:int, super:str|None):
    rendered = _rendered[type]
    if super:
        overlay = _supers[SUPERS.index(super)]
        rendered = rendered.copy()
        rendered.blit(overlay, (0, 0))
    return rendered
    