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
    """Initialize mixer and load sounds/music."""
    pygame.mixer.init()
    _estado[SILENCIO] = False
    _estado[VOLUMEN] = 1.0
    
    _sonidos[PUNTAJE] = pygame.mixer.Sound("sounds/score.mp3")
    _sonidos[PUNTAJE_2] = pygame.mixer.Sound("sounds/score_3.mp3")
    _sonidos[PUNTAJE_SUPER] = pygame.mixer.Sound("sounds/score_6.mp3")
    _sonidos[MOVER] = pygame.mixer.Sound("sounds/move.mp3")
    _sonidos[MOVER_MAL] = pygame.mixer.Sound("sounds/wrong_move.mp3")
    _sonidos[CLICK] = pygame.mixer.Sound("sounds/click.mp3")
    _sonidos[FALLO] = pygame.mixer.Sound("sounds/fail.mp3")

MUSICA_MENU = 0
MUSICA_PARTIDA = 1
def reproducir_musica(track:int):
    """reproduce uno de los tracks de musica definidos en el modulo indefinidamente.

    Args:
        track (int): el numero de track a reporducir, los tracks disponibles son constantes del modulo de sonido.
    """
    if track == MUSICA_MENU:
        pygame.mixer.music.load("sounds/background.mp3")
    else:
        pygame.mixer.music.load("sounds/gaming_background.mp3")
    pygame.mixer.music.set_volume(volumen())
    pygame.mixer.music.play(-1)
    
def volumen():
    valor = 0
    if not _estado[SILENCIO]:
        valor = _estado[VOLUMEN]
    return valor

def silenciar():
    pygame.mixer.music.stop()

def sonido_puntaje(super: bool):
    if super:
        reproducir_sonido(PUNTAJE_SUPER)
    else:
        reproducir_sonido(PUNTAJE)
        
def reproducir_sonido(key:str):
    if key in _sonidos and not _estado[SILENCIO]:
        _sonidos[key].play()
        
def sonido_puntaje_nivel_2(super: bool):
    if super:
        reproducir_sonido(PUNTAJE_SUPER)
    else:
        reproducir_sonido(PUNTAJE_2)

def cambiar_volumen(vol: float):
    vol = max(0.0, min(vol, 1.0))
    _estado[VOLUMEN] = vol
    volumen_general(vol)

def mutear():
    _estado[SILENCIO] = True
    volumen_general(0)
        
def volumen_general(vol:float):
    for sonido in _sonidos.values():
        sonido.set_volume(vol)
    if not _estado[SILENCIO]:
        pygame.mixer.music.set_volume(vol)

def unmute():
    _estado[SILENCIO] = False
    volumen_general(_estado[VOLUMEN])
