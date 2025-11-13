import pygame
import config
import display
import game_objects.menu

def iniciar():
    background = pygame.Surface(display.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    display.screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 90)
    text = font.render("Gandy Grush", True, config.TEXT_COLOR)
    pos = text.get_rect()
    display.align(pos, 1, 0)
    display.screen.blit(text, pos)
    game_objects.menu.menu_inicio()