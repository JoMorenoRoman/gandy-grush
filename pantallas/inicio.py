import pygame
import config
import display
import eventq
import graphics
import game_objects.menu as menu
import texto

graficos = []

def iniciar():
    eventq.full_reset()
    graphics.addRenderer(render, clear)
    render()
    menu.menu_inicio()
    
def render():
    clear()
    background = pygame.Surface(config.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    graphics.setBackground(background)
    font = pygame.font.Font(None, 90)
    text = texto.titulo("Gandy Grush")
    display.align(text[1], 1, 0)
    graficos.append(text)
    graphics.addLayer(graficos)
    
def clear():
    if graficos:
        graphics.removeLayer(graficos)
        graficos.clear()
    