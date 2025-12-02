import os
import pygame
import config

fonts:list[pygame.font.Font] = []

def normal(texto:str):
    """
    Renderiza un texto con el estilo normal.

    Args:
        texto (str): Texto a renderizar.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: Superficie con el texto renderizado y su rectángulo asociado.
    """
    return render(texto, 0, config.TEXT_COLOR)

def subtitulo(texto:str):
    """
    Renderiza un texto con el estilo subtítulo.

    Args:
        texto (str): Texto a renderizar.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: Superficie con el texto renderizado y su rectángulo asociado.
    """
    return render(texto, 1, config.TEXT_COLOR)

def titulo(texto:str):
    """
    Renderiza un texto con el estilo 'título'.

    Args:
        texto (str): Texto a renderizar.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: Superficie con el texto renderizado y su rectángulo asociado.
    """
    return render(texto, 2, config.TEXT_COLOR)
    
def render(texto:str, index:int, color:tuple[int, int, int]):
    """
    Renderiza un texto usando una fuente específica y color.

    Args:
        texto (str): Texto a renderizar.
        index (int): Índice de la fuente en la lista global `fonts`.
        color (tuple[int, int, int]): Color del texto en formato RGB.

    Returns:
        tuple[pygame.Surface, pygame.Rect]: Superficie con el texto renderizado y su rectángulo asociado.
    """
    surf = fonts[index].render(texto, True, color)
    return (surf, surf.get_rect())

def reset():
    """
    Reinicia la configuración de los textos llamando a la funcion `init()`.
    """
    init()

def init():
    """
    Inicializa la lista de fuentes `fonts` con diferentes tamaños.

        - Calcula el tamaño base en función de la altura de la pantalla (`config.screen.get_height()`).
        - Carga la fuente 'alagard.ttf' desde la carpeta 'data'.
        - Agrega tres tamaños de fuente: normal, subtítulo y título.
    """
    fonts.clear()
    size = int(config.screen.get_height() / 20)
    alagard = os.path.join("data", "alagard.ttf")
    fonts.append(pygame.font.Font(alagard, size))
    fonts.append(pygame.font.Font(alagard, round(size * 1.5)))
    fonts.append(pygame.font.Font(alagard, round(size * 3)))