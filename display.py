import pygame
import config
import graphics
from utils import min, max

def set_screen(width:int, height:int):
    config.screen = pygame.display.set_mode((width, height))
    graphics.re_render()
    
def text_height(): 
    return int(config.screen.get_height() / 20)

def align(item:pygame.Rect, x_third, y_third, ref:pygame.Rect | None = None):
    if not ref:
        ref = config.screen.get_rect()
    x_sixth = ref.w / 6
    x_pos = ref.x + (x_sixth * ((x_third * 2) + 1))
    x_pos -= item.width / 2
    y_sixth = ref.h / 6
    y_pos = ref.y + (y_sixth * ((y_third * 2) + 1))
    y_pos -= item.height / 2
    item.x = x_pos
    item.y = y_pos
    
def matrix_align(matrix:list[list[dict]], token:pygame.Rect, x, y, container:pygame.Rect):
    token.x = container.x + (token.w * x)
    token.y = container.y + (token.h * (len(matrix[0]) - y - 1))
    
def createGraphic(x_proportion:float, y_proportion:float, ref:pygame.Rect | None = None):
    if not ref:
        ref = config.screen.get_rect()
    rect = pygame.Rect(0, 0, ref.w * x_proportion, ref.h * y_proportion)
    surf = pygame.Surface((rect.w, rect.h))
    rect.centerx = ref.centerx
    rect.centery = ref.centery
    return (surf, rect)

def createRect(x_proportion:float, y_proportion:float, ref:pygame.Rect | None = None):
    return createGraphic(x_proportion, y_proportion, ref)[1]
    
def square(rect:pygame.Rect):
    if rect.w == 0:
        rect = pygame.Rect(rect.left, rect.top, rect.h, rect.h)
    else:
        rect = pygame.Rect(rect.left, rect.top, rect.w, rect.w)
    return rect

def make_multiple(rect:pygame.Rect, xMult:int|None, yMult:int|None):
    while xMult and rect.width % xMult != 0:
        rect.width -= 1
        
    while yMult and rect.height % yMult != 0:
        rect.height -= 1
        
def construir_limite(borde:float, tercio_x:int, tercio_y:int, ref:pygame.Rect|None = None):
    if not ref:
        ref = config.screen.get_rect()
    tercio_ancho = ref.width / 3
    tercio_alto = ref.height / 3
    borde_x = tercio_ancho * borde
    borde_y = tercio_alto * borde
    x = ref.x + (tercio_ancho * tercio_x) + borde_x
    y = ref.y + (tercio_alto * tercio_y) + borde_y
    return pygame.Rect(x, y, tercio_ancho - (borde_x * 2), tercio_alto - (borde_y * 2))

def combinar_limites(lim1:pygame.Rect, lim2:pygame.Rect):
    min_x = min([lim1, lim2], lambda f: f.x)
    min_y = min([lim1, lim2], lambda f: f.y)
    ancho = max([lim1, lim2], lambda f: f.right) - min_x
    alto = max([lim1, lim2], lambda f: f.bottom) - min_y
    return pygame.Rect(min_x, min_y, ancho, alto) # type: ignore

def encastrar(graficos:list[tuple[pygame.Surface, pygame.Rect]], ref:pygame.Rect):
    min_x = min(graficos, lambda f: f[1].x)
    min_y = min(graficos, lambda f: f[1].y)
    ancho = max(graficos, lambda f: f[1].right) - min_x
    alto = max(graficos, lambda f: f[1].bottom) - min_y
    
    escala_ancho = ref.width / ancho
    escala_alto = ref.height / alto
    
    escala:float = min([escala_ancho, escala_alto], lambda f: f)
    result:dict[int, tuple[pygame.Surface, pygame.Rect]] = {}
    y = ref.top
    for i in range(len(graficos)):
        graf = graficos[i]
        rect = graf[1]
        surf = graf[0]
        
        if escala > 1:
            nuevo_ancho = rect.width
            nuevo_alto = rect.height
        else:        
            nuevo_ancho = int(rect.width  * escala)
            nuevo_alto = int(rect.height * escala)
        nuevo_surf = pygame.transform.smoothscale(surf, (nuevo_ancho, nuevo_alto))
        rel_x = rect.x - min_x
        rel_y = rect.y - min_y
        nuevo_x = ref.x + int(rel_x * escala)
        nuevo_y = ref.y + int(rel_y * escala)
        nuevo_rect = pygame.Rect(nuevo_x, nuevo_y, nuevo_ancho, nuevo_alto)
        nuevo_rect.centerx = ref.centerx
        nuevo_rect.y = y
        y += nuevo_rect.h
        result[i] = (nuevo_surf, nuevo_rect)
    return result

def crear_container(grafs:dict, borde:float):
    values = list(grafs.values())
    min_x = min(values, lambda f: f[1].x)
    min_y = min(values, lambda f: f[1].y)
    ancho = max(values, lambda f: f[1].right) - min_x
    alto = max(values, lambda f: f[1].bottom) - min_y
    borde_x = ancho * borde 
    min_x -= borde_x
    ancho += borde_x * 2
    borde_y = alto * borde
    min_y -= borde_y
    alto += borde_y * 2
    return pygame.Rect(min_x, min_y, ancho, alto)

def pad(items:list[tuple[pygame.Surface, pygame.Rect]], escala:float):
    res = []
    for item in items:
        res.append(item)
        pad_surf = pygame.transform.smoothscale(item[0], (item[1].w * escala, item[1].h * escala))
        res.append((pad_surf, pad_surf.get_rect()))
    return res

def alinear(items:list[tuple[pygame.Surface, pygame.Rect]]):
    x = 0
    y = 0
    for surf, rect in items:
        rect.x = x
        rect.y = y
        y += rect.height
