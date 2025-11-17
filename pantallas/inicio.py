import pygame
import config
import display
import graphics
import game_objects.menu as menu

def iniciar():
    render()
    menu.menu_inicio()
    
def render():
    background = pygame.Surface(display.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    graphics.setBackground(background)
    font = pygame.font.Font(None, 90)
    text = font.render("Gandy Grush", True, config.TEXT_COLOR)
    pos = text.get_rect()
    display.align(pos, 1, 0)
    graphics.addLayer([(text, pos)])
    graphics.addRenderer(__name__)