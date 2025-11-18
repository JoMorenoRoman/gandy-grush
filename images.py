import os
import pygame

def load_png(name:str, size:tuple[int, int]):
    """ Load image and return image object"""
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    image = pygame.transform.scale(image, size)
    return image

def tint_png(image:pygame.Surface, color):
    tinted = image.copy()
    tinted.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    tinted.fill(color + (0,), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted