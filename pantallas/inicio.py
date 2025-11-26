import pygame
import config
import display
import graphics
import game_objects.menu as menu

graficos = []

def iniciar():
    clear()
    render()
    graphics.clearRenderers()
    graphics.addRenderer(render, clear)
    menu.menu_inicio()
    
def render():
    clear()
    background = pygame.Surface(config.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    graphics.setBackground(background)
    font = pygame.font.Font(None, 90)
    text = font.render("Gandy Grush", True, config.TEXT_COLOR)
    pos = text.get_rect()
    display.align(pos, 1, 0)
    graficos.append((text, pos))
    graphics.addLayer(graficos)
    
def clear():
    if graficos:
        for graf in graficos:
            graphics.removeGraphic(graf)
        graficos.clear()
    