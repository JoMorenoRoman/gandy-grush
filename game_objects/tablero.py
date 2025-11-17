import pygame

def iniciar(container:pygame.Rect):
    weights:list[int] = [0] * 7
    matrix:list[list[dict]] = [[] * 12]
    for row in matrix:
        for col in range(6):
            row.append({})
    return

def render():
    return

def chooseCellColor(matrix:list[list[dict]], weights:list[int], x:int, y:int):
    return
    
def invalidColors(matrix:list[list[dict]], x:int, y:int):
    
    return

def matches(matrix:list[list[dict]], x:int, y:int):
    return
    
def sonar(matrix:list[list[dict]], x:int, y:int, move_x:int, move_y:int):
    for _ in range(2):
        x += move_x
        y += move_y
        item = safeIndex(matrix, x, y)
        if item:
            color = item["color"]

def safeIndex(matrix:list[list[dict]], x:int, y:int):
    item = None
    if x < (len(matrix)) and x >= 0:
        row = matrix[x]
        if y <(len(row)) and y >= 0:
            item = row[y]
        
    return item
    