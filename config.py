import pygame

MAINCOLOR = (255, 182, 193)
BACKGROUND = (221, 160, 221)
TEXT_COLOR = (100, 100, 100)
MENU_BG = (20, 20, 20)
BLANCO = (230, 230, 230)
ROWS = 8
COLUMNS = 8


framerate:int = 60
screen:pygame.Surface = pygame.display.set_mode((800, 600))
background:pygame.Surface
ceventsBase:int = pygame.NUMEVENTS + 1