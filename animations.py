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
        if anim[FRAME] >= anim[DURATION]:
            removes.append(anim)
            continue
        else:
            anim[CALLBACK]()
            anim[FRAME] += 1
    for remove in removes:
        animations.remove(remove)
    return

ROUND = "round"
DEST = "dest"
ORIGIN = "origin"
def shake_token(token:tuple[pygame.Surface, pygame.Rect], state:dict|None = None):
    if not state:
        state = {
            DURATION: timer.seconds(1) / 3,
            FRAME: 1,
            ROUND: 1,
            ORIGIN: token[1].x
        }
        state[CALLBACK] = lambda: shake_token(token, state)
        animations.append(state)
    
    if not state.get(DEST):
        match state[ROUND]:
            case 1:
                state[DEST] = (state[ORIGIN] - (token[1].w) / 3, token[1].y)
            case 2:
                state[DEST] = (state[ORIGIN] + (token[1].w) / 3, token[1].y)
            case 3:
                state[DEST] = (state[ORIGIN], token[1].y)
                
    move_token(token, state[DEST], state=state)
    
    if state[FRAME] == (state[DURATION] - 1) and state[ROUND] != 3:
        state[DEST] = None
        state[FRAME] = 1
        state[ROUND] += 1
    return

def switch_tokens(token1:tuple[pygame.Surface, pygame.Rect], token2:tuple[pygame.Surface, pygame.Rect]):
    dest1 = (token2[1].x, token2[1].y)
    dest2 = (token1[1].x, token1[1].y)
    move_token(token1, dest1)
    move_token(token2, dest2)
    return

def move_token(token:tuple[pygame.Surface, pygame.Rect], dest:tuple[int, int], duration:float = 0.5, state:dict|None = None):
    if not state:
        state = {
            DURATION: timer.seconds(duration), 
            FRAME: 1
            }
        state[CALLBACK] = lambda: move_token(token, dest, state=state)
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
            DURATION: timer.seconds(0.5),
            FRAME: 1
            }
        state[CALLBACK] = lambda: destroy_token(token, state)
        animations.append(state)
    
    if state.get(CURRENT):
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