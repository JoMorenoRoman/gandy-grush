
import pygame

MAINCOLOR = (255, 182, 193)
"""tuple[int, int, int]: Color principal en formato RGB."""

BACKGROUND = (221, 160, 221)
"""tuple[int, int, int]: Color de fondo en formato RGB."""

TEXT_COLOR = (100, 100, 100)
"""tuple[int, int, int]: Color del texto en formato RGB."""

MENU_BG = (20, 20, 20)
"""tuple[int, int, int]: Color de fondo del menú."""

BLANCO = (230, 230, 230)
"""tuple[int, int, int]: Color blanco personalizado."""

ROWS = 8
"""int: Número de filas en la grilla principal."""

COLUMNS = 8
"""int: Número de columnas en la grilla principal."""

framerate: int = 60
"""int: Tasa de fotogramas por segundo (FPS)."""

screen: pygame.Surface = pygame.display.set_mode((800, 600))
"""pygame.Surface: Superficie principal de la ventana del juego."""

background: pygame.Surface
"""pygame.Surface: Imagen de fondo actual (se asigna dinámicamente)."""

ceventsBase: int = pygame.NUMEVENTS + 1
"""int: Base para generar eventos personalizados en Pygame."""
