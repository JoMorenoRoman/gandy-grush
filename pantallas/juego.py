import pygame
import display
import graphics
import config


def iniciar():
    graphics.clear()
    render()
    graphics.addRenderer(__name__)

def render():
    outer = display.createGraphic(1/3, 1)
    outer[0].fill(config.MAINCOLOR)
    display.align(outer[1], 1, 1)
    graphics.addLayer([outer])
    inner = display.createGraphic(1, 1, outer[1].inflate(-10, -10))
    inner[0].fill(config.BACKGROUND)
    display.align(inner[1], 1, 1)
    graphics.addLayer([inner])