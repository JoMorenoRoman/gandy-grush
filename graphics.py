
from typing import Any
import pygame
import config

_layers: list[list[tuple[pygame.Surface, pygame.Rect]]] = []
_overlay: list[tuple[pygame.Surface, pygame.Rect]] = []
_clipped: dict[int, pygame.Rect] = {}
_temps: dict[int, list[tuple[pygame.Surface, pygame.Rect]]] = {}
_renderers: dict[str, tuple[Any, Any]] = {}

def addLayer(layer: list[tuple[pygame.Surface, pygame.Rect]], clipped: pygame.Rect | None = None):
    """
    Agrega una capa al sistema de renderizado.

    Args:
        layer: Lista de gráficos (Surface y Rect) que componen la capa.
        clipped: Área de recorte opcional para la capa.

    Returns:
        list: La capa agregada.
    """
    _layers.append(layer)
    if clipped:
        _clipped[len(_layers) - 1] = clipped
    return layer


def removeLayer(layer: list[tuple[pygame.Surface, pygame.Rect]]):
    """
    Elimina una capa del sistema de renderizado y ajusta las áreas de recorte.

    Args:
        layer: Capa a eliminar.
    """
    if layer in _layers:
        index = _layers.index(layer)
        _layers.remove(layer)
        if _clipped.get(index):
            _clipped.pop(index)
        for key in sorted(_clipped.keys()):
            if key > index:
                _clipped[key - 1] = _clipped[key]


def buscar_capa(grafico: tuple[pygame.Surface, pygame.Rect]):
    """
    Busca la capa que contiene un gráfico específico.

    Args:
        grafico: Gráfico (Surface y Rect) a buscar.

    Returns:
        int | None: Índice de la capa o None si no se encuentra.
    """
    index = None
    for i, capa in enumerate(_layers):
        if grafico in capa:
            index = i
    return index


def removeGraphic(graphic: tuple[pygame.Surface, pygame.Rect]):
    """
    Elimina un gráfico de la capa en la que se encuentra.

    Args:
        graphic: Gráfico (Surface y Rect) a eliminar.

    Returns:
        list | None: La capa modificada o None si no se encontró.
    """
    for layer in _layers:
        if graphic in layer:
            layer.remove(graphic)
            return layer
    return None


def add_temp(grafico: tuple[pygame.Surface, pygame.Rect], capa: int | None):
    """
    Agrega un gráfico temporal a una capa específica.

    Args:
        grafico: Gráfico (Surface y Rect).
        capa: Índice de la capa o -1 si es global.
    """
    if not capa:
        capa = -1
    if _temps.get(capa):
        _temps[capa].append(grafico)
    else:
        _temps[capa] = [grafico]


def reset():
    """
    Reinicia el sistema de capas y renderizadores.
    """
    _layers.clear()
    _clipped.clear()
    _temps.clear()
    _overlay.clear()
    for _, clear in _renderers.values():
        if clear:
            clear()
    _renderers.clear()


def addRenderer(ref, render, clear):
    """
    Registra un renderizador adicional.

    Args:
        ref: Referencia única.
        render: Función para renderizar.
        clear: Función para limpiar.
    """
    _renderers[ref] = (render, clear)


def re_render():
    """
    Ejecuta todos los renderizadores registrados.
    """
    for render, _ in _renderers.values():
        if render:
            render()


def setBackground(background: pygame.Surface):
    """
    Establece la imagen de fondo.

    Args:
        background: Imagen de fondo.
    """
    config.background = background


def renderizar():
    """
    Renderiza todas las capas y gráficos temporales en la pantalla principal.

    
        - Aplica recortes si están definidos.
        - Limpia gráficos temporales después de dibujar.
        - Actualiza la pantalla.
    """
    config.screen.blit(config.background, (0, 0))
    for i, layer in enumerate(_layers):
        clip = _clipped.get(i)
        if clip:
            config.screen.set_clip(clip)
        for (surf, rect) in layer:
            config.screen.blit(surf, rect)
        if _temps.get(i):
            for (surf, rect) in _temps[i]:
                config.screen.blit(surf, rect)
        config.screen.set_clip(None)
    if _temps.get(-1):
        for (surf, rect) in _temps[-1]:
            config.screen.blit(surf, rect)
    _temps.clear()
    pygame.display.flip()
