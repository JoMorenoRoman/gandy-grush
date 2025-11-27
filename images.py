import os
import pygame

def load_png(nombre:str, medidas:tuple[int, int]):
    try:
        image = pygame.image.load(os.path.join("data", nombre))
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"no se pudo cargar la imagen: {nombre}")
        raise SystemExit
    image = pygame.transform.scale(image, medidas)
    return image

def colorear_png(imagen:pygame.Surface, color:tuple[int, int, int]):
    copia = imagen.copy()
    copia.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    copia.fill(color + (0,), special_flags=pygame.BLEND_RGBA_ADD)
    return copia