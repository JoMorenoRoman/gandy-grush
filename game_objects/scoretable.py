import pygame
import config
import display
import graphics
from pantallas import nuevo_record
from utils import guardar_archivo_texto, convertir_csv_a_matriz, leer_archivo_texto

estado:dict = {}
GRAFS = "grafs"
REF = "ref"
POS = "pos"
PUNTOS = "puntos"

def iniciar(referencia:pygame.Rect):
    clear()
    estado.clear()
    estado[REF] = referencia
    estado[GRAFS] = []
    estado[PUNTOS] = 0
    graphics.addRenderer(render, clear)
    render()

def render():
    clear()
    ref:pygame.Rect = estado[REF]
    graf = pygame.Rect(0, 0, 10, 10)
    estado[POS] = graf
    graphics.addLayer(estado[GRAFS])
    screen = config.screen.get_rect()
    display.centrar_entre(graf, (ref.centerx, ref.bottom), (screen.centerx, screen.bottom))
    
def clear():        
    if estado.get(GRAFS, None):
        graphics.removeLayer(estado[GRAFS])
        
def cambiarPuntaje(puntaje:int):
    text = config.texto.render(str(puntaje), True, config.TEXT_COLOR)
    tupla = (text, text.get_rect())
    tupla[1].centerx = estado[POS].centerx
    tupla[1].centery = estado[POS].centery
    grafs = estado[GRAFS]
    if len(grafs) > 0:
        graphics.removeGraphic(grafs[-1])
        grafs.clear()
    grafs.append(tupla)
    estado[PUNTOS] = puntaje

def score(n:int):
    if n <= 3:
        puntaje = n * 15
    else:
        puntaje = 3 * 15 + (n - 3) * 30
    return puntaje

def tiene_puntaje():
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

    # si NO entra → no pedimos nombre
    return entra_al_top_10

def agregar_puntaje_historico():
    puntos = estado.get(PUNTOS, None)
    if not puntos:
        return
    nuevo_record.iniciar(puntos, guardar)

def guardar(nombre:str, puntos:int):
    # agregamos el nuevo registro
    datos = leer_archivo_texto("puntajes_historicos.csv")
    matriz = convertir_csv_a_matriz(datos)
    matriz.append([nombre, str(puntos)])
    burbujeo_descendente(matriz)

    # recortar top 10
    if len(matriz) > 10:
        matriz = matriz[:10]

    texto = ""
    for fila in matriz:
        texto += fila[0] + "," + fila[1] + "\n"

    texto = texto.strip()
    guardar_archivo_texto("puntajes_historicos.csv", texto)

    return True

def limpiar_matriz(matriz):
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

def burbujeo_descendente(matriz:list[list]):
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
