import pygame
import config
import eventq

def next():
    num = config.ceventsBase
    config.ceventsBase += 1
    return num

SWITCH_TOKENS = next()
CAMBIAR_PANTALLA = next()

def cambiar_pantalla(event:pygame.event.Event):
    if event.dict and event.dict.get("dest", None):
        event.dict["dest"]()