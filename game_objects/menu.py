
from typing import Any
import pygame
import eventq
import display
import pantallas.inicio
import pantallas.juego
import graphics

import texto
from utils import convertir_csv_a_matriz, leer_archivo_texto

_estado: dict = {}
"""dict: Estado interno del menú (opciones, título y si está pausado)."""

_layer: list[tuple[pygame.Surface, pygame.Rect]] = []
"""list: Capa gráfica principal del menú (contiene superficies y rectángulos)."""

colisiones: list[tuple[pygame.Rect, Any]] = []
"""list: Lista de colisiones activas asociadas a las opciones del menú."""

OPCIONES = "opciones"
"""str: Clave para la lista de opciones del menú dentro de `_estado`."""

TITULO = "titulo"
"""str: Clave para el título opcional del menú dentro de `_estado`."""

PAUSADO = "pausado"
"""str: Clave que indica si el menú está en estado de pausa dentro de `_estado`."""


def iniciar(options: list[tuple[str, Any]], titulo: str | None = None, paused: bool = False):
    """
    Inicializa el menú con un conjunto de opciones.

    Args:
        options (list[tuple[str, Any]]): Lista de opciones. Cada opción es un par
            `(texto, callback)` donde `callback` es la función a ejecutar al seleccionar.
        titulo (str | None): Título opcional que se mostrará arriba del menú.
        paused (bool): Indica si el menú debe registrarse como “pausado”
            (las colisiones se agregan en la lista de colisiones pausadas).
    """
    _estado.clear()
    _estado[OPCIONES] = []
    for opt in options:
        _estado[OPCIONES].append(opt)
    if titulo:
        _estado[TITULO] = titulo
    _estado[PAUSADO] = paused
    graphics.addRenderer("menu", render, clear)
    render()


def clear():
    """
    Limpia la capa gráfica del menú y elimina las colisiones registradas.
    """
    graphics.removeLayer(_layer)
    _layer.clear()
    for colision in colisiones:
        eventq.quitar_colision(colision)
    colisiones.clear()


def render():
    """
    Renderiza el menú en pantalla con sus opciones y, si corresponde, un título.

    
        - Construye un contenedor semitransparente para el menú.
        - Alinea y distribuye los elementos (título y opciones) verticalmente.
        - Registra colisiones para permitir interacción con el mouse.
        - Si el menú está en pausa, las colisiones se agregan a la cola pausada.
    """
    clear()
    opciones = _estado[OPCIONES]

    # Área base del menú centrado
    limite = display.createGraphic(1, 1, display.createRect(0.5, 0.6))
    limite = display.alinear_en(limite, display.construir_limite(0, 1, 1), display.PRINCIPIO, 0, display.CENTRO)[1]

    temps = []
    items = []
    titulo = None

    # Título opcional
    if _estado.get(TITULO, None):
        titulo = texto.subtitulo(_estado[TITULO])
        temps.append(titulo)

    # Construcción de opciones (texto)
    for opcion in opciones:
        text = texto.normal(opcion[0])
        temps.append(text)
        items.append(text)

    # Duplicamos con padding y alineamos verticalmente
    temps = display.pad(temps, 0.3)
    display.alinear(temps)

    # Encastramos dentro del límite y construimos contenedor
    refs = display.encastrar(temps, limite, True)
    rect = display.crear_container(refs, 0.1)

    # Fondo semitransparente del menú
    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    menu_color = (255, 182, 193, 200)
    surf.fill(menu_color)
    surf.convert()
    _layer.append((surf, rect))
    graphics.addLayer(_layer)

    # Agregar título si está presente
    if titulo:
        _layer.append(refs[0])

    # Agregar cada opción y su colisión asociada
    for i in range(len(opciones)):
        opcion = opciones[i]
        graf = refs[temps.index(items[i])]
        _layer.append(graf)
        colision = opcion[1]
        if colision:
            if _estado[PAUSADO]:
                colisiones.append(eventq.add_paused_collision(graf[1], colision))
            else:
                colisiones.append(eventq.addCollision(graf[1], colision))


def menu_inicio():
    """
    Construye y muestra el menú de inicio del juego.

    Opciones:
        - Inicio: inicia la partida (cierra el menú y llama a `pantallas.juego.iniciar`).
        - Cambiar Resolucion: abre el menú de resoluciones.
        - Puntajes Mas Altos: muestra la lista de puntajes históricos.
        - Cerrar Juego: publica un evento `QUIT` y cierra la aplicación.
    """
    opciones = [
        ("Inicio", lambda: cerrar(pantallas.juego.iniciar)),
        ("Cambiar Resolucion", lambda: cerrar(menu_resoluciones)),
        ("Puntajes Mas Altos", lambda: cerrar(puntajes_mas_altos)),
        ("Cerrar Juego", eventq.quit)
    ]
    iniciar(opciones)


def puntajes_mas_altos():
    """
    Construye y muestra el menú con los puntajes históricos (solo lectura).

    
        - Lee `puntajes_historicos.csv`, convierte a matriz y muestra `nombre: puntaje`.
        - Agrega opción de 'volver' al menú anterior.
    """
    opciones = []
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz_2 = convertir_csv_a_matriz(datos)
    for row in matriz_2:
        nombre = row[0]
        puntaje = row[1]
        text = f"{nombre}: {puntaje}"
        opciones.append((text, None))
    opciones.append(("volver", lambda: cerrar(menu_inicio)))
    iniciar(opciones)


def menu_resoluciones():
    """
    Construye y muestra el menú para cambiar la resolución de la ventana.

    Opciones:
        - 800x600
        - 1200x800
        - 1920x1080
        - volver (regresa al menú de inicio)
    """
    opciones = [
        ("800x600", lambda: display.set_screen(800, 600)),
        ("1200x800", lambda: display.set_screen(1200, 800)),
        ("1920x1080", lambda: display.set_screen(1920, 1080)),
        ("volver", lambda: cerrar(menu_inicio))
    ]
    iniciar(opciones)


def menu_partida():
    """
    Construye y muestra el menú de pausa dentro de la partida.

    Opciones:
        - Continuar: cierra el menú y continúa el juego.
        - Reiniciar: reinicia la partida.
        - Abandonar: regresa a la pantalla de inicio.
    """
    opciones = [
        ("Continuar", lambda: cerrar()),
        ("Reiniciar", lambda: cerrar(pantallas.juego.iniciar)),
        ("Abandonar", lambda: cerrar(pantallas.inicio.iniciar))
    ]
    iniciar(opciones, "Pausa", True)


def cerrar(followup=None):
    """
    Cierra el menú actual y ejecuta una acción de seguimiento (si se indica).

    Args:
        followup: Función a ejecutar después de cerrar el menú (opcional).

    
        - Si el menú estaba en pausa, limpia las colisiones pausadas.
        - Remueve capas y limpia el estado interno.
        - Ejecuta `followup()` si se proporcionó.
    """
    if _estado.get(PAUSADO):
        eventq.clear_paused_collisions()
    clear()
    _estado.clear()
    if followup:
        followup()
