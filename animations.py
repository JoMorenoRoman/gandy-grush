import pygame
import graphics
import timer

animations:list[dict] = []
CALLBACK = "callback"
FRAME = "frame"
DURATION = "duration"

def run_animations():
    removes = []
    for anim in animations:
        if anim[FRAME] == anim[DURATION]:
            removes.append(anim)
            continue
        else:
            anim[CALLBACK]()
            anim[FRAME] += 1
    for remove in removes:
        animations.remove(remove)
    return

def shake_token(seconds:float, graphic:tuple[pygame.Surface, pygame.Rect]):
    duration = timer.seconds(1)
    
    return

def switch_tokens(token1:tuple[pygame.Surface, pygame.Rect], token2:tuple[pygame.Surface, pygame.Rect]):
    dest1 = (token2[1].x, token2[1].y)
    dest2 = (token1[1].x, token1[1].y)
    move_token(token1, dest1)
    move_token(token2, dest2)
    return

def move_token(token:tuple[pygame.Surface, pygame.Rect], dest:tuple[int, int], state:dict|None = None):
    if not state:
        state = {
            CALLBACK: lambda: move_token(token, dest, state),
            DURATION: timer.seconds(0.5), 
            FRAME: 1
            }
        animations.append(state)
    remaining = state[DURATION] - state[FRAME]
    token[1].x = animate(token[1].x, dest[0], remaining)
    token[1].y = animate(token[1].y, dest[1], remaining)
    return
    
CURRENT = "current"
def destroy_token(token:tuple[pygame.Surface, pygame.Rect], state:dict|None = None):
    if not state:
        graphics.removeGraphic(token)
        state = {
            CALLBACK: lambda: destroy_token(token, state),
            DURATION: timer.seconds(0.5),
            FRAME: 1
            }
        animations.append(state)
    
    if state[CURRENT]:
        current = state[CURRENT]
    else:
        current = 0
    
    remaining = state[DURATION] - state[FRAME]
    rotation = animate(current, 360, remaining)
    surf = pygame.transform.rotate(token[0], rotation)
    size = surf.get_size()
    size = (animate(size[0], 0, remaining), animate(size[1], 0, remaining))
    surf = pygame.transform.smoothscale(surf, size)
    graphics.add_temp((surf, token[1]))
    state[CURRENT] = rotation
    return

def animate(origin:int, dest:int, interval:int):
    return origin + round((dest - origin) / interval)

def animate_f(origin:float, dest:float, interval:int, precision:int) -> float:
    result = animate(origin * (10**precision), dest * (10**precision), interval)
    return result / (10**precision)