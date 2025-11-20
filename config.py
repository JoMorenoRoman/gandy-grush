import pygame

BACKGROUND = (0, 0, 0)
MAINCOLOR = (50, 150, 255)
TEXT_COLOR = (100, 100, 100)
MENU_BG = (20, 20, 20)
ROWS = 8
COLUMNS = 8

framerate:int = 60
font:pygame.font.Font
screen:pygame.Surface = pygame.display.set_mode((800, 600))
background:pygame.Surface
ceventsBase:int = pygame.NUMEVENTS + 1