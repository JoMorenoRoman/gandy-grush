
import pygame
import animations
import config
import graphics
import timer
from typing import Any

_subscribers: dict[int, list] = {}
_timed: list[dict[str, Any]] = []
_collisions: list[tuple[pygame.Rect, Any]] = []
_pausedCollisions: list[tuple[pygame.Rect, Any]] = []
_flags: set = set()

IGNORE_MOUSE = "no_mouse"

def start():
    """
    Inicia el bucle principal de eventos del juego.

        - Procesa eventos de Pygame.
        - Ejecuta funciones que apuntan a eventos.
        - Maneja colisiones y clics del mouse.
        - Actualiza animaciones y renderizado.
    """
    while True:
        pygame.time.Clock().tick(config.framerate)
        for event in pygame.event.get():
            paused = len(_pausedCollisions) > 0
            if _subscribers.get(event.type, None) and not paused:
                for sub in _subscribers[event.type]:
                    sub(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and IGNORE_MOUSE not in _flags:
                collisions = _pausedCollisions if paused else _collisions
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


def quitar_bandera(flag: str):
    """
    Elimina una bandera del conjunto de control.

    Args:
        flag: Nombre de la bandera.
    """
    _flags.discard(flag)


def subscribe(subscriber, *eventos: int):
    """
    Suscribe (apunta) una función a uno o más eventos de Pygame.

    Args:
        subscriber: Función que manejará el evento.
        eventos: Tipos de eventos.
    """
    for event in eventos:
        if _subscribers.get(event, None):
            _subscribers[event].append(subscriber)
        else:
            _subscribers[event] = [subscriber]


def addTimed(seconds: float, callback, shouldPause: bool = True) -> None:
    """
    Agrega una función temporizada que se ejecutará después de cierto tiempo.

    Args:
        seconds: Tiempo en segundos.
        callback: Función a ejecutar.
        shouldPause: Si debe pausarse cuando hay colisiones pausadas.
    """
    _timed.append({"frames": timer.seconds(seconds), "callback": callback, "pause": shouldPause})


def add_frame_func(callback, shouldPause: bool = True, frames: int = 1, repeat: int = 1):
    """
    Agrega una función que se ejecutará después de un número específico de frames.

    Args:
        callback: Función a ejecutar.
        shouldPause: Si debe pausarse cuando hay colisiones pausadas.
        frames: Cantidad de frames antes de ejecutar.
        repeat: Si se repite, cantidad de frames entre ejecuciones.

    Returns:
        dict: Objeto que representa la función temporizada.
    """
    func = {"frames": frames, "callback": callback, "pause": shouldPause, "repeat": repeat}
    _timed.append(func)
    return func


def quitar_frame_func(func: dict):
    """
    Elimina una función temporizada.

    Args:
        func: Objeto que representa la función temporizada.
    """
    if func in _timed:
        _timed.remove(func)


def addCollision(rect: pygame.Rect, func):
    """
    Agrega una colisión activa.

    Args:
        rect: Área de colisión.
        func: Función a ejecutar cuando se detecta clic en el área.

    Returns:
        tuple: Colisión agregada.
    """
    colision = (rect, func)
    _collisions.append(colision)
    return colision


def clearCollisions():
    """
    Elimina todas las colisiones activas.
    """
    _collisions.clear()


def quitar_colision(colision: tuple[pygame.Rect, Any]):
    """
    Elimina una colisión específica.

    Args:
        colision: Colisión a eliminar.
    """
    if colision in _collisions:
        _collisions.remove(colision)
    elif colision in _pausedCollisions:
        _pausedCollisions.remove(colision)


def add_paused_collision(rect: pygame.Rect, func):
    """
    Agrega una colisión que se ejecuta solo cuando el juego está pausado.

    Args:
        rect: Área de colisión.
        func: Función a ejecutar.

    Returns:
        tuple: Colisión agregada.
    """
    colision = (rect, func)
    _pausedCollisions.append(colision)
    return colision


def clear_paused_collisions():
    """
    Elimina todas las colisiones pausadas.
    """
    _pausedCollisions.clear()


def reset():
    """
    Reinicia el sistema de eventos (suscriptores, temporizadores, colisiones y banderas).
    """
    _subscribers.clear()
    _timed.clear()
    _collisions.clear()
    _pausedCollisions.clear()
    _flags.clear()


def full_reset():
    """
    Reinicia el sistema de eventos y también gráficos y animaciones.
    """
    reset()
    graphics.reset()
    animations.reset()


def postear(evento: int, data: dict | None = None):
    """
    Publica un evento en la cola de Pygame.

    Args:
        evento: Tipo de evento.
        data: Datos adicionales opcionales.
    """
    if data:
        pygame.event.post(pygame.event.Event(evento, data))
    else:
        pygame.event.post(pygame.event.Event(evento))


def quit():
    """
    Agrega un evento de salida en la cola de Pygame.
    """
    pygame.event.post(pygame.event.Event(pygame.QUIT))
