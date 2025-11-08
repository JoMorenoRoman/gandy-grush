import pygame

class Background:
    
    instance = None
    
    def __init__(self, screen:pygame.Surface):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))