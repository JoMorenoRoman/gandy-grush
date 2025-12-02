import pygame

_sonidos:dict[str, pygame.mixer.Sound] = {}
PUNTAJE = "score"
PUNTAJE_2 = "score_3"
PUNTAJE_SUPER = "score_6"
MOVER = "move"
MOVER_MAL = "wrong_move"
CLICK = "click"
FALLO = "fail"

_estado = {}
SILENCIO = "silencio"
VOLUMEN = "volumen"

def init():
    """
    Inicializa el sistema de sonido y carga los efectos y música.

        - Inicializa el mezclador de audio (`pygame.mixer.init()`).
        - Configura el estado inicial: sonido activo y volumen en 1.0.
        - Carga los efectos de sonido desde la carpeta 'sonidos/' y los almacena en `_sonidos`.
    """
    pygame.mixer.init()
    _estado[SILENCIO] = False
    _estado[VOLUMEN] = 1.0
    
    _sonidos[PUNTAJE] = pygame.mixer.Sound("sonidos/score.mp3")
    _sonidos[PUNTAJE_2] = pygame.mixer.Sound("sonidos/score_3.mp3")
    _sonidos[PUNTAJE_SUPER] = pygame.mixer.Sound("sonidos/score_6.mp3")
    _sonidos[MOVER] = pygame.mixer.Sound("sonidos/move.mp3")
    _sonidos[MOVER_MAL] = pygame.mixer.Sound("sonidos/wrong_move.mp3")
    _sonidos[CLICK] = pygame.mixer.Sound("sonidos/click.mp3")
    _sonidos[FALLO] = pygame.mixer.Sound("sonidos/fail.mp3")

MUSICA_MENU = 0
MUSICA_PARTIDA = 1
def reproducir_musica(track:int):
    """reproduce uno de los tracks de musica definidos en el modulo indefinidamente.

    Args:
        track (int): el numero de track a reporducir, los tracks disponibles son constantes del modulo de sonido.
    """
    if track == MUSICA_MENU:
        pygame.mixer.music.load("sonidos/background.mp3")
    else:
        pygame.mixer.music.load("sonidos/gaming_background.mp3")
    pygame.mixer.music.set_volume(volumen())
    pygame.mixer.music.play(-1)
    
def volumen():
    """
    Obtiene el volumen actual del sistema de sonido.

    Returns:
        float: Valor entre 0.0 y 1.0. Si está silenciado, retorna 0.
    """
    valor = 0
    if not _estado[SILENCIO]:
        valor = _estado[VOLUMEN]
    return valor

def silenciar():
    """
    Detiene la música en reproducción.
    """
    pygame.mixer.music.stop()

def sonido_puntaje(super: bool):
    """
    Reproduce el sonido de puntaje normal o super puntaje.

    Args:
        super (bool): Si es True, reproduce el sonido de puntaje especial.
    """
    if super:
        reproducir_sonido(PUNTAJE_SUPER)
    else:
        reproducir_sonido(PUNTAJE)
        
def reproducir_sonido(key:str):
    """
    Reproduce un efecto de sonido específico si no está silenciado.

    Args:
        key (str): Clave del sonido en el diccionario `_sonidos`.
    """
    if key in _sonidos and not _estado[SILENCIO]:
        _sonidos[key].play()
        
def sonido_puntaje_nivel_2(super: bool):
    """
    Reproduce el sonido de puntaje para nivel 2 (normal o super).

    Args:
        super (bool): Si es True, reproduce el sonido de puntaje especial.
    """
    if super:
        reproducir_sonido(PUNTAJE_SUPER)
    else:
        reproducir_sonido(PUNTAJE_2)

def cambiar_volumen(vol: float):
    """
    Cambia el volumen general del sistema de sonido.

    Args:
        vol (float): Nuevo volumen entre 0.0 y 1.0.
    """
    vol = max(0.0, min(vol, 1.0))
    _estado[VOLUMEN] = vol
    volumen_general(vol)

def mutear():
    """
    Activa el modo silencio (mute) y ajusta el volumen a 0.
    """
    _estado[SILENCIO] = True
    volumen_general(0)
        
def volumen_general(vol:float):
    """
    Ajusta el volumen de todos los sonidos y música.

    Args:
        vol (float): Valor entre 0.0 y 1.0.
    """
    for sonido in _sonidos.values():
        sonido.set_volume(vol)
    if not _estado[SILENCIO]:
        pygame.mixer.music.set_volume(vol)

def unmute():
    """
    Desactiva el modo silencio y restaura el volumen anterior.
    """
    _estado[SILENCIO] = False
    volumen_general(_estado[VOLUMEN])
