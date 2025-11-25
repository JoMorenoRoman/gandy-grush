from utils import guardar_archivo_texto, convertir_csv_a_matriz, leer_archivo_texto

def score(n:int):
    if n <= 3:
        puntaje = n * 15
    else:
        puntaje = 3 * 15 + (n - 3) * 30
    puntaje = puntaje + int(leer_archivo_texto("puntaje.csv"))
    guardar_archivo_texto("puntaje.csv", puntaje)

def limpiar_puntaje():
    guardar_archivo_texto("puntaje.csv", '0')

def agregar_puntaje_historico():
    puntos = leer_archivo_texto("puntaje.csv")

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
    if not entra_al_top_10:
        return False

    # SI ENTRA → PIDO NOMBRE
    nombre = input("¡Nuevo récord! Por favor, ingresa tu nombre: ")

    # agregamos el nuevo registro
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
