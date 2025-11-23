from pickle import APPEND
from sre_parse import State
import pygame
import random
import animations
import display
import eventq
import graphics
import game_objects.tokens as t

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
MATRIX = "matrix"

def iniciar(matrix:list[list[dict]], rows:int, columns:int):
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            type = chooseType(matrix, x, y)
            token = {
                TYPE: type,
                GRAPHIC: None,
                STATE: t.IDLE,
                BUSY_COUNT: 0,
                POSITION: (x, y),
                MATRIX: matrix
                }
            matrix[x].append(token)
    return matrix

def render(matrix:list[list[dict]], container:pygame.Rect, token_rect:pygame.Rect):
    layer = graphics.addLayer([])
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            token = matrix[x][y]
            rect = token_rect.copy()
            display.matrix_align(rect, x, y, container)
            color = t.rendered[token[TYPE]]
            token[GRAPHIC] = (color, rect)
            layer.append(token[GRAPHIC])
            eventq.addCollision(token[GRAPHIC][1], lambda: select(matrix, x, y))
    return layer

def chooseType(matrix:list[list[dict]], x:int, y:int):
    invalids = matches(matrix, x, y)
    while True:
        color = random.randint(0, len(t.types) - 1)
        if color not in invalids:
            break
        
    return color

def select(matrix:list[list[dict]], x:int, y:int):
    token = matrix[x][y]
    if token[STATE] == t.BUSY:
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
                
def find(matrix:list[list[dict]], func) -> list[dict]:
    res:list[dict] = []
    for row in matrix:
        for item in row:
            if func(item):
                res.append(item)
    return res

def getSelected(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.SELECT:
                return cell
    return {}

def try_switch(matrix:list[list[dict]], x:int, y:int):
    selected = getSelected(matrix)
    matchTypes = matches(matrix, x, y)
    if selected[TYPE] in matchTypes:
        switch(matrix, selected, matrix[x][y])
        scored = score(matrix, x, y)
        destroy_and_replace(scored)
        return
    else:
        reject([selected, matrix[x][y]])
        set_busy(matrix)
        eventq.addTimed(1, lambda: remove_busy(matrix))
    return

def switch(matrix:list[list[dict]], selected:dict, switch:dict):
    animations.switch_tokens(selected[GRAPHIC], switch[GRAPHIC])
    
    matrix[selected[POSITION][0]][selected[POSITION][1]] = switch
    matrix[switch[POSITION][0]][switch[POSITION][1]] = selected
    
    temp = switch[POSITION]
    switch[POSITION] = selected[POSITION]
    selected[POSITION] = temp
    return

def reject(rejected:list[dict]):
    for rej in rejected:
        animations.shake_token(1, rej[GRAPHIC])
    return

def score(matrix:list[list[dict]], x:int, y:int):
    line = matches(matrix, x, y)
    if len(line) != 4:
        make_l(line)
        make_t(line)
    return line

def destroy_and_replace(scored:list[dict]):
    for token in scored:
        animations.destroy_token(token[GRAPHIC])
    return

def make_l(line:list[dict]):
    return

def make_t(line:list[dict]):
    return

def matches(matrix:list[list[dict]], x:int, y:int):
    matching = sonar(matrix, x, y, C_LEFT) + [matrix[x][y]] + sonar(matrix, x, y, C_RIGHT)
    if len(matching) < 3:
        matching = sonar(matrix, x, y, C_DOWN) + [matrix[x][y]] + sonar(matrix, x, y, C_UP)
    return matching
    
def sonar(matrix:list[list[dict]], x:int, y:int, move_vector:tuple[int, int], steps:int|None = 2) -> list[dict]:
    matching: list[dict] = []
    if not steps:
        steps = len(matrix) + len(matrix[0])
    for _ in range(steps):
        x += move_vector[0]
        y += move_vector[1]
        item = safeIndex(matrix, x, y)
        if item and item[TYPE] == matrix[x][y][TYPE]:
            matching.append(item[TYPE])
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
    changes = []
    for row in matrix:
        changes.append([])
        for cell in row:
            if cell[STATE] != t.BUSY:
                cell[STATE] = resetTo
                changes.append(True)
            else:
                changes.append(False)
    return changes

def set_busy(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.BUSY:
                cell[BUSY_COUNT] += 1
            else:
                cell[STATE] = t.BUSY
                
def remove_busy(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[State] == t.BUSY:
                if cell[BUSY_COUNT] == 0:
                    cell[STATE] = t.IDLE
                else:
                    cell[BUSY_COUNT] -= 1
                    

def safeIndex(matrix:list[list[dict]], x:int, y:int):
    item = None
    if x < (len(matrix)) and x >= 0:
        row = matrix[x]
        if y <(len(row)) and y >= 0:
            item = row[y]
        
    return item