
import pygame
import config
import eventq

def next():
    """
    Genera un nuevo identificador único para eventos personalizados.

    Returns:
        int: Número de evento único.
    """
    num = config.ceventsBase
    config.ceventsBase += 1
    return num

SWITCH_TOKENS = next()
"""int: Evento para intercambiar tokens."""

CAMBIAR_PANTALLA = next()
"""int: Evento para cambiar la pantalla."""

def cambiar_pantalla(event: pygame.event.Event):
    """
    Ejecuta el cambio de pantalla según el destino definido en el evento.

    Args:
        event (pygame.event.Event): Evento que contiene la clave 'dest' con la función destino.
    """
    if event.dict and event.dict.get("dest", None):
        event.dict["dest"]()