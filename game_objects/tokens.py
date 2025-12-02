
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
"""list[tuple[int, int, int]]: Colores disponibles para los tokens."""

BOMB = "bomb"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
SUPERS = [BOMB, VERTICAL, HORIZONTAL]
"""list[str]: Tipos especiales de tokens."""

_rendered: list[pygame.Surface] = []
_supers: list[pygame.Surface] = []

IDLE = "idle"
SELECT = "select"
HIGHLIGHT = "highlight"

def render(size: tuple[int, int]):
    """
    Renderiza las imágenes base y especiales para los tokens.

    Args:
        size (tuple[int, int]): Tamaño de cada token.
    """
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

def graficar_token(type: int, super: str | None):
    """
    Devuelve la imagen renderizada para un token.

    Args:
        type (int): Índice del color base.
        super (str | None): Tipo especial (si aplica).

    Returns:
        pygame.Surface: Imagen del token renderizado.
    """
    rendered = _rendered[type]
    if super:
        overlay = _supers[SUPERS.index(super)]
        rendered = rendered.copy()
        rendered.blit(overlay, (0, 0))
    return rendered
