from typing import Any
import pygame
import eventq
import config
import display
import pantallas.inicio
import pantallas.juego
import graphics

from utils import convertir_csv_a_matriz, leer_archivo_texto

_estado:dict = {}
_layer:list[tuple[pygame.Surface, pygame.Rect]] = []

OPCIONES = "opciones"
TITULO = "titulo"
PAUSADO = "pausado"

def iniciar(options:list[tuple[str, Any]], titulo:str|None = None, paused:bool = False):
    _estado.clear()
    _estado[OPCIONES] = []
    for opt in options:
        _estado[OPCIONES].append(opt)
    if titulo:
        _estado[TITULO] = titulo
    _estado[PAUSADO] = paused
    render()
    graphics.addRenderer(__name__)
    
def render():
    _layer.clear()
    graphics.removeLayer(_layer)
    opciones = _estado[OPCIONES]
    limite = display.combinar_limites(display.construir_limite(0.1, 1, 1), display.construir_limite(0.1, 1, 2))
    temps = []
    items = []
    titulo = None
    if _estado.get(TITULO, None):
        titulo = config.subtitulo.render(_estado[TITULO], True, config.TEXT_COLOR)
        titulo = (titulo, titulo.get_rect()) 
        temps.append(titulo)
    
    for opcion in opciones:
        text = config.texto.render(opcion[0], True, config.TEXT_COLOR)
        tupla = (text, text.get_rect())
        temps.append(tupla)
        items.append(tupla)
        
    temps = display.pad(temps, 0.3)
    display.alinear(temps)
    refs = display.encastrar(temps, limite)
    rect = display.crear_container(refs, 0.1)
    surf = pygame.Surface((rect.w, rect.h))
    surf.fill(config.MENU_BG)
    surf.convert()
    _layer.append((surf, rect))
    graphics.addLayer(_layer)
    
    if titulo:
        _layer.append(refs[0])
    
    for i in range(len(opciones)):
        opcion = opciones[i]
        graf = refs[temps.index(items[i])]
        _layer.append(graf)
        colision = opcion[1]
        if colision:
            if _estado[PAUSADO]:
                eventq.add_paused_collision(graf[1], colision)
            else:
                eventq.addCollision(graf[1], colision)
                

def menu_inicio():
    opciones = [
        ("Inicio", pantallas.juego.iniciar),
        ("Cambiar Resolucion", menu_resoluciones),
        ("Puntajes Mas Altos", puntajes_mas_altos),
        ("Cerrar Juego", eventq.quit),
    ]
    eventq.clearCollisions()
    iniciar(opciones)

def puntajes_mas_altos():
    opciones = []
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz_2 = convertir_csv_a_matriz(datos)
    for row in matriz_2:
        nombre = row[0]
        puntaje = row[1]
        text = f"{nombre}: {puntaje}"
        opciones.append((text, None))
    opciones.append(("volver", menu_inicio))
    eventq.clearCollisions()
    iniciar(opciones)

def menu_resoluciones():
    opciones = [
        ("800x600", lambda: display.set_screen(800, 600)),
        ("1200x800", lambda:display.set_screen(1200, 800)),
        ("1920x1080", lambda: display.set_screen(1920, 1080)),
        ("volver", menu_inicio)
    ]
    eventq.clearCollisions()
    iniciar(opciones)
    
def menu_partida(reiniciar):
    opciones = [
        ("Continuar", cerrar),
        ("Reiniciar", reiniciar),
        ("Abandonar", pantallas.inicio.iniciar)
    ]
    iniciar(opciones, "Pausa", True)
    
def cerrar():
    if _estado[PAUSADO]:
        eventq.clear_paused_collisions()
    _estado.clear()
    graphics.removeLayer(_layer)
    _layer.clear()