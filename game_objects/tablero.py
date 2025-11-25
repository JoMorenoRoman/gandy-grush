from dis import Positions
from sre_parse import State
import pygame
import random
import animations
import display
import eventq
import graphics
import game_objects.tokens as t
import timer

# TODO: funcs a snake case
C_LEFT = (-1, 0)
C_UP = (0, 1)
C_RIGHT = (1, 0)
C_DOWN = (0, -1)
CARDINALS = [C_LEFT, C_UP, C_RIGHT, C_DOWN]

STATE = "state"
TYPE = "type"
GRAPHIC = "graphic"
BUSY_COUNT = "busy_count"
POSITION = "position"

def iniciar(matrix:list[list[dict]], rows:int, columns:int):
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            matrix[x].append({})
            crear_token(matrix, x, y)
    return matrix

def crear_token(matrix:list[list[dict]], x:int, y:int):
    type = chooseType(matrix, x, y)
    token = {
        TYPE: type,
        GRAPHIC: None,
        STATE: t.IDLE,
        BUSY_COUNT: 0,
        POSITION: (x, y)
        }
    matrix[x][y] = token

def render(matrix:list[list[dict]], container:pygame.Rect, token_rect:pygame.Rect):
    layer = graphics.addLayer([], True)
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            primer_render_token(matrix, x, y, layer, container, token_rect)
    return layer
# TODO: estan mal los numeros de las posiciones. x e y como los usamos no estan significando lo que son.
def primer_render_token(matrix:list[list[dict]], x:int, y:int, layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    token = matrix[x][y]
    rect = token_rect.copy()
    display.matrix_align(rect, x, len(matrix) - y - 1, container)
    color = t.rendered[token[TYPE]]
    token[GRAPHIC] = (color, rect)
    pos_y = token[GRAPHIC][1].y
    token[GRAPHIC][1].y -= container.height
    layer.append(token[GRAPHIC])
    eventq.addCollision(token[GRAPHIC][1], lambda: select(matrix, x, y))
    move_token(matrix, token, (token[GRAPHIC][1].x, pos_y))
    
def chooseType(matrix:list[list[dict]], x:int, y:int):
    invalids = set()
    for card in CARDINALS:
        matching = sonar(matrix, x, y, card, 2)
        if len(matching) > 1:
            invalids.add(matching[0][TYPE])
    while True:
        color = random.randint(0, len(t.types) - 1)
        if color not in invalids:
            break
    return color

def select(matrix:list[list[dict]], x:int, y:int):
    token = matrix[x][y]
    if token[STATE] == t.BUSY or token[STATE] == t.SCORE:
        return
    elif token[STATE] == t.HIGHLIGHT:
        try_switch(matrix, x, y)
        return
    elif token[STATE] == t.CANCEL:
        reset(matrix)
    
    token[STATE] = t.SELECT
    for item in cardinals(matrix, x, y):
        if item[STATE] == t.IDLE:
            item[STATE] = t.HIGHLIGHT
    flagIdles(matrix, t.CANCEL)
    
def flagIdles(matrix:list[list[dict]], state:str):
    for row in matrix:
        for item in row:
            if item[STATE] == t.IDLE:
                item[STATE] = state

def getSelected(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.SELECT:
                return cell
    return {}

def try_switch(matrix:list[list[dict]], x:int, y:int):
    selected = getSelected(matrix)
    switch_token = matrix[x][y]
    switch(matrix, selected, switch_token)
    matching = matches(matrix, x, y)
    if len(matching) > 2:
        duration = 0.5
        animations.switch_tokens(selected[GRAPHIC], switch_token[GRAPHIC], duration)
        eventq.addTimed(duration, lambda: buscar_matches(matrix))
    else:
        switch(matrix, selected, switch_token)
        reject([selected, switch_token])
        set_busy(matrix)
        eventq.addTimed(1, lambda: remove_busy(matrix))

def switch(matrix:list[list[dict]], selected:dict, switch:dict):
    temp = selected[POSITION]
    move_to(matrix, selected, switch[POSITION])
    move_to(matrix, switch, temp)

def move_to(matrix:list[list[dict]], token:dict|None, to:tuple[int, int]):
    matrix[to[0]][to[1]] = token # type: ignore
    if token:
        token[POSITION] = to

def reject(rejected:list[dict]):
    for rej in rejected:
        animations.shake_token(rej[GRAPHIC])
    return

def score(matrix:list[list[dict]], x:int, y:int):
    line = matches(matrix, x, y)
    if len(line) != 4:
        make_l(line)
        make_t(line)
    for token in line:
        token[STATE] = t.SCORE
    return line

def destroy(matrix:list[list[dict]], scored:list[dict]):
    for token in scored:
        animations.destroy_token(token[GRAPHIC])
        move_to(matrix, None, token[POSITION])
    return

def fill_empty(matrix:list[list[dict]], layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if not matrix[x][y]:
                replacement = fall_replace(matrix, (x, y))
                if replacement:
                    busy(matrix, replacement[POSITION])
                    animations.move_token(replacement[GRAPHIC], (x, y))
                    move_to(matrix, replacement, (x, y))
                else:
                    crear_token(matrix, x, y)
                    primer_render_token(matrix, x, y, layer, container, token_rect)
    eventq.addTimed(0.5, lambda: buscar_matches(matrix))

def buscar_matches(matrix:list[list[dict]]):
    for x in range(len(matrix)):
        matching = sonar(matrix, x, 0, C_RIGHT)
        if len(matching) > 2:
            break
    if len(matching) < 3:
        for y in range(len(matrix[0])):
            matching = sonar(matrix, 0, y, C_UP)
            if len(matching) > 2:
                break
    if len(matching) > 2:
        pos = matching[0][POSITION]
        scored = score(matrix, pos[0], pos[1])
        destroy(matrix, scored)
                    
def move_token(matrix:list[list[dict]], token:dict, pos:tuple[int, int]):
    busy(matrix, token[POSITION])
    duration = 0.5
    animations.move_token(token[GRAPHIC], pos, duration)
    eventq.addTimed(duration, lambda: debusy(matrix, token[POSITION]))

def fall_replace(matrix:list[list[dict]], xy:tuple) -> dict|None:
    xy = (xy[0], xy[1] + 1)
    if in_bound(matrix, xy):
        replacement = safeIndex(matrix, xy[0], xy[1])
        if replacement and replacement[STATE] != t.SCORE:
            return replacement
        else:
            return fall_replace(matrix, xy)
    else:
        return None

def make_l(line:list[dict]):
    return line

def make_t(line:list[dict]):
    return line

def matches(matrix:list[list[dict]], x:int, y:int):
    matching = sonar(matrix, x, y, C_LEFT) + [matrix[x][y]] + sonar(matrix, x, y, C_RIGHT)
    if len(matching) < 3:
        matching = sonar(matrix, x, y, C_DOWN) + [matrix[x][y]] + sonar(matrix, x, y, C_UP)
    return matching
    
def sonar(matrix:list[list[dict]], x:int, y:int, move_vector:tuple[int, int], steps:int|None = None) -> list[dict]:
    origin = safeIndex(matrix, x, y)
    matching: list[dict] = []
    if not steps:
        steps = len(matrix) + len(matrix[0])
    for _ in range(steps):
        x += move_vector[0]
        y += move_vector[1]
        if not in_bound(matrix, (x, y)):
            break
        item = safeIndex(matrix, x, y)
        if item:
            if origin:
                if origin[TYPE] == item[TYPE]:
                    matching.append(item)
                else:
                    break
            else:
                if len(matching) != 0 and item[TYPE] != matching[0][TYPE]:
                    matching.clear()
                matching.append(item)
        else:
            break
    return matching
    
def cardinals(matrix:list[list[dict]], x:int, y:int):
    res:list[dict] = list()
    for direction in CARDINALS:
        item = safeIndex(matrix, x + direction[0], y + direction[1])
        if item:
            res.append(item)
    return res

def reset(matrix:list[list[dict]], resetTo:str = t.IDLE):
    for row in matrix:
        for cell in row:
            if cell[STATE] != t.BUSY and cell[STATE] != t.SCORE:
                cell[STATE] = resetTo

def set_busy(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            busy(matrix, cell[POSITION])
                
def busy(matrix:list[list[dict]], xy:tuple):
    cell = matrix[xy[0]][xy[1]]
    if cell[STATE] == t.BUSY:
        cell[BUSY_COUNT] += 1
    else:
        cell[STATE] = t.BUSY
        
def debusy(matrix:list[list[dict]], pos:tuple):
    cell = matrix[pos[0]][pos[1]]
    if cell[BUSY_COUNT] > 0:
        cell[BUSY_COUNT] -= 1
    else:
        if cell[STATE] == t.BUSY:
            cell[STATE] = t.IDLE
                
def remove_busy(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.BUSY:
                if cell[BUSY_COUNT] == 0:
                    cell[STATE] = t.IDLE
                else:
                    cell[BUSY_COUNT] -= 1
                    
def in_bound(matrix:list[list[dict]], xy:tuple):
    res = False
    if xy[0] < (len(matrix)) and xy[0] >= 0:
        row = matrix[xy[0]]
        res = xy[1] <(len(row)) and xy[1] >= 0
    return res

def safeIndex(matrix:list[list[dict]], x:int, y:int):
    item = None
    if in_bound(matrix, (x, y)):
        item = matrix[x][y]
    return item