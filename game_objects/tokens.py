import images
import pygame

types = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (0, 125, 125) 
]

rendered:list[pygame.Surface] = []

IDLE = "idle"
SELECT = "select"
HIGHLIGHT = "highlight"
SCORE = "score"

def render(size:tuple[int, int]):
    image = images.load_png("token.png", size)
    if len(rendered) > 0:
        rendered.clear()
    for i in range(len(types)):
        color = types[i]
        rendered.append(images.tint_png(image, color))
    