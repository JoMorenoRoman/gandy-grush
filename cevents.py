import pygame

_base = pygame.NUMEVENTS + 1

def next():
    global _base
    num = _base
    _base += 1
    return num

SWITCH_TOKENS = next()
