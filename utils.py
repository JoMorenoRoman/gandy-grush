def guardar_archivo_texto(ruta:str, datos:str)-> None:
    archivo = open(ruta,"w")
    archivo.write(datos)
    archivo.close()

def leer_archivo_texto(ruta:str)->str|None:
    try:
        with open(ruta, "r") as archivo:
            datos = archivo.read()
    except:
        print("La Ruta No Existe..")
        datos = None
    return datos    

def convertir_csv_a_matriz(datos:str|None)->list[list]:
    if not datos:
        return []
    datos_limpios = datos.strip()
    lista_filas = datos_limpios.split("\n")
    matriz = []
    for i in range(len(lista_filas)):
        lista_columnas = lista_filas[i].split(",")
        matriz.append(lista_columnas)
    return matriz    
