import pygame
import random
import display
import eventq
import graphics
import game_objects.tokens as t

# TODO: funcs a snake case
_cardinals = [(-1, 0), (0, 1), (1, 0), (0, -1)]
STATE = "state"
TYPE = "type"
GRAPHIC = "graphic"

def iniciar(matrix:list[list[dict]], rows:int, columns:int):
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            type = chooseType(matrix, x, y)
            token = {
                TYPE: type,
                GRAPHIC: None,
                STATE: t.IDLE
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
    token = getSelected(matrix)
    matchTypes = matches(matrix, x, y)
    if token[TYPE] in matchTypes:
        switch()
        return
    else:
        reject([token, matrix[x][y]])
        map = reset(matrix, t.BUSY)
        # eventq.addTimed(1, )
    return

def switch():
    return

def reject(rejected:list[dict]):
    return

def matches(matrix:list[list[dict]], x:int, y:int):
    matches:set[int] = set()
    for direction in _cardinals:
        match = sonar(matrix, x, y, direction)
        if match:
            matches.add(match)
    return matches
    
def sonar(matrix:list[list[dict]], x:int, y:int, move_vector:tuple[int, int]):
    types: list[int] = []
    for _ in range(2):
        x += move_vector[0]
        y += move_vector[1]
        item = safeIndex(matrix, x, y)
        if item:
            types.append(item[TYPE])
    if len(types) == 2 and types[0] == types[1]:
        return types[0]
    else:
        return None
    
def cardinals(matrix:list[list[dict]], x:int, y:int):
    res:list[dict] = list()
    for direction in _cardinals:
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

def safeIndex(matrix:list[list[dict]], x:int, y:int):
    item = None
    if x < (len(matrix)) and x >= 0:
        row = matrix[x]
        if y <(len(row)) and y >= 0:
            item = row[y]
        
    return item