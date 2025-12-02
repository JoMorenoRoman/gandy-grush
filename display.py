
import pygame
import config
import graphics
import texto
from utils import min, max

def set_screen(width: int, height: int):
    """
    Configura la pantalla principal del juego con las dimensiones configuradas.

    Args:
        width (int): Ancho de la pantalla.
        height (int): Alto de la pantalla.

        - Actualiza la pantalla con el nuevo tamaño.
        - Reinicia el sistema de texto y vuelve a renderizar gráficos.
    """
    config.screen = pygame.display.set_mode((width, height))
    texto.reset()
    graphics.re_render()


def centrar_entre(rect: pygame.Rect, xy1: tuple[int, int] | None, xy2: tuple[int, int] | None):
    """
    Centra un rectángulo dentro del área definida por dos puntos.

    Args:
        rect (pygame.Rect): Rectángulo a centrar.
        xy1 (tuple[int, int] | None): Puntos iniciales del área.
        xy2 (tuple[int, int] | None): Puntos finales del área.

    
        - Si no se especifican puntos, se usa el centro de la pantalla.
    """
    screen = config.screen.get_rect()
    if not xy1:
        xy1 = (screen.centerx, screen.centery)
    if not xy2:
        xy2 = (screen.centerx, screen.centery)

    area_width = xy2[0] - xy1[0]
    area_height = xy2[1] - xy1[1]

    rect.x = xy1[0] + (area_width - rect.width) // 2
    rect.y = xy1[1] + (area_height - rect.height) // 2


def align(item: pygame.Rect, x_third, y_third, ref: pygame.Rect | None = None):
    """
    Alinea un rectángulo en una posición basada en tercios dentro de una referencia.

    Args:
        item (pygame.Rect): Rectángulo a posicionar.
        x_third: Índice horizontal (0, 1, 2).
        y_third: Índice vertical (0, 1, 2).
        ref (pygame.Rect | None): Área de referencia (por defecto, pantalla).

    Returns:
        pygame.Rect: Rectángulo alineado.
    """
    if not ref:
        ref = config.screen.get_rect()
    x_sixth = ref.w / 6
    x_pos = ref.x + (x_sixth * ((x_third * 2) + 1))
    x_pos -= item.width / 2
    y_sixth = ref.h / 6
    y_pos = ref.y + (y_sixth * ((y_third * 2) + 1))
    y_pos -= item.height / 2
    item.x = x_pos
    item.y = y_pos
    return item


def centrar(item: tuple[pygame.Surface, pygame.Rect], referencia: pygame.Rect | None = None):
    """
    Centra un gráfico (Surface y Rect) dentro de una referencia.

    Args:
        item: Gráfico a centrar.
        referencia (pygame.Rect | None): Área de referencia  .

    Returns:
        tuple: Gráfico centrado.
    """
    if not referencia:
        referencia = config.screen.get_rect()
    item[1].centerx = referencia.centerx
    item[1].centery = referencia.centery
    return item


def matrix_align(matrix: list[list[dict]], token: pygame.Rect, x, y, container: pygame.Rect):
    """
    Agrega un rectángulo dentro de una matriz.

    Args:
        matrix (list[list[dict]]): Matriz.
        token (pygame.Rect): Rectángulo a agregar.
        x (int): Índice horizontal.
        y (int): Índice vertical.
        container (pygame.Rect): Área.
    """
    token.x = container.x + (token.w * x)
    token.y = container.y + (token.h * (len(matrix[0]) - y - 1))


def createGraphic(x_proportion: float = 1, y_proportion: float = 1, ref: pygame.Rect | None = None, **kwargs):
    """
    Crea un gráfico (Surface y Rect) proporcional al área de referencia.

    Args:
        x_proportion (float): Proporción del ancho.
        y_proportion (float): Proporción del alto.
        ref (pygame.Rect | None): Área de referencia (por defecto, pantalla).
        kwargs: Parámetros opcionales (e.g., color).

    Returns:
        tuple: Superficie y rectángulo creados.
    """
    if not ref:
        ref = config.screen.get_rect()
    rect = pygame.Rect(0, 0, ref.w * x_proportion, ref.h * y_proportion)
    surf = pygame.Surface((rect.w, rect.h))
    rect.centerx = ref.centerx
    rect.centery = ref.centery
    if kwargs and kwargs.get("color"):
        surf.fill(kwargs["color"])
    return (surf, rect)


def createRect(x_proportion: float = 1, y_proportion: float = 1, ref: pygame.Rect | None = None):
    """
    Crea un rectángulo proporcional al área de referencia.

    Args:
        x_proportion (float): Proporción del ancho.
        y_proportion (float): Proporción del alto.
        ref (pygame.Rect | None): Área de referencia.

    Returns:
        pygame.Rect: Rectángulo creado.
    """
    return createGraphic(x_proportion, y_proportion, ref)[1]


def square(rect: pygame.Rect):
    """
    Convierte un rectángulo en un cuadrado usando su ancho o alto.

    Args:
        rect (pygame.Rect): Rectángulo original.

    Returns:
        pygame.Rect: Nuevo rectángulo cuadrado.
    """
    if rect.w == 0:
        rect = pygame.Rect(rect.left, rect.top, rect.h, rect.h)
    else:
        rect = pygame.Rect(rect.left, rect.top, rect.w, rect.w)
    return rect


def make_multiple(rect: pygame.Rect, xMult: int | None, yMult: int | None):
    """
    Ajusta las dimensiones de un rectángulo para que sean múltiplos de los valores indicados.

    Args:
        rect (pygame.Rect): Rectángulo a ajustar.
        xMult (int | None): Múltiplo para el ancho.
        yMult (int | None): Múltiplo para el alto.

    Returns:
        pygame.Rect: Rectángulo ajustado.
    """
    while xMult and rect.width % xMult != 0:
        rect.width -= 1
    while yMult and rect.height % yMult != 0:
        rect.height -= 1
    return rect


def construir_limite(borde: float, tercio_x: int, tercio_y: int, ref: pygame.Rect | None = None):
    """
    Construye un rectángulo dentro de una grilla de tercios con borde interno.

    Args:
        borde (float): Proporción del borde.
        tercio_x (int): Índice horizontal (0, 1, 2).
        tercio_y (int): Índice vertical (0, 1, 2).
        ref (pygame.Rect | None): Área de referencia.

    Returns:
        pygame.Rect: Rectángulo construido.
    """
    if not ref:
        ref = config.screen.get_rect()
    tercio_ancho = ref.width / 3
    tercio_alto = ref.height / 3
    borde_x = tercio_ancho * borde
    borde_y = tercio_alto * borde
    x = ref.x + (tercio_ancho * tercio_x) + borde_x
    y = ref.y + (tercio_alto * tercio_y) + borde_y
    return pygame.Rect(x, y, tercio_ancho - (borde_x * 2), tercio_alto - (borde_y * 2))


def combinar_limites(lim1: pygame.Rect, lim2: pygame.Rect):
    """
    Combina dos límites en un rectángulo que los contenga.

    Args:
        lim1 (pygame.Rect): Primer límite.
        lim2 (pygame.Rect): Segundo límite.

    Returns:
        pygame.Rect: Rectángulo combinado.
    """
    min_x = min([lim1, lim2], lambda f: f.x)
    min_y = min([lim1, lim2], lambda f: f.y)
    ancho = max([lim1, lim2], lambda f: f.right) - min_x
    alto = max([lim1, lim2], lambda f: f.bottom) - min_y
    return pygame.Rect(min_x, min_y, ancho, alto)  # type: ignore


def encastrar(graficos: list[tuple[pygame.Surface, pygame.Rect]], ref: pygame.Rect, no_expandir: bool = False):
    """
    Escala y posiciona una lista de gráficos dentro de un área de referencia.

    Args:
        graficos (list): Lista de gráficos (Surface y Rect).
        ref (pygame.Rect): Área de referencia.
        no_expandir (bool): Si es True, evita escalar hacia arriba.

    Returns:
        dict: Diccionario con gráficos escalados y posicionados.
    """
    min_x = min(graficos, lambda f: f[1].x)
    min_y = min(graficos, lambda f: f[1].y)
    ancho = max(graficos, lambda f: f[1].right) - min_x
    alto = max(graficos, lambda f: f[1].bottom) - min_y

    escala_ancho = ref.width / ancho
    escala_alto = ref.height / alto

    escala: float = min([escala_ancho, escala_alto], lambda f: f)
    if no_expandir and escala > 1:
        escala = 1
    result: dict[int, tuple[pygame.Surface, pygame.Rect]] = {}
    y = ref.top
    for i in range(len(graficos)):
        surf, rect = graficos[i]
        nuevo_ancho = int(rect.width * escala)
        nuevo_alto = int(rect.height * escala)
        nuevo_surf = pygame.transform.smoothscale(surf, (nuevo_ancho, nuevo_alto))
        rel_x = rect.x - min_x
        rel_y = rect.y - min_y
        nuevo_x = ref.x + int(rel_x * escala)
        nuevo_y = ref.y + int(rel_y * escala)
        nuevo_rect = pygame.Rect(nuevo_x, nuevo_y, nuevo_ancho, nuevo_alto)
        nuevo_rect.centerx = ref.centerx
        nuevo_rect.y = y
        y += nuevo_rect.h
        result[i] = (nuevo_surf, nuevo_rect)
    return result


def crear_container(grafs: dict, borde: float):
    """
    Crea un contenedor que engloba todos los gráficos con un borde adicional.

    Args:
        grafs (dict): Diccionario de gráficos.
        borde (float): Proporción del borde.

    Returns:
        pygame.Rect: Rectángulo contenedor.
    """
    values = list(grafs.values())
    min_x = min(values, lambda f: f[1].x)
    min_y = min(values, lambda f: f[1].y)
    ancho = max(values, lambda f: f[1].right) - min_x
    alto = max(values, lambda f: f[1].bottom) - min_y
    borde_x = ancho * borde
    min_x -= borde_x
    ancho += borde_x * 2
    borde_y = alto * borde
    min_y -= borde_y
    alto += borde_y * 2
    return pygame.Rect(min_x, min_y, ancho, alto)


def pad(items: list[tuple[pygame.Surface, pygame.Rect]], escala: float):
    """
    Duplica una lista de gráficos agregando versiones escaladas.

    Args:
        items (list): Lista de gráficos.
        escala (float): Factor de escala.

    Returns:
        list: Lista original más gráficos escalados.
    """
    res = []
    for item in items:
        res.append(item)
        pad_surf = pygame.transform.smoothscale(item[0], (item[1].w * escala, item[1].h * escala))
        res.append((pad_surf, pad_surf.get_rect()))
    return res


def alinear(items: list[tuple[pygame.Surface, pygame.Rect]]):
    """
    Alinea una lista de gráficos en columna.

    Args:
        items (list): Lista de gráficos.
    """
    x = 0
    y = 0
    for _, rect in items:
        rect.x = x
        rect.y = y
        y += rect.height


PRINCIPIO = "principio"
CENTRO = "centro"
FINAL = "final"

def alinear_en(grafico: tuple[pygame.Surface, pygame.Rect], ref: pygame.Rect | None, posicion: str | None = None, borde: float | None = None, posicion_horizontal: str | None = None):
    """
    Alinea un gráfico dentro de una referencia según posición vertical y horizontal.

    Args:
        grafico (tuple): Gráfico a alinear.
        ref (pygame.Rect | None): Área de referencia.
        posicion (str | None): Posición vertical ('principio', 'centro', 'final').
        borde (float | None): Proporción del borde.
        posicion_horizontal (str | None): Posición horizontal ('principio', 'centro', 'final').

    Returns:
        tuple: Gráfico alineado.
    """
    if not ref:
        ref = config.screen.get_rect()
    if borde:
        borde = round(ref.height * borde)
    else:
        borde = 0
    if posicion:
        if posicion == PRINCIPIO:
            grafico[1].top = ref.top + borde
        elif posicion == CENTRO:
            grafico[1].centery = ref.centery
        elif posicion == FINAL:
            grafico[1].bottom = ref.bottom - borde
    if posicion_horizontal:
        if posicion_horizontal == PRINCIPIO:
            grafico[1].left = ref.left + borde
        elif posicion_horizontal == CENTRO:
            grafico[1].centerx = ref.centerx
        elif posicion_horizontal == FINAL:
            grafico[1].right = ref.right - borde
    return grafico
