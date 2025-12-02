import pygame
import config
import display
import eventq
import graphics
import game_objects.menu as menu
import images
import sonido
import texto

graficos = []

def iniciar():
    eventq.full_reset()
    graphics.addRenderer("inicio", render, clear)
    render()
    menu.menu_inicio()
    sonido.reproducir_musica(sonido.MUSICA_MENU)
    
def render():
    clear()
    graphics.setBackground(images.load_png("title_background.png", config.screen.get_size()))
    text = texto.titulo("Gandy Grush")
    display.align(text[1], 1, 0)
    graficos.append(text)
    graphics.addLayer(graficos)
    
def clear():
    if graficos:
        graphics.removeLayer(graficos)
        graficos.clear()
