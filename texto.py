import os
import pygame

import config

fonts:list[pygame.font.Font] = []

def normal(texto:str):
    return render(texto, 0, config.TEXT_COLOR)

def subtitulo(texto:str):
    return render(texto, 1, config.TEXT_COLOR)

def titulo(texto:str):
    return render(texto, 2, config.TEXT_COLOR)
    
def render(texto:str, index:int, color:tuple[int, int, int]):
    surf = fonts[index].render(texto, True, color)
    return (surf, surf.get_rect())

def reset():
    init()

def init():
    fonts.clear()
    size = int(config.screen.get_height() / 20)
    alagard = os.path.join("data", "alagard.ttf")
    fonts.append(pygame.font.Font(alagard, size))
    fonts.append(pygame.font.Font(alagard, round(size * 1.5)))
    fonts.append(pygame.font.Font(alagard, round(size * 3)))