import images
import pygame

types = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (125, 125, 125) 
]

rendered:list[pygame.Surface] = []

def render(size:tuple[int, int]):
    global rendered, types
    image = images.load_png("token.png", size)
    if len(rendered) == 0:
        rendered = [image] * len(types)
    for i in range(len(types)):
        color = types[i]
        rendered[i] = images.tint_png(image, color)
    
def pick(matrix:list[list[dict]], x:int, y:int):
    token = matrix[x][y]
    token["state"] = "pick"