import pygame
import random
import display
import events
import graphics
import game_objects.tokens as tokens

_cardinals = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def iniciar(rows:int, columns:int):
    matrix:list[list[dict]] = []
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            type = chooseType(matrix, x, y)
            token = {
                "type": type,
                "graphic": None,
                "state": "idle"
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
            color = tokens.rendered[token["type"]]
            token["graphic"] = (color, rect)
            layer.append(token["graphic"])
            events.addCollision(token["graphic"][1], lambda: tokens.pick(matrix, x, y))
    return

def chooseType(matrix:list[list[dict]], x:int, y:int):
    invalids = matches(matrix, x, y)
    while True:
        color = random.randint(0, len(tokens.types) - 1)
        if color not in invalids:
            break
        
    return color

def matches(matrix:list[list[dict]], x:int, y:int):
    global _cardinals
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
            types.append(item["type"])
    if len(types) == 2 and types[0] == types[1]:
        return types[0]
    else:
        return None

def safeIndex(matrix:list[list[dict]], x:int, y:int):
    item = None
    if x < (len(matrix)) and x >= 0:
        row = matrix[x]
        if y <(len(row)) and y >= 0:
            item = row[y]
        
    return item
    