from game_objects.scoretable import agregar_puntaje_historico, limpiar_puntaje
import pygame
import animations
import config
import graphics
import timer
from typing import Any

_subscribers:dict[int, set] = {}
_timed:list[dict[str, Any]] = []
_collisions:list[tuple[pygame.Rect, Any]] = []

paused = False
_pausedCollisions: list[tuple[pygame.Rect, Any]] = []

def start():
    while True:
        pygame.time.Clock().tick(config.framerate)
        for event in pygame.event.get():
            if _subscribers.get(event.type) and not paused:
                for sub in _subscribers[event.type]:
                    sub(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    collisions = _pausedCollisions
                else:
                    collisions = _collisions
                # TODO: don't call mouse pos 1000 times
                for box in collisions:
                    if box[0].collidepoint(pygame.mouse.get_pos()):
                        box[1]()
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
                
        animations.run_animations()
        graphics.renderDisplay()
        
                
def subscribe(subscriber, *args):
    for event in args:
        if _subscribers[event]:
            _subscribers[event].add(subscriber)
        else:
            _subscribers.update({event: (subscriber)})
            
def addTimed(seconds:float, callback, shouldPause:bool = True) -> None:
    _timed.append({"frames": timer.seconds(seconds), "callback": callback, "pause": shouldPause})
    
def add_frame_func(callback, shouldPause:bool = True):
    func = {"frames": 1, "callback": callback, "pause": shouldPause, "repeat": 1}
    _timed.append(func)
    return func
    
def quitar_frame_func(func:dict):
    if func in _timed:
        _timed.remove(func)
    
def addCollision(rect:pygame.Rect, func):
    _collisions.append((rect, func))
    
def clearCollisions():
    _collisions.clear()
    
def reset():
    _subscribers.clear()
    _timed.clear()
    _collisions.clear()
    _pausedCollisions.clear()
    
def quit():
    agregar_puntaje_historico()
    limpiar_puntaje()
    pygame.event.post(pygame.event.Event(pygame.QUIT))