
import pygame
import config
import display
import graphics
from pantallas import nuevo_record
import sonido
import texto
from utils import first, guardar_archivo_texto, convertir_csv_a_matriz, leer_archivo_texto

estado: dict = {}
"""dict: Estado interno del puntaje actual."""

capa: list[tuple[pygame.Surface, pygame.Rect]] = []
"""list: Lista de gráficos para mostrar el puntaje en pantalla."""

POS = "pos"
PUNTOS = "puntos"

def iniciar():
    """
    Inicializa el sistema de puntaje en la partida.
    """
    estado.clear()
    estado[PUNTOS] = 0
    graphics.addRenderer("puntaje", None, clear)

def render(ref: pygame.Rect):
    """
    Renderiza el área donde se mostrará el puntaje.

    Args:
        ref (pygame.Rect): Rectángulo de referencia para posicionar el puntaje.
    """
    clear()
    graf = display.alinear_en(display.createGraphic(0.01, 0.01), ref, display.PRINCIPIO, 0.2, display.CENTRO)[1]
    screen = config.screen.get_rect()
    display.centrar_entre(graf, (ref.centerx, ref.bottom), (screen.centerx, screen.bottom))
    estado[POS] = graf
    graphics.addLayer(capa)
    cambiarPuntaje(0)

def clear():
    """
    Limpia la capa gráfica del puntaje.
    """
    graphics.removeLayer(capa)
    capa.clear()

def cambiarPuntaje(puntaje: int):
    """
    Actualiza el puntaje mostrado en pantalla.

    Args:
        puntaje (int): Nuevo puntaje.
    """
    estado[PUNTOS] = puntaje
    tupla = texto.normal(str(puntaje))
    tupla[1].centerx = estado[POS].centerx
    tupla[1].centery = estado[POS].centery
    capa.clear()
    capa.append(tupla)

def score(n: int, isSuper: bool):
    """
    Calcula el puntaje obtenido según la cantidad y tipo de movimiento.

    Args:
        n (int): Número de elementos eliminados.
        isSuper (bool): Indica si el movimiento es especial.

    Returns:
        int: Puntaje calculado.
    """
    if n <= 3:
        sonido.sonido_puntaje(isSuper)
        puntaje = n * 15
    else:
        sonido.sonido_puntaje_nivel_2(isSuper)
        puntaje = 3 * 20 + (n - 3) * 30
    return puntaje

def tiene_puntaje():
    """
    Verifica si el puntaje actual entra en el top 10 histórico.

    Returns:
        bool: True si entra en el top 10, False en caso contrario.
    """
    puntos = estado.get(PUNTOS, None)
    if not puntos:
        return

    if puntos == '0':
        return False
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz = convertir_csv_a_matriz(datos)

    entra_al_top_10 = False
    if len(matriz) < 10:
        entra_al_top_10 = True
    else:
        burbujeo_descendente(matriz)
        peor_puntaje = int(matriz[-1][1])

        if puntos > peor_puntaje:
            entra_al_top_10 = True

    return entra_al_top_10

def agregar_puntaje_historico():
    """
    Inicia la pantalla para agregar un nuevo puntaje histórico.
    """
    puntos = estado.get(PUNTOS, None)
    if not puntos:
        return
    nuevo_record.iniciar(puntos)

def guardar(nombre: str, puntos: int):
    """
    Guarda un nuevo puntaje histórico en el archivo CSV.

    Args:
        nombre (str): Nombre del jugador.
        puntos (int): Puntaje obtenido.

    Returns:
        bool: True si se guardó correctamente.
    """
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz = convertir_csv_a_matriz(datos)
    mismo_nombre = first(matriz, lambda x: x[0] == nombre)
    if int(mismo_nombre[1]) > puntos:
        return
    else:
        matriz.remove(mismo_nombre)
    matriz.append([nombre, str(puntos)])
    burbujeo_descendente(matriz)

    if len(matriz) > 10:
        matriz = matriz[:10]

    texto_csv = ""
    for fila in matriz:
        texto_csv += fila[0] + "," + fila[1] + "\n"

    texto_csv = texto_csv.strip()
    guardar_archivo_texto("puntajes_historicos.csv", texto_csv)

    return True

def limpiar_matriz(matriz):
    """
    Limpia una matriz eliminando filas incompletas o inválidas.

    Args:
        matriz (list[list]): Matriz original.

    Returns:
        list[list]: Matriz limpia.
    """
    matriz_limpia = []
    for fila in matriz:
        if len(fila) < 2:
            continue
        nombre = fila[0].strip()
        puntaje = fila[1].strip()
        if nombre == "" or puntaje == "":
            continue
        matriz_limpia.append([nombre, puntaje])
    return matriz_limpia

def burbujeo_descendente(matriz: list[list]):
    """
    Ordena la matriz de puntajes en orden descendente usando burbujeo.

    Args:
        matriz (list[list]): Matriz de puntajes.

    Returns:
        list[list]: Matriz ordenada.
    """
    n = len(matriz)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            v1 = matriz[j][1].strip()
            v2 = matriz[j+1][1].strip()
            if v1 == "" or v2 == "":
                continue
            a = int(v1)
            b = int(v2)
            if a < b:
                aux = matriz[j]
                matriz[j] = matriz[j+1]
                matriz[j+1] = aux
    return matriz
