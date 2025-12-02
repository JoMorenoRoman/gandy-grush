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
    eventq.reset()
    estado[PUNTOS] = puntaje
    estado[CALLBACK] = scoretable.guardar
    estado[GRAFS] = []
    render()
    graphics.addRenderer(render, clear)
    
def clear():
    if estado.get(GRAFS):
        graphics.removeLayer(estado[GRAFS])
        estado[GRAFS].clear()
    estado[TEXT] = ""
    estado[PARAR] = False

def render():
    clear()
    capa:list[tuple[pygame.Surface, pygame.Rect]] = estado[GRAFS]
    graphics.addLayer(capa)
    fondo = display.createGraphic(2/3, 1/4, color=config.BACKGROUND)
    capa.append(fondo)
    titulo = texto.subtitulo("Felicitaciones! Ingrese su nombre:")
    titulo = display.encastrar([titulo], fondo[1].inflate(-20, -20))[0]
    display.alinear_en(titulo, fondo[1], display.PRINCIPIO, 0.10)
    capa.append(titulo)
    text_ref = display.createGraphic(0.01, 0.01)
    text_ref = display.alinear_en(text_ref, fondo[1], display.FINAL, 0.10, display.CENTRO)
    estado[POS] = text_ref[1]
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
        estado[TEXT] += event.text[0:12-len(estado[TEXT])]
    render_text()
        
def render_text():
    text = estado[TEXT]
    text = texto.subtitulo(text)
    display.alinear_en(text, estado[POS], display.FINAL, 0, display.CENTRO)
    if len(estado[GRAFS]) > 2:
       estado[GRAFS][-1] = text
    else:
        estado[GRAFS].append(text)   
        
def terminar():
    scoretable.guardar(estado[TEXT], estado[PUNTOS])
    inicio.iniciar()