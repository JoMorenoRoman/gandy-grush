import pygame

class EventQueue:
    def __init__(self):
        pass
    
    def start(self):
        while True:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return