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
POSITION = "position"
MATRIX = "matrix"
BUSY = "busy"
ANIM_SPEED = "animation_speed"

def iniciar(matrix:list[list[dict]], rows:int, columns:int):
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            matrix[x].append({})
            crear_token(matrix, x, y)
    return matrix

def crear_token(matrix:list[list[dict]], x:int, y:int):
    type = choose_type(matrix, x, y)
    token = {
        TYPE: type,
        GRAPHIC: None,
        STATE: t.IDLE,
        POSITION: (x, y)
        }
    matrix[x][y] = token
    
def choose_type(matrix:list[list[dict]], x:int, y:int):
    invalids = match_types(matrix, x, y)
    while True:
        color = random.randint(0, len(t.types) - 1)
        if color not in invalids:
            break
    return color

def match_types(matrix:list[list[dict]], x:int, y:int):
    types = set()
    for direction in [(1, 0),(0, 1)]:
        for pairs in [[-2, -1], [-1, 1], [1, 2]]:
            compare = None
            for distance in pairs:
                item = safe_index(matrix, x + (direction[0] * distance), y + (direction[1] * distance))
                if not item:
                    continue
                if compare and compare[TYPE] == item[TYPE]:
                    types.add(item[TYPE])
                else:
                    compare = item
    return types
        
def render(tablero:dict, container:pygame.Rect, token_rect:pygame.Rect):
    matrix = tablero[MATRIX]
    layer = graphics.addLayer([], True)
    set_as_busy(tablero, tablero[ANIM_SPEED])
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            primer_render_token(tablero, x, y, layer, container, token_rect)
    return layer

def set_as_busy(tablero:dict, duration:float):
    set_state(tablero, True)
    eventq.addTimed(duration, lambda: set_state(tablero, False))

def set_state(tablero:dict, state:bool):
    tablero[BUSY] = state

def primer_render_token(tablero:dict, x:int, y:int, layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    matrix = tablero[MATRIX]
    token = matrix[x][y]
    rect = token_rect.copy()
    display.matrix_align(matrix, rect, x, y, container)
    color = t.rendered[token[TYPE]]
    token[GRAPHIC] = (color, rect)
    pos_y = token[GRAPHIC][1].y
    token[GRAPHIC][1].y -= container.height
    layer.append(token[GRAPHIC])
    eventq.addCollision(token[GRAPHIC][1], lambda: select(tablero, x, y))
    animations.move_token(token[GRAPHIC], (token[GRAPHIC][1].x, pos_y), tablero[ANIM_SPEED])

def select(tablero:dict, x:int, y:int):
    if tablero[BUSY]:
        return
    matrix = tablero[MATRIX]
    token = matrix[x][y]
    if token[STATE] == t.SCORE:
        return
    elif token[STATE] == t.HIGHLIGHT:
        try_switch(tablero, x, y)
        return
    elif token[STATE] == t.CANCEL:
        reset(matrix)
    
    token[STATE] = t.SELECT
    for item in cardinals(matrix, x, y):
        if item[STATE] == t.IDLE:
            item[STATE] = t.HIGHLIGHT
    flag_idles(matrix, t.CANCEL)
    
def flag_idles(matrix:list[list[dict]], state:str):
    for row in matrix:
        for item in row:
            if item[STATE] == t.IDLE:
                item[STATE] = state

def get_selected(matrix:list[list[dict]]):
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.SELECT:
                return cell
    return {}

def try_switch(tablero:dict, x:int, y:int):
    matrix = tablero[MATRIX]
    selected = get_selected(matrix)
    switch_token = matrix[x][y]
    switch(matrix, selected, switch_token)
    matching = matches(matrix, x, y)
    if len(matching) > 2:
        set_as_busy(tablero, tablero[ANIM_SPEED])
        animations.switch_tokens(selected[GRAPHIC], switch_token[GRAPHIC], tablero[ANIM_SPEED])
    else:
        set_as_busy(tablero, 1)
        switch(matrix, selected, switch_token)
        for rejected in [selected, switch_token]:
            animations.shake_token(rejected[GRAPHIC])
            
def matches(matrix:list[list[dict]], x:int, y:int):
    matching = sonar(matrix, x, y, C_LEFT) + [matrix[x][y]] + sonar(matrix, x, y, C_RIGHT)
    if len(matching) < 3:
        matching = sonar(matrix, x, y, C_DOWN) + [matrix[x][y]] + sonar(matrix, x, y, C_UP)
    return matching

def switch(matrix:list[list[dict]], selected:dict, switch:dict):
    temp = selected[POSITION]
    move_to(matrix, selected, switch[POSITION])
    move_to(matrix, switch, temp)

def move_to(matrix:list[list[dict]], token:dict|None, to:tuple[int, int]):
    matrix[to[0]][to[1]] = token # type: ignore
    if token:
        token[POSITION] = to

def score(matrix:list[list[dict]], line:list[dict]):
    if len(line) != 4:
        make_l(matrix, line)
        make_t(matrix, line)
    for token in line:
        token[STATE] = t.SCORE
    return line

def destroy(tablero:dict, scored:list[dict]):
    set_as_busy(tablero, 0.5)
    for token in scored:
        animations.destroy_token(token[GRAPHIC])
        move_to(tablero[MATRIX], None, token[POSITION])
    return

def fill_empty(tablero:dict, layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    if tablero[BUSY]:
        return
    matrix:list[list[dict]] = tablero[MATRIX]
    changes = False
    for y in range(len(matrix[0])):
        for x in range(len(matrix)):
            if not matrix[x][y]:
                changes = True
                replacement = fall_replace(matrix, x, y)
                if replacement:
                    duration = 0.5
                    dest = token_rect.copy()
                    display.matrix_align(matrix, dest, x, y, container)
                    animations.move_token(replacement[GRAPHIC], (dest.x, dest.y), duration)
                    moved_from = replacement[POSITION]
                    move_to(matrix, replacement, (x, y))
                    move_to(matrix, None, moved_from)
                else:
                    crear_token(matrix, x, y)
                    primer_render_token(tablero, x, y, layer, container, token_rect)
    if changes:
        set_as_busy(tablero, tablero[ANIM_SPEED])
    
def fall_replace(matrix:list[list[dict]], x:int, y:int) -> dict|None:
    y += 1
    if in_bound(matrix, (x, y)):
        replacement = safe_index(matrix, x, y)
        if replacement and replacement[STATE] != t.SCORE:
            return replacement
        else:
            return fall_replace(matrix, x, y)
    else:
        return None    

def buscar_matches(tablero:dict):
    if tablero[BUSY]:
        return
    matrix:list[list[dict]] = tablero[MATRIX]
    for x in range(len(matrix)):
        matching = find_matching(matrix, x, 0, C_UP)
        if len(matching) > 2:
            break
    if len(matching) < 3:
        for y in range(len(matrix[0])):
            matching = find_matching(matrix, 0, y, C_RIGHT)
            if len(matching) > 2:
                break
            
    if len(matching) > 2:
        scored = score(matrix, matching)
        destroy(tablero, scored)

def make_l(matrix:list[list[dict]], line:list[dict]):
    return line

def make_t(matrix:list[list[dict]], line:list[dict]):
    return line
    
def sonar(matrix:list[list[dict]], x:int, y:int, move:tuple[int, int]) -> list[dict]:
    origin = safe_index(matrix, x, y)
    matching: list[dict] = []
    for _ in range(2):
        x += move[0]
        y += move[1]
        if not in_bound(matrix, (x, y)):
            break
        else:
            token = safe_index(matrix, x, y)
            if not token:
                break
            if origin:
                if token[TYPE] == origin[TYPE]:
                    matching.append(token)
                else:
                    break
            else:
                if len(matching) == 0 or token[TYPE] == matching[0][TYPE]:
                    matching.append(token)
                else:
                    break
    return matching

def find_matching(matrix:list[list[dict]], x:int, y:int, move:tuple[int, int]):
    matching:list[dict] = []
    while in_bound(matrix, (x, y)):
        token = safe_index(matrix, x, y)
        if not token:
            break
        if len(matching) == 0:
            matching.append(token)
        else:
            if matching[0][TYPE] == token[TYPE]:
                matching.append(token)
            else:
                if len(matching) > 2:
                    break
                else:
                    matching.clear()
                    matching.append(token)
        x += move[0]
        y += move[1]
    return matching
        
def cardinals(matrix:list[list[dict]], x:int, y:int):
    res:list[dict] = list()
    for direction in CARDINALS:
        item = safe_index(matrix, x + direction[0], y + direction[1])
        if item:
            res.append(item)
    return res

def reset(matrix:list[list[dict]], resetTo:str = t.IDLE):
    for row in matrix:
        for cell in row:
            if cell[STATE] != t.SCORE:
                cell[STATE] = resetTo
                    
def in_bound(matrix:list[list[dict]], xy:tuple):
    res = False
    if xy[0] < (len(matrix)) and xy[0] >= 0:
        row = matrix[xy[0]]
        res = xy[1] <(len(row)) and xy[1] >= 0
    return res

def safe_index(matrix:list[list[dict]], x:int, y:int):
    item = None
    if in_bound(matrix, (x, y)):
        item = matrix[x][y]
    return item