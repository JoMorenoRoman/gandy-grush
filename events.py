import pygame
import graphics
from typing import Callable

_subscribers:dict[int, set] = {}
_timed:list[tuple[int, Callable]] = []
_collisions:list[tuple[pygame.Rect, Callable]] = []
_running = True

def start():
    global _running, _subscribers, _collisions
    while _running:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if _subscribers.get(event.type):
                for sub in _subscribers[event.type]:
                    sub(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in _collisions:
                    if box[0].collidepoint(pygame.mouse.get_pos()):
                        box[1]()
        # for timeFuncs in timed:
        #     timeFuncs[0] -= 1
        graphics.renderDisplay()
                
def subscribe(subscriber, *args):
    global _subscribers
    for event in args:
        if _subscribers[event]:
            _subscribers[event].add(subscriber)
        else:
            _subscribers.update({event: (subscriber)})
            
def addTimed(framesToWait, func):
    global _timed
    _timed.append((framesToWait, func))
    
def addCollision(rect:pygame.Rect, func):
    global _collisions
    _collisions.append((rect, func))
    
def clearCollisions():
    global _collisions
    _collisions.clear()
    
def reset():
    global _subscribers, _timed, _collisions
    _subscribers = {}
    _timed = []
    _collisions = []
    
def quit():
    global _running
    _running = False
    pygame.event.post(pygame.event.Event(pygame.QUIT))