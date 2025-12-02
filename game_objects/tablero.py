import time
import pygame
import random
import animations
import display
import eventq
from game_objects import scoretable
import graphics
import game_objects.tokens as t
import sonido

C_LEFT = (-1, 0)
C_UP = (0, 1)
C_RIGHT = (1, 0)
C_DOWN = (0, -1)
CARDINALS = [C_LEFT, C_UP, C_RIGHT, C_DOWN]

STATE = "state"
TYPE = "type"
GRAPHIC = "graphic"
POSITION = "position"
COLISION = "collition"
SUPER = "super"
MATRIX = "matrix"
SUPER_LIMITE = "super_limite"
BUSY = "busy"
ANIM_SPEED = "animation_speed"
NEXT_SUPER = "next_super"
PUNTAJE = "puntaje"
ULTIMO_CLICK = "ultimo_click"


def iniciar(matrix:list[list[dict]], rows:int, columns:int, imposible:bool = False):
    """Inicializa la matriz con tokens.
    Args:
        matrix (list[list[dict]]): Matriz del tablero.
        rows (int): Cantidad de filas.
        columns (int): Cantidad de columnas.
        imposible (bool): Si crea un patron sin combinaciones posibles.
    Returns:
        list[list[dict]]: Matriz inicializada.
    """
    matrix.clear()
    for x in range(rows):
        matrix.append([])
        for y in range(columns):
            matrix[x].append({})
            crear_token(matrix, x, y)
    if imposible:
        for x, row in enumerate(matrix):
            for y, cell in enumerate(row):
                base = 0
                if y % 2:
                    base = 3
                cell[TYPE] = base + x % 3 
    return matrix


def crear_token(matrix:list[list[dict]], x:int, y:int):
    """Crea un token en la posicion dada.
    Args:
        matrix (list[list[dict]]): Matriz de juego.
        x (int): Fila.
        y (int): Columna.
    """
    type = elegir_color(matrix, x, y)
    token = {
        TYPE: type,
        GRAPHIC: None,
        STATE: t.IDLE,
        POSITION: (x, y),
        COLISION: None,
        SUPER: None
        }
    matrix[x][y] = token
    

def elegir_color(matrix:list[list[dict]], x:int, y:int):
    """Elige un color evitando matches inmediatos.
    Args:
        matrix (list[list[dict]]): Matriz del tablero.
        x (int): Fila actual.
        y (int): Columna actual.
    Returns:
        int: Tipo de token.
    """
    invalids = colores_con_match(matrix, x, y)
    while True:
        color = random.randint(0, len(t.types) - 1)
        if color not in invalids:
            break
    return color


SENTIDO_H = "horizontal"
SENTIDO_V = "vertical"
def colores_con_match(matrix:list[list[dict]], x:int, y:int, sentido:str|None = None):
    """Calcula tipos que formarian un match.
    Args:
        matrix (list[list[dict]]): Matriz del juego.
        x (int): Fila objetivo.
        y (int): Columna objetivo.
        sentido (str|None): Direccion opcional de analisis.
    Returns:
        set[int]: Tipos invalidos.
    """
    types = set()
    if sentido:
       if sentido == SENTIDO_H:
           direcciones = [(1, 0)] 
       else:
           direcciones = [(0, 1)]
    else:
        direcciones = [(1, 0),(0, 1)]
        
    for direccion in direcciones:
        for pairs in [[-2, -1], [-1, 1], [1, 2]]:
            compare = None
            for distance in pairs:
                item = safe_index(matrix, sumar((x, y), mult_escalar(direccion, distance)))
                if not item:
                    continue
                if compare and compare[TYPE] == item[TYPE]:
                    types.add(item[TYPE])
                else:
                    compare = item
    return types
        
        
def render(tablero:dict, container:pygame.Rect, token_rect:pygame.Rect):
    """Renderiza todos los tokens en pantalla.
    Args:
        tablero (dict): Datos del tablero.
        container (pygame.Rect): Area de render.
        token_rect (pygame.Rect): Tamano base del token.
    Returns:
        list: Capa grafica con tokens.
    """
    matrix = tablero[MATRIX]
    layer = tablero["capa"]
    graphics.addLayer(layer, container)
    set_as_busy(tablero, tablero[ANIM_SPEED])
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            primer_render_token(tablero, x, y, layer, container, token_rect)
    return layer


def set_as_busy(tablero:dict, duration:float):
    """Marca el tablero como ocupado temporalmente.
    Args:
        tablero (dict): Tablero.
        duration (float): Tiempo en segundos.
    """
    set_state(tablero, True)
    eventq.addTimed(duration, lambda: set_state(tablero, False))


def set_state(tablero:dict, state:bool):
    """Cambia el estado ocupado del tablero.
    Args:
        tablero (dict): Tablero.
        state (bool): Nuevo estado.
    """
    tablero[BUSY] = state


def primer_render_token(tablero:dict, x:int, y:int, layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    """Renderiza un token con animacion de entrada.
    Args:
        tablero (dict): Datos del tablero.
        x (int): Fila.
        y (int): Columna.
        layer (list): Capa grafica.
        container (pygame.Rect): Area de render.
        token_rect (pygame.Rect): Tamano base.
    """
    matrix = tablero[MATRIX]
    token = matrix[x][y]
    rect = token_rect.copy()
    display.matrix_align(matrix, rect, x, y, container)
    if tablero.get(NEXT_SUPER, None) is not None:
        token[SUPER] = t.SUPERS[tablero[NEXT_SUPER]]
        tablero[NEXT_SUPER] = None
    color = t.graficar_token(token[TYPE], token[SUPER])
        
    token[GRAPHIC] = (color, rect)
    pos_y = token[GRAPHIC][1].y
    token[GRAPHIC][1].y -= container.height
    layer.append(token[GRAPHIC])
    token[COLISION] = eventq.addCollision(token[GRAPHIC][1], lambda: select(tablero, token))
    animations.move_token(token[GRAPHIC], (token[GRAPHIC][1].x, pos_y), tablero[ANIM_SPEED])


def select(tablero:dict, token:dict):
    """Gestiona seleccion y switch de tokens.
    Args:
        tablero (dict): Tablero.
        token (dict): Token seleccionado.
    """
    tablero[ULTIMO_CLICK] = time.time()
    x = token[POSITION][0]
    y = token[POSITION][1]
    matrix:list[list[dict]] = tablero[MATRIX]
    if tablero[BUSY] or not token:
        return
    match token[STATE]:
        case t.IDLE | t.SELECT:
            reset(matrix)
            token[STATE] = t.SELECT
            for item in cardinals(matrix, (x, y)):
                if item[STATE] == t.IDLE:
                    item[STATE] = t.HIGHLIGHT
        case t.HIGHLIGHT:
            if not get_selected(matrix):
                token[STATE] = t.IDLE
                select(tablero, token)
            else:
                try_switch(tablero, x, y)
                reset(matrix)
    

def reset(matrix:list[list[dict]], resetTo:str = t.IDLE):
    """Resetea estados de todos los tokens.
    Args:
        matrix (list[list[dict]]): Matriz.
        resetTo (str): Estado destino.
    """
    for row in matrix:
        for cell in row:
            cell[STATE] = resetTo


def try_switch(tablero:dict, x:int, y:int):
    """Intenta intercambiar tokens.
    Args:
        tablero (dict): Tablero.
        x (int): Fila.
        y (int): Columna.
    """
    matrix = tablero[MATRIX]
    selected = get_selected(matrix)
    if not selected:
        reset(matrix)
        return
    switch_token = matrix[x][y]
    switch(matrix, selected, switch_token)
    if hay_matches(matrix, [selected, switch_token]):
        set_as_busy(tablero, tablero[ANIM_SPEED])
        animations.switch_tokens(selected[GRAPHIC], switch_token[GRAPHIC], tablero[ANIM_SPEED])
        sonido.reproducir_sonido(sonido.MOVER)
    else:
        set_as_busy(tablero, 1)
        switch(matrix, selected, switch_token)
        for rejected in [selected, switch_token]:
            sonido.reproducir_sonido(sonido.MOVER_MAL)
            animations.shake_token(rejected[GRAPHIC])
            

def get_selected(matrix:list[list[dict]]):
    """Obtiene el token seleccionado.
    Args:
        matrix (list[list[dict]]): Matriz del juego.
    Returns:
        dict|None: Token seleccionado.
    """
    for row in matrix:
        for cell in row:
            if cell[STATE] == t.SELECT:
                return cell
    return None
    

def hay_matches(matrix:list[list[dict]], tokens:list[dict]):
    """Verifica si un intercambio produce un match.
    Args:
        matrix (list[list[dict]]): Matriz.
        tokens (list[dict]): Tokens evaluados.
    Returns:
        bool: Si hay match.
    """
    result = False
    for token in tokens:
        matching = colores_con_match(matrix, token[POSITION][0], token[POSITION][1])
        if token[TYPE] in matching:
            result = True
            break
    return result


def switch(matrix:list[list[dict]], selected:dict, switch:dict):
    """Intercambia dos tokens.
    Args:
        matrix (list[list[dict]]): Matriz.
        selected (dict): Token seleccionado.
        switch (dict): Token objetivo.
    """
    temp = selected[POSITION]
    move_to(matrix, selected, switch[POSITION])
    move_to(matrix, switch, temp)


def move_to(matrix:list[list[dict]], token:dict|None, to:tuple[int, int]):
    """Mueve un token a otra posicion.
    Args:
        matrix (list[list[dict]]): Matriz.
        token (dict|None): Token.
        to (tuple[int,int]): Posicion destino.
    """
    matrix[to[0]][to[1]] = token  # type: ignore
    if token:
        token[POSITION] = to


def fill_empty(tablero:dict, layer:list, container:pygame.Rect, token_rect:pygame.Rect):
    """Rellena espacios vacios despues de destrucciones.
    Args:
        tablero (dict): Datos del tablero.
        layer (list): Capa grafica.
        container (pygame.Rect): Area de render.
        token_rect (pygame.Rect): Tamano base.
    """
    if tablero[BUSY]:
        return
    matrix:list[list[dict]] = tablero[MATRIX]
    changes = False
    for y in range(len(matrix[0])):
        for x in range(len(matrix)):
            if not safe_index(matrix, (x, y)):
                changes = True
                replacement = fall_replace(matrix, x, y)
                if replacement:
                    dest = token_rect.copy()
                    display.matrix_align(matrix, dest, x, y, container)
                    animations.move_token(replacement[GRAPHIC], (dest.x, dest.y), tablero[ANIM_SPEED] % 2)
                    moved_from = replacement[POSITION]
                    move_to(matrix, replacement, (x, y))
                    move_to(matrix, None, moved_from)
                else:
                    crear_token(matrix, x, y)
                    primer_render_token(tablero, x, y, layer, container, token_rect)
    if changes:
        set_as_busy(tablero, tablero[ANIM_SPEED])
    

def fall_replace(matrix:list[list[dict]], x:int, y:int) -> dict|None:
    """Busca un token arriba para bajar.
    Args:
        matrix (list[list[dict]]): Matriz.
        x (int): Fila.
        y (int): Columna.
    Returns:
        dict|None: Token encontrado o None.
    """
    y += 1
    if in_bound(matrix, (x, y)):
        replacement = safe_index(matrix, (x, y))
        if replacement:
            return replacement
        else:
            return fall_replace(matrix, x, y)
    else:
        return None    


def buscar_matches(tablero:dict):
    """Busca matches en el tablero.
    Args:
        tablero (dict): Datos del tablero.
    """
    if tablero[BUSY]:
        return
    matrix:list[list[dict]] = tablero[MATRIX]
    for x in range(len(matrix)):
        matching = buscar(matrix, x, 0, C_UP, buscar_3)
        if len(matching) > 2:
            break
    if len(matching) < 3:
        for y in range(len(matrix[0])):
            matching = buscar(matrix, 0, y, C_RIGHT, buscar_3)
            if len(matching) > 2:
                break
    if len(matching) > 2:
        score(tablero, matching)
        destroy(tablero, matching)
        

def score(tablero:dict, line:list[dict]):
    """Suma puntaje y determina supers.
    Args:
        tablero (dict): Datos del tablero.
        line (list[dict]): Tokens del match.
    """
    horizontal = line[0][POSITION][1] == line[1][POSITION][1]
    agregar_eje_contrario(tablero[MATRIX], line, horizontal)
    super = False
    for token in line:
        if token[SUPER]:
            super = True
            resolver_super(tablero[MATRIX], token, line)
    tablero[PUNTAJE] += scoretable.score(len(line), super)
    if not super and len(line) >=  tablero[SUPER_LIMITE]:
        tablero[NEXT_SUPER] = random.randint(0, len(t.SUPERS) -1)
        

def resolver_super(matrix:list[list[dict]], token:dict, line:list[dict]):
    """Expande efecto de un token super.
    Args:
        matrix (list[list[dict]]): Matriz.
        token (dict): Token super.
        line (list[dict]): Tokens afectados.
    """
    match token[SUPER]:
        case t.BOMB:
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    agregar_super(matrix, pos_x(token) + x, pos_y(token) + y, line)
        case t.VERTICAL:
            for y in range(len(matrix[0])):
                agregar_super(matrix, pos_x(token), y, line)
        case t.HORIZONTAL:
            for x in range(len(matrix)):
                agregar_super(matrix, x, pos_y(token), line)
                        

def agregar_super(matrix:list[list[dict]], x:int, y:int, line:list[dict]):
    """Agrega un token afectado por super.
    Args:
        matrix (list[list[dict]]): Matriz.
        x (int): Fila.
        y (int): Columna.
        line (list[dict]): Tokens afectados.
    """
    target = safe_index(matrix, (x, y))
    if target and target not in line:
        line.append(target)


def agregar_eje_contrario(matrix:list[list[dict]], line:list[dict], es_horizontal:bool):
    """Busca matches perpendiculares adicionales.
    Args:
        matrix (list[list[dict]]): Matriz.
        line (list[dict]): Tokens principales.
        es_horizontal (bool): Si el match es horizontal.
    """
    sentido = SENTIDO_H
    if es_horizontal: 
        sentido = SENTIDO_V
    for token in line.copy():
        types = colores_con_match(matrix, pos_x(token), pos_y(token), sentido)
        if token[TYPE] in types:
            direcciones = [C_LEFT, C_RIGHT]
            if es_horizontal:
                direcciones = [C_DOWN, C_UP]
            for direccion in direcciones:
                for match in buscar(matrix, pos_x(token), pos_y(token), direccion, lambda a,b: comparar_tipo(a, b, token[TYPE])):
                    line.append(match)


def pos_x(token:dict) -> int:
    """Retorna la coordenada X del token.
    Args:
        token (dict): Token.
    Returns:
        int: Coordenada X.
    """
    return token[POSITION][0]


def pos_y(token:dict) -> int:
    """Retorna la coordenada Y del token.
    Args:
        token (dict): Token.
    Returns:
        int: Coordenada Y.
    """
    return token[POSITION][1]


def destroy(tablero:dict, scored:list[dict]):
    """Destruye tokens de un match.
    Args:
        tablero (dict): Datos del tablero.
        scored (list[dict]): Tokens a destruir.
    """
    set_as_busy(tablero, tablero[ANIM_SPEED])
    for token in scored:
        animations.destroy_token(token[GRAPHIC], tablero[ANIM_SPEED])
        move_to(tablero[MATRIX], None, token[POSITION])
        eventq.quitar_colision(token[COLISION])
        

def buscar_jugada(tablero:dict):
    """Busca jugadas posibles.
    Args:
        tablero (dict): Tablero.
    Returns:
        list[dict]: Tokens que permiten jugada.
    """
    if tablero[BUSY]:
        return
    matrix:list[list[dict]] = tablero[MATRIX]
    for x in range(len(matrix)):
        matching = buscar(matrix, x, 0, C_UP, lambda a,b: buscar_posibles(matrix, a, b))
        if len(matching) > 2:
            break
    if len(matching) < 3:
        for y in range(len(matrix[0])):
            matching = buscar(matrix, 0, y, C_RIGHT, lambda a,b: buscar_posibles(matrix, a, b))
            if len(matching) > 2:
                break
    return matching


def buscar(matrix:list[list[dict]], x:int, y:int, move:tuple[int, int], comparar):
    """Busca secuencia de tokens consecutivos bajo una condicion.
    Args:
        matrix (list[list[dict]]): Matriz.
        x (int): Fila inicial.
        y (int): Columna inicial.
        move (tuple[int,int]): Direccion.
        comparar (callable): Regla de comparacion.
    Returns:
        list[dict]: Tokens encontrados.
    """
    matching:list[dict] = []
    while in_bound(matrix, (x, y)):
        token = safe_index(matrix, (x, y))
        if not token:
            if len(matching) > 2:
                break
            else:
                matching.clear()
        elif not comparar(matching, token):
            break
        x += move[0]
        y += move[1]
    return matching


def comparar_tipo(validos:list[dict], token:dict, tipo:int) -> bool:
    """Compara un token por tipo.
    Args:
        validos (list[dict]): Tokens validos.
        token (dict): Token actual.
        tipo (int): Tipo requerido.
    Returns:
        bool: Si coincide.
    """
    iguales = token[TYPE] == tipo 
    if iguales:
        validos.append(token)
    return iguales


def buscar_3(validos:list[dict], token:dict) -> bool:
    """Regla para detectar secuencias de 3 iguales.
    Args:
        validos (list[dict]): Tokens acumulados.
        token (dict): Token actual.
    Returns:
        bool: Si continua la serie.
    """
    continuar = True
    if len(validos) == 0:
        validos.append(token)
    else:
        if validos[0][TYPE] == token[TYPE]:
            validos.append(token)
        else:
            if len(validos) > 2:
                continuar = False
            else:
                validos.clear()
                validos.append(token)
    return continuar


def buscar_posibles(matrix:list[list[dict]], validos:list[dict], token:dict) -> bool:
    """Evalua si un movimiento puede formar un match.
    Args:
        matrix (list[list[dict]]): Matriz.
        validos (list[dict]): Tokens acumulados.
        token (dict): Token actual.
    Returns:
        bool: Si debe seguir buscando.
    """
    validar:list[dict]|None = None
    pos = token[POSITION]
    if len(validos) == 0:
        validos.append(token)
    else:
        ref = validos[0]
        mov = sumar(pos, mult_escalar(ref[POSITION], -1))
        prox = safe_index(matrix, sumar(pos, mov))
        if token[TYPE] == ref[TYPE]:
            validos.append(token)
            validar = cardinals(matrix, sumar(pos, mov))
            validar.remove(token)
            posteriores = cardinals(matrix, sumar(ref[POSITION], mult_escalar(mov, -1)))
            if posteriores:
                posteriores.remove(ref)
                for posterior in posteriores:
                    validar.append(posterior)
        elif prox and ref[TYPE] == prox[TYPE]:
            validar = cardinals(matrix, pos, mov[0] == 1, mov[1] == 1) 
        else:
            validos.clear()
            validos.append(token)
    if validar:
        for cardinal in validar:
            if cardinal[TYPE] == validos[0][TYPE]:
                validos.append(cardinal)
                return False
        validos.clear()
        validos.append(token)
    return True


def pos(token:dict) -> tuple[int, int]:
    """Retorna coordenadas del token.
    Args:
        token (dict): Token.
    Returns:
        tuple[int,int]: Posicion.
    """
    return token[POSITION]


def sumar(pos1:tuple[int, int], pos2:tuple[int, int]):
    """Suma dos coordenadas.
    Args:
        pos1 (tuple[int,int]): Primer vector.
        pos2 (tuple[int,int]): Segundo vector.
    Returns:
        tuple[int,int]: Resultado.
    """
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def mult_escalar(pos:tuple[int, int], escalar:int):
    """Multiplica un vector por un escalar.
    Args:
        pos (tuple[int,int]): Vector.
        escalar (int): Escalar.
    Returns:
        tuple[int,int]: Resultado.
    """
    return (pos[0] * escalar, pos[1] * escalar)
             

def cardinals(matrix:list[list[dict]], xy:tuple[int, int], vertical:bool = False, horizontal:bool = False):
    """Obtiene vecinos cardinales del token.
    Args:
        matrix (list[list[dict]]): Matriz.
        xy (tuple[int,int]): Posicion.
        vertical (bool): Solo arriba/abajo.
        horizontal (bool): Solo izquierda/derecha.
    Returns:
        list[dict]: Vecinos.
    """
    res:list[dict] = list()
    directions = CARDINALS
    if horizontal:
        directions = [C_LEFT, C_RIGHT]
    elif vertical:
        directions = [C_UP, C_DOWN]
         
    for direction in directions:
        item = safe_index(matrix, sumar(xy, direction))
        if item:
            res.append(item)
    return res
                    

def in_bound(matrix:list[list[dict]], xy:tuple):
    """Verifica si una posicion esta dentro de la matriz.
    Args:
        matrix (list[list[dict]]): Matriz.
        xy (tuple[int,int]): Posicion.
    Returns:
        bool: Dentro del rango.
    """
    res = False
    if xy[0] < (len(matrix)) and xy[0] >= 0:
        row = matrix[xy[0]]
        res = xy[1] <(len(row)) and xy[1] >= 0
    return res


def safe_index(matrix:list[list[dict]], xy:tuple[int, int]):
    """Obtiene un elemento o None si esta fuera de rango.
    Args:
        matrix (list[list[dict]]): Matriz.
        xy (tuple[int,int]): Posicion buscada.
    Returns:
        dict|None: Token o None.
    """
    item = None
    if in_bound(matrix, xy):
        x, y = xy
        item = matrix[x][y]
    return item