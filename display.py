import pygame
import graphics

screen:pygame.Surface = pygame.display.set_mode((640, 480))

def set_screen(width:int, height:int):
    global screen 
    screen = pygame.display.set_mode((width, height))
    graphics.rewriteScreen()
    
def text_height(): 
    return int(screen.get_height() / 20)

def align(item:pygame.Rect, x_third, y_third, ref:pygame.Rect | None = None):
    if not ref:
        ref = screen.get_rect()
    x_size = ref.w / 6
    x_pos = x_size * (x_third * 2 + 1)
    x_pos -= item.width / 2
    y_size = ref.h / 6
    y_pos = y_size * (y_third * 2 + 1)
    y_pos -= item.height / 2
    item.x = x_pos
    item.y = y_pos
    
def matrix_align(rect:pygame.Rect, x_pos, y_pos, container:pygame.Rect):
    rect.x = container.x + (rect.w * x_pos)
    rect.y = container.y + (rect.h * y_pos)
    
def createGraphic(x_proportion:float, y_proportion:float, ref:pygame.Rect | None = None):
    if not ref:
        ref = screen.get_rect()
    rect = pygame.Rect(0, 0, ref.w * x_proportion, ref.h * y_proportion)
    surf = pygame.Surface((rect.w, rect.h))
    return (surf, rect)

def createRect(x_proportion:float, y_proportion:float, ref:pygame.Rect | None = None):
    return createGraphic(x_proportion, y_proportion, ref)[1]
    
def square(rect:pygame.Rect):
    if rect.w == 0:
        rect = pygame.Rect(rect.left, rect.top, rect.h, rect.h)
    else:
        rect = pygame.Rect(rect.left, rect.top, rect.w, rect.w)
    return rect
    