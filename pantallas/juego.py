import display
import graphics
import config
import game_objects.tokens as tokens
import game_objects.tablero as tablero

_tablero:list[list[dict]] = []

def iniciar():
    graphics.clear()
    _tablero.clear()
    tablero.iniciar(_tablero, config.ROWS, config.COLUMNS)
    render()
    graphics.addRenderer(__name__)

def render():
    outer = display.createRect(0, 2/3)
    outer = display.square(outer)
    outer = display.createGraphic(1, 1, outer)
    outer[0].fill(config.MAINCOLOR)
    display.align(outer[1], 1, 1)
    graphics.addLayer([outer])
    
    inner = display.createGraphic(1, 1, outer[1].inflate(-10, -10))
    inner[0].fill(config.BACKGROUND)
    display.align(inner[1], 1, 1)
    graphics.addLayer([inner])
    
    token_rect = display.createRect(1/config.ROWS, 1/config.COLUMNS, inner[1])
    tokens.render(token_rect.size)
    tablero.render(_tablero, inner[1], token_rect)
    