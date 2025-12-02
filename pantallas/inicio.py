
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
"""list: Lista de gráficos renderizados en la pantalla de inicio."""

def iniciar():
    """
    Inicializa la pantalla de inicio del juego.

    
        - Reinicia eventos y gráficos.
        - Renderiza el título y menú principal.
        - Reproduce música del menú.
    """
    eventq.full_reset()
    graphics.addRenderer("inicio", render, clear)
    render()
    menu.menu_inicio()
    sonido.reproducir_musica(sonido.MUSICA_MENU)

def render():
    """
    Renderiza la pantalla de inicio con el título del juego.
    """
    clear()
    graphics.setBackground(images.load_png("title_background.png", config.screen.get_size()))
    text = texto.titulo("Gandy Grush")
    display.align(text[1], 1, 0)
    graficos.append(text)
    graphics.addLayer(graficos)

def clear():
    """
    Limpia los gráficos de la pantalla de inicio.
    """
    if graficos:
        graphics.removeLayer(graficos)
        graficos.clear()
