import display
import eventq
from game_objects import boton_pausa, reloj
import graphics
import config
import game_objects.tokens as tokens
import game_objects.tablero as tablero
import pantallas.nuevo_record

_tablero:dict = {}
_funcs:list[dict] = []

def iniciar():
    #eventq.full_reset()
    _tablero.clear()
    _tablero[tablero.MATRIX] = []
    _tablero[tablero.BUSY] = False
    _tablero[tablero.ANIM_SPEED] = 0.5
    _tablero[tablero.PUNTAJE] = 0
    tablero.iniciar(_tablero[tablero.MATRIX], config.ROWS, config.COLUMNS)

    graphics.addRenderer(__name__)
    render()
    reloj.iniciar(90, lambda: pantallas.nuevo_record.iniciar(_tablero[tablero.PUNTAJE]))
    boton_pausa.iniciar(iniciar)

def render():
    _funcs.clear()
    outer = display.createRect(0, 2/3)
    outer = display.square(outer)
    outer = display.createGraphic(1, 1, outer)
    outer[0].fill(config.MAINCOLOR)
    display.align(outer[1], 1, 1)
    graphics.addLayer([outer])
    
    inner = display.createRect(1, 1, outer[1].inflate(-10, -10))
    display.make_multiple(inner, config.COLUMNS, config.ROWS)
    inner = display.createGraphic(1, 1, inner)
    inner[0].fill(config.BACKGROUND)
    display.align(inner[1], 1, 1)
    graphics.addLayer([inner])
    
    token_rect = display.createRect(1/config.ROWS, 1/config.COLUMNS, inner[1])
    tokens.render(token_rect.size)
    capa_tablero = tablero.render(_tablero, inner[1], token_rect)
    _funcs.append(eventq.add_frame_func(lambda: tablero.buscar_matches(_tablero)))
    _funcs.append(eventq.add_frame_func(lambda: tablero.fill_empty(_tablero, capa_tablero, inner[1], token_rect)))