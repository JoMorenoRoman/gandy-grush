import pygame
import display
from typing import Callable

subscribers:dict[int, set] = {}
timed:list[tuple[int, Callable]] = []
collisions:list[tuple[pygame.Rect, Callable]] = []
running = True

def start():
    while running:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if subscribers.get(event.type):
                for sub in subscribers[event.type]:
                    sub(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in collisions:
                    if box[0].collidepoint(pygame.mouse.get_pos()):
                        box[1]()
        pygame.display.flip()
        # for timeFuncs in timed:
        #     timeFuncs[0] -= 1
                
def subscribe(subscriber, *args):
    for event in args:
        if subscribers[event]:
            subscribers[event].add(subscriber)
        else:
            subscribers.update({event: (subscriber)})
            
def addTimed(framesToWait, func):
    timed.append((framesToWait, func))
    
def addCollision(rect:pygame.Rect, func):
    collisions.append((rect, func))
    
def reset():
    global subscribers, timed, collisions
    subscribers = {}
    timed = []
    collisions = []
    
def quit():
    global running
    running = False
    pygame.event.post(pygame.event.Event(pygame.QUIT))