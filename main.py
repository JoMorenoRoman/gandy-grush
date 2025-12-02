import eventq
import pantallas.inicio
import ctypes

import sonido
import texto

try:
    import sys
    import pygame
    ctypes.windll.user32.SetProcessDPIAware()
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

def main():
    print("hello")
    
    pygame.init()
    pygame.font.init()
    texto.init()
    sonido.init()
    pygame.display.set_caption("Grandy Grush")
    
    pantallas.inicio.iniciar()
    eventq.start()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()