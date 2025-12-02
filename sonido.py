import pygame

_sounds = {}
_muted = False
_volume = 1.0 

def init():
    """Initialize mixer and load sounds/music."""
    pygame.mixer.init()

    _sounds["score"] = pygame.mixer.Sound("sounds/score.mp3")
    _sounds["score_3"] = pygame.mixer.Sound("sounds/score_3.mp3")
    _sounds["score_6"] = pygame.mixer.Sound("sounds/score_6.mp3")
    _sounds["move"] = pygame.mixer.Sound("sounds/move.mp3")
    _sounds["wrong_move"] = pygame.mixer.Sound("sounds/wrong_move.mp3")
    _sounds["click"] = pygame.mixer.Sound("sounds/click.mp3")
    _sounds["fail"] = pygame.mixer.Sound("sounds/fail.mp3")
    
    for s in _sounds.values():
        s.set_volume(_volume)

def reproducir_musica_de_juego():
    """Play music track in a loop."""
    pygame.mixer.music.load("sounds/gaming_background.mp3")
    pygame.mixer.music.set_volume(_volume if not _muted else 0)
    pygame.mixer.music.play(-1)  # Loop forever

def reproducir_musica_de_menu():
    """Play music track in a loop."""
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.set_volume(_volume if not _muted else 0)
    pygame.mixer.music.play(-1)  # Loop forever

def silenciar():
    """Stop the currently playing music."""
    pygame.mixer.music.stop()

def sonido_puntaje(isSuper: bool):
    """Play scoring sound once."""
    if isSuper and "score" in _sounds and not _muted:
        _sounds["score_6"].play()
    if "score" in _sounds and not _muted:
        _sounds["score"].play()

def sonido_puntaje_nivel_2(isSuper: bool):
    """Play scoring sound once."""
    if isSuper and "score" in _sounds and not _muted:
        _sounds["score_6"].play()
    if "score" in _sounds and not _muted:
        _sounds["score_3"].play()

def sonido_efecto(nombre: str):
    """Play a short sound effect (e.g., move or click)."""
    if nombre in _sounds and not _muted:
        _sounds[nombre].play()

def set_volume(vol: float):
    """Set global volume (0.0 to 1.0)."""
    global _volume
    _volume = max(0.0, min(vol, 1.0))  # Clamp between 0 and 1
    pygame.mixer.music.set_volume(_volume if not _muted else 0)
    for s in _sounds.values():
        s.set_volume(_volume)

def mute():
    """Mute all sounds and music."""
    global _muted
    _muted = True
    pygame.mixer.music.set_volume(0)
    for s in _sounds.values():
        s.set_volume(0)

def unmute():
    """Unmute all sounds and restore volume."""
    global _muted
    _muted = False
    pygame.mixer.music.set_volume(_volume)
    for s in _sounds.values():
        s.set_volume(_volume)
