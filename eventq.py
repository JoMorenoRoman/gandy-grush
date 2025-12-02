import pygame
import animations
import config
import graphics
import timer
from typing import Any

_subscribers:dict[int, list] = {}
_timed:list[dict[str, Any]] = []
_collisions:list[tuple[pygame.Rect, Any]] = []
_pausedCollisions: list[tuple[pygame.Rect, Any]] = []
_flags:set = set()

IGNORE_MOUSE = "no_mouse"
def start():
    while True:
        pygame.time.Clock().tick(config.framerate)
        for event in pygame.event.get():
            paused = len(_pausedCollisions) > 0
            if _subscribers.get(event.type, None) and not paused:
                for sub in _subscribers[event.type]:
                    sub(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and IGNORE_MOUSE not in _flags:
                if paused:
                    collisions = _pausedCollisions
                else:
                    collisions = _collisions
                for (box, func) in collisions.copy():
                    if box.collidepoint(pygame.mouse.get_pos()):
                        _flags.add(IGNORE_MOUSE)
                        addTimed(0.3, lambda: quitar_bandera(IGNORE_MOUSE), False)
                        func()
            elif event.type == pygame.QUIT:
                return
            
        removes = []
        for timeFunc in _timed:
            if timeFunc["pause"] and paused:
                continue
            else:
                timeFunc["frames"] -= 1
                if timeFunc["frames"] <= 0:
                    timeFunc["callback"]()
                    repeat = timeFunc.get("repeat")
                    if repeat:
                        timeFunc["frames"] = repeat
                    else:
                        removes.append(timeFunc)
        for remove in removes:
            _timed.remove(remove)
                
        animations.ejecutar()
        graphics.renderizar()
        
def quitar_bandera(flag:str):
    _flags.discard(flag)
       
def subscribe(subscriber, *eventos:int):
    for event in eventos:
        if _subscribers.get(event, None):
            _subscribers[event].append(subscriber)
        else:
            _subscribers[event] = [subscriber]
            
def addTimed(seconds:float, callback, shouldPause:bool = True) -> None:
    _timed.append({"frames": timer.seconds(seconds), "callback": callback, "pause": shouldPause})
    
def add_frame_func(callback, shouldPause:bool = True, frames:int = 1, repeat:int = 1):
    func = {"frames": frames, "callback": callback, "pause": shouldPause, "repeat": repeat}
    _timed.append(func)
    return func

def quitar_frame_func(func:dict):
    if func in _timed:
        _timed.remove(func)
    
def addCollision(rect:pygame.Rect, func):
    colision = (rect, func)
    _collisions.append(colision)
    return colision
    
def clearCollisions():
    _collisions.clear()
    
def quitar_colision(colision:tuple[pygame.Rect, Any]):
    if colision in _collisions:
        _collisions.remove(colision)
    elif colision in _pausedCollisions:
        _pausedCollisions.remove(colision)
    
def add_paused_collision(rect:pygame.Rect, func):
    colision = (rect, func)
    _pausedCollisions.append(colision)
    return colision
    
def clear_paused_collisions():
    _pausedCollisions.clear()
    
def reset():
    _subscribers.clear()
    _timed.clear()
    _collisions.clear()
    _pausedCollisions.clear()
    _flags.clear()
    
def full_reset():
    reset()
    graphics.reset()
    animations.reset()

def postear(evento:int, data:dict|None = None):
    if data:
        pygame.event.post(pygame.event.Event(evento, data))
    else:
        pygame.event.post(pygame.event.Event(evento))

def quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))