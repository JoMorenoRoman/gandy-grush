
import math
import pygame
import graphics
import timer
import random

animaciones: list[dict] = []
"""list[dict]: Lista de animaciones activas."""

CALLBACK = "callback"
FRAME = "frame"
DURACION = "duracion"

def ejecutar():
    """
    Ejecuta todas las animaciones activas y elimina las completadas.

        - Incrementa el frame actual.
        - Llama al callback de cada animación.
    """
    removes = []
    for anim in animaciones:
        if anim[FRAME] >= anim[DURACION]:
            removes.append(anim)
            continue
        else:
            anim[CALLBACK]()
            anim[FRAME] += 1
    for remove in removes:
        animaciones.remove(remove)
    return

ROUND = "round"
DEST = "destino"
ORIGEN = "origen"

def shake_token(token: tuple[pygame.Surface, pygame.Rect], state: dict | None = None):
    """
    Aplica una animación de sacudida a un token.

    Args:
        token: Token (Surface y Rect).
        state: Estado interno de la animación.
    """
    if not state:
        state = {
            DURACION: timer.seconds(1) / 3,
            FRAME: 1,
            ROUND: 1,
            ORIGEN: token[1].x
        }
        state[CALLBACK] = lambda: shake_token(token, state)
        animaciones.append(state)

    if not state.get(DEST):
        match state[ROUND]:
            case 1:
                state[DEST] = (state[ORIGEN] - (token[1].w) / 3, token[1].y)
            case 2:
                state[DEST] = (state[ORIGEN] + (token[1].w) / 3, token[1].y)
            case 3:
                state[DEST] = (state[ORIGEN], token[1].y)

    move_token(token, state[DEST], estado=state)

    if state[FRAME] == (state[DURACION] - 1) and state[ROUND] != 3:
        state[DEST] = None
        state[FRAME] = 1
        state[ROUND] += 1
    return

def switch_tokens(token1: tuple[pygame.Surface, pygame.Rect], token2: tuple[pygame.Surface, pygame.Rect], duration: float):
    """
    Intercambia la posición de dos tokens con animación.

    Args:
        token1 (tuple): Primer token.
        token2 (tuple): Segundo token.
        duration (float): Duración de la animación en segundos.
    """
    dest1 = (token2[1].x, token2[1].y)
    dest2 = (token1[1].x, token1[1].y)
    move_token(token1, dest1, duration)
    move_token(token2, dest2, duration)
    return

def move_token(token: tuple[pygame.Surface, pygame.Rect], dest: tuple[int, int], duracion: float = 0.5, estado: dict | None = None):
    """
    Mueve un token hacia una posición destino con animación.

    Args:
        token (tuple): Token (Surface y Rect).
        dest (tuple[int, int]): Coordenadas destino.
        duracion (float): Duración en segundos.
        estado (dict | None): Estado interno de la animación.
    """
    if not estado:
        estado = {
            DURACION: timer.seconds(duracion),
            FRAME: 1
        }
        estado[CALLBACK] = lambda: move_token(token, dest, estado=estado)
        animaciones.append(estado)
    resto = estado[DURACION] - estado[FRAME]
    token[1].x = mover_lineal(token[1].x, dest[0], resto)
    token[1].y = mover_lineal(token[1].y, dest[1], resto)
    return

ACTUAL = "actual"

def destroy_token(token: tuple[pygame.Surface, pygame.Rect], duracion: float = 0.5, state: dict | None = None):
    """
    Aplica animación de destrucción a un token (rotación y reducción).

    Args:
        token (tuple): Token (Surface y Rect).
        duracion (float): Duración en segundos.
        state (dict | None): Estado interno de la animación.
    """
    if not state:
        state = {
            DURACION: timer.seconds(duracion),
            FRAME: 1,
            LAYER: graphics.buscar_capa(token)
        }
        graphics.removeGraphic(token)
        state[CALLBACK] = lambda: destroy_token(token, duracion, state)
        animaciones.append(state)

    if state.get(ACTUAL):
        current = state[ACTUAL]
    else:
        current = 0

    remaining = state[DURACION] - state[FRAME]
    rotacion = mover_lineal(current, 360, remaining)
    surf = pygame.transform.rotate(token[0], rotacion)
    size = surf.get_size()
    size = (mover_lineal(size[0], 0, remaining), mover_lineal(size[1], 0, remaining))
    surf = pygame.transform.smoothscale(surf, size)
    graphics.add_temp((surf, token[1]), state[LAYER])
    state[ACTUAL] = rotacion
    return

LAYER = "layer"

def titilar(token: tuple[pygame.Surface, pygame.Rect], duracion: float = 0.5, max_brillo: int = 60, estado: dict | None = None):
    """
    Aplica animación de parpadeo a un token.

    Args:
        token (tuple): Token (Surface y Rect).
        duracion (float): Duración en segundos.
        max_brillo (int): Nivel máximo de brillo.
        estado (dict | None): Estado interno de la animación.
    """
    if not estado:
        estado = {
            DURACION: timer.seconds(duracion),
            FRAME: 1,
            LAYER: graphics.buscar_capa(token)
        }
        estado[CALLBACK] = lambda: titilar(token, duracion, max_brillo, estado)
        animaciones.append(estado)

    progreso = round(mover_curvo(max_brillo, estado[FRAME], estado[DURACION]))
    temp: pygame.Surface = token[0].copy()
    temp.fill((progreso, progreso, progreso), special_flags=pygame.BLEND_RGB_ADD)
    graphics.add_temp((temp, token[1]), estado[LAYER])
    return estado

def opacar(rect: pygame.Rect, duracion: float = 1, max_opaco: int = 255, estado: dict | None = None):
    """
    Aplica animación de oscurecimiento sobre un área.

    Args:
        rect (pygame.Rect): Área a oscurecer.
        duracion (float): Duración en segundos.
        max_opaco (int): Nivel máximo de opacidad.
        estado (dict | None): Estado interno de la animación.
    """
    if not estado:
        estado = {
            DURACION: timer.seconds(duracion),
            FRAME: 1,
        }
        estado[CALLBACK] = lambda: opacar(rect, duracion, max_opaco, estado)
        animaciones.append(estado)

    progreso = round(mover_curvo(max_opaco, estado[FRAME], estado[DURACION]))
    temp = pygame.Surface((rect.w, rect.h))
    temp.fill((0, 0, 0))
    temp.set_alpha(progreso)
    graphics.add_temp((temp, rect), None)
    return estado

def mover_curvo(final: int, frame_actual: int, frame_final: int):
    """
    Calcula un valor curvo para animación (usando seno).

    Args:
        final (int): Valor final.
        frame_actual (int): Frame actual.
        frame_final (int): Frame final.

    Returns:
        float: Valor calculado.
    """
    progreso = 1 - (frame_actual / frame_final)
    curvado = math.sin(progreso * math.pi)
    return final * curvado

def mover_lineal(origin: int, dest: int, interval: int):
    """
    Calcula un valor lineal para animación.

    Args:
        origin (int): Valor inicial.
        dest (int): Valor destino.
        interval (int): Intervalo restante.

    Returns:
        int: Valor calculado.
    """
    return origin + round((dest - origin) / interval)

def reset():
    """
    Reinicia la lista de animaciones activas.
    """
    animaciones.clear()
