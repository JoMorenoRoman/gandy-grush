
from operator import call
import pygame

from animations import CALLBACK
import config
import display
import eventq
import graphics
from pantallas import inicio

estado:dict = {}
GRAFS = "grafs"
TEXT = "text"
POS = "pos"
PARAR = "parar"
PUNTOS = "puntos"
CALLBACK = "callback"

def iniciar(puntaje:int, callback):
    estado[PUNTOS] = puntaje
    estado[CALLBACK] = callback
    render()
    graphics.addRenderer(render, clear)

def render():
    clear()
    graphics.addLayer(estado[GRAFS])
    screen = config.screen.get_rect()
    background = pygame.Surface(config.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    estado[GRAFS].append((background, background.get_rect()))
    text_ref = pygame.Rect(screen.centerx, screen.centery, 10, 10)
    estado[POS] = text_ref
    titulo = config.subtitulo.render("Felicitaciones! Ingrese su nombre:", True, config.TEXT_COLOR)
    titulo = (titulo, titulo.get_rect())
    display.centrar_entre(titulo[1], (screen.centerx, screen.top), (text_ref.x, text_ref.y))
    estado[GRAFS].append(titulo)
    eventq.subscribe(borrar, pygame.KEYDOWN)
    eventq.subscribe(escribir, pygame.TEXTINPUT)

def borrar(event):
    if event.key == pygame.K_BACKSPACE:
        estado[TEXT] = estado[TEXT][:-1]
    elif event.key == pygame.K_RETURN:
        estado[PARAR] = True
        terminar()
    render_text()

def escribir(event):
    if len(estado[TEXT]) < 12:
        estado[TEXT] += event.text
    render_text()
        
def render_text():
    text = estado[TEXT]
    text = config.texto.render(text, True, config.TEXT_COLOR)
    text = (text, text.get_rect())
    text[1].centerx = estado[POS].centerx
    text[1].centery = estado[POS].centery
    if len(estado[GRAFS]) > 2:
       estado[GRAFS][-1] = text
    else:
        estado[GRAFS].append(text)   
        
def terminar():
    if estado[PARAR]:
        estado[CALLBACK](estado[TEXT], estado[PUNTOS])
        inicio.iniciar()
    

def clear():
    grafs:list|None = estado.get(GRAFS, None)
    if grafs:
        graphics.removeLayer(grafs)
        grafs.clear()
    estado[GRAFS] = []
    estado[TEXT] = ""
    estado[PARAR] = False