import pygame
import graphics
from typing import Any, Callable

_subscribers:dict[int, set] = {}
_timed:list[dict[str, Any]] = []
_collisions:list[tuple[pygame.Rect, Callable]] = []

_paused = False
_pausedCollisions: list[tuple[pygame.Rect, Callable]] = []

def start():
    global _paused, _subscribers, _collisions, _timed
    while True:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if _subscribers.get(event.type) and not _paused:
                for sub in _subscribers[event.type]:
                    sub(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global _collisions, _pausedCollisions
                if _paused:
                    collisions = _pausedCollisions
                else:
                    collisions = _collisions
                    
                for box in collisions:
                    if box[0].collidepoint(pygame.mouse.get_pos()):
                        box[1]()
            elif event.type == pygame.QUIT:
                break
            
        for timeFunc in _timed:
            if timeFunc["pause"] and _paused:
                continue
            else:
                timeFunc["frames"] -= 1
                if timeFunc["frames"] == 0:
                    timeFunc["callback"]()
        graphics.renderDisplay()
                
def subscribe(subscriber, *args):
    global _subscribers
    for event in args:
        if _subscribers[event]:
            _subscribers[event].add(subscriber)
        else:
            _subscribers.update({event: (subscriber)})
            
def addTimed(framesToWait:int, callback, shouldPause:bool = True) -> None:
    global _timed
    _timed.append({"frames": framesToWait, "callback": callback, "pause": shouldPause})
    
def addCollision(rect:pygame.Rect, func):
    global _collisions
    _collisions.append((rect, func))
    
def clearCollisions():
    global _collisions
    _collisions.clear()
    
def reset():
    global _subscribers, _timed, _collisions, _pausedCollisions
    _subscribers = {}
    _timed = []
    _collisions = []
    _pausedCollisions = []
    
def quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))