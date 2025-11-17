from tkinter import W
import pygame
import graphics

screen:pygame.Surface = pygame.display.set_mode((640, 480))

def set_screen(width:int, height:int):
    global screen 
    screen = pygame.display.set_mode((width, height))
    graphics.rewriteScreen()
    
def text_height(): 
    global screen
    return int(screen.get_height() / 20)

def align(item:pygame.Rect, x_third, y_third):
    global screen
    x_size = screen.get_width() / 6
    x_pos = x_size * (x_third * 2 + 1)
    x_pos -= item.width / 2
    y_size = screen.get_height() / 6
    y_pos = y_size * (y_third * 2 + 1)
    y_pos -= item.height / 2
    item.x = x_pos
    item.y = y_pos
    
def createGraphic(x_proportion:float, y_proportion:float, ref:pygame.Rect | None = None):
    if not ref:
        global screen
        ref = screen.get_rect()
    rect = pygame.Rect(0, 0, ref.w * x_proportion, ref.h * y_proportion)
    surf = pygame.Surface((rect.w, rect.h))
    return (surf, rect)

    