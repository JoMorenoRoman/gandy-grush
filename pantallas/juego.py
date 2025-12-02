import time
import pygame
import animations
import display as d
import eventq
from game_objects import boton_pausa, reloj, scoretable
import graphics
import config
import game_objects.tokens as tokens
import game_objects.tablero as tablero
from pantallas import nuevo_record
import pantallas.inicio
import timer
import sonido

_tablero:dict = {}
_funcs:list[dict] = []
_capas:list[list[tuple[pygame.Surface, pygame.Rect]]] = []
CAPA = "capa"


def iniciar():
    """Inicia la pantalla de juego.
    Args:
        None
    """
    sonido.reproducir_musica(sonido.MUSICA_PARTIDA)
    eventq.full_reset()
    _tablero.clear()
    iniciar_tablero(True, False)
    graphics.addRenderer("juego", render, clear)
    reloj.iniciar(config.TIEMPO, fin_partida)
    scoretable.iniciar()
    boton_pausa.iniciar()
    render()
    

def fin_partida():
    """Gestiona la logica al finalizar la partida.
    Args:
        None
    """
    if scoretable.tiene_puntaje():
        scoretable.agregar_puntaje_historico()
    else:
        pantallas.inicio.iniciar()
    

def iniciar_tablero(reset_fuerte:bool, imposible:bool):
    """Inicializa valores y estructuras del tablero.
    Args:
        reset_fuerte (bool): Si reinicia puntaje.
        imposible (bool): Si crea un tablero sin jugadas posibles.
    """
    if _tablero.get(CAPA):
        graphics.removeLayer(_tablero[CAPA])
    if reset_fuerte:
        _tablero[tablero.PUNTAJE] = 0
    _tablero[tablero.MATRIX] = []
    _tablero[tablero.BUSY] = False
    _tablero[tablero.ANIM_SPEED] = 0.5
    _tablero[tablero.ULTIMO_CLICK] = time.time()
    _tablero[tablero.SUPER_LIMITE] = config.SUPER_THRESHOLD
    _tablero[CAPA] = []
    tablero.iniciar(_tablero[tablero.MATRIX], config.ROWS, config.COLUMNS, imposible)
    

def clear():
    """Limpia todas las capas y el tablero.
    Args:
        None
    """
    if _capas:
        for capa in _capas:
            graphics.removeLayer(capa)
    clear_tablero()
    

def clear_tablero(quitar_grafico:bool = True):
    """Limpia colisiones, graficos y funciones registradas del tablero.
    Args:
        quitar_grafico (bool): Si remueve la capa grafica del tablero.
    """
    if quitar_grafico and _tablero.get(CAPA):
        graphics.removeLayer(_tablero[CAPA])
        _tablero[CAPA] = []
    if _funcs:
        for func in _funcs:
            eventq.quitar_frame_func(func)
    _funcs.clear()
    if _tablero.get(tablero.MATRIX):
        for row in _tablero[tablero.MATRIX]:
            for cell in row:
                if cell:
                    eventq.quitar_colision(cell[tablero.COLISION])
    

def render():
    """Renderiza los elementos principales del juego.
    Args:
        None
    """
    clear()
    outer = d.createGraphic(1, 1, d.square(d.createRect(0, 2/3)))
    d.align(outer[1], 1, 1)
    outer[0].fill(config.MAINCOLOR)
    _capas.append(graphics.addLayer([outer]))
    
    inner = outer[1].inflate(-10, -10).copy()
    d.make_multiple(inner, config.COLUMNS, config.ROWS)
    inner = d.createGraphic(ref=inner)
    inner[0].fill(config.BACKGROUND)
    d.align(inner[1], 1, 1)
    _capas.append(graphics.addLayer([inner]))
    
    render_tablero()
    scoretable.render(outer[1])
    reloj.render(outer[1])


def render_tablero():
    """Renderiza el tablero de juego y registra funciones de actualizacion.
    Args:
        None
    """
    clear_tablero()
    inner = _capas[1][0]
    token_rect = d.createRect(1/config.ROWS, 1/config.COLUMNS, inner[1])
    tokens.render(token_rect.size)
    tablero.render(_tablero, inner[1], token_rect)
    
    _funcs.append(eventq.add_frame_func(lambda: scoretable.cambiarPuntaje(_tablero[tablero.PUNTAJE]), False, 15, 15))
    matchear = lambda: tablero.buscar_matches(_tablero)
    limpiar = lambda: tablero.fill_empty(_tablero, _tablero["capa"], inner[1], token_rect)
    _funcs.append(eventq.add_frame_func(lambda: encadenar(matchear, limpiar)))
    duracion = timer.seconds(0.35)
    _funcs.append(eventq.add_frame_func(lambda: titilar(_tablero[tablero.MATRIX], 0.35), True, duracion, duracion))
    _funcs.append(eventq.add_frame_func(encontrar_jugada, True, timer.seconds(1), timer.seconds(0.25)))


def encadenar(*funcs):
    """Ejecuta funciones encadenadas.
    Args:
        *funcs (callable): Funciones a ejecutar.
    """
    for func in funcs:
        func()


def encontrar_jugada():
    """Detecta jugadas posibles y destaca o resetea el tablero segun sea necesario.
    Args:
        None
    """
    jugada = tablero.buscar_jugada(_tablero)
    if jugada:
        if len(jugada) > 2:
            ult_click =  time.time() - _tablero[tablero.ULTIMO_CLICK]
            if ult_click > 5:
                for token in jugada:
                    token[tablero.STATE] = tokens.HIGHLIGHT
        else:
            reiniciar_tablero()
            

def reiniciar_tablero():
    """Reinicia el tablero si no quedan jugadas posibles.
    Args:
        None
    """
    clear_tablero(False)
    animations.opacar(_capas[1][0][1])
    tablero.set_as_busy(_tablero, 1)
    iniciar_tablero(False, False)
    eventq.addTimed(0.5, lambda: encadenar(lambda: iniciar_tablero(False, False), render_tablero), False)


def titilar(matrix:list[list[dict]], duracion:float):
    """Aplica efecto de titilado a tokens destacados.
    Args:
        matrix (list[list[dict]]): Matriz de tokens.
        duracion (float): Duracion del efecto.
    """
    for row in matrix:
        for token in row:
            if token and token[tablero.STATE] == tokens.HIGHLIGHT:
                animations.titilar(token[tablero.GRAPHIC], duracion, 240)
