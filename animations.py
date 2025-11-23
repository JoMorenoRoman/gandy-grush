import pygame

animations:dict = {}

def shake_token(seconds:float, graphic:tuple[pygame.Surface, pygame.Rect]):
    return

def switch_tokens(token1:tuple[pygame.Surface, pygame.Rect], token2:tuple[pygame.Surface, pygame.Rect]):
    return

def destroy_token(token:tuple[pygame.Surface, pygame.Rect]):
    return

def animate(origin:int, dest:int, interval:int):
    num = dest - origin
    origin += round(num / interval)
    return (origin, dest, interval - 1) 