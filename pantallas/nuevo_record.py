
import pygame
import config
import display
import eventq
from game_objects import scoretable
import graphics
from pantallas import inicio
import texto

estado:dict = {}
GRAFS = "grafs"
TEXT = "text"
POS = "pos"
PARAR = "parar"
PUNTOS = "puntos"
CALLBACK = "callback"

def iniciar(puntaje:int):
    eventq.full_reset()
    estado[PUNTOS] = puntaje
    estado[CALLBACK] = scoretable.guardar
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
    titulo = texto.titulo("Felicitaciones! Ingrese su nombre:")
    display.centrar_entre(titulo[1], (screen.centerx, screen.top), (text_ref.x, text_ref.y))
    estado[GRAFS].append(titulo)
    eventq.subscribe(borrar, pygame.KEYDOWN)
    eventq.subscribe(escribir, pygame.TEXTINPUT)

def borrar(event):
    if event.key == pygame.K_BACKSPACE:
        estado[TEXT] = estado[TEXT][:-1]
    elif event.key == pygame.K_RETURN:
        terminar()
    render_text()

def escribir(event):
    if len(estado[TEXT]) < 12:
        estado[TEXT] += event.text
    render_text()
        
def render_text():
    text = estado[TEXT]
    text = texto.subtitulo(text)
    text[1].centerx = estado[POS].centerx
    text[1].centery = estado[POS].centery
    if len(estado[GRAFS]) > 2:
       estado[GRAFS][-1] = text
    else:
        estado[GRAFS].append(text)   
        
def terminar():
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