import eventq
import pantallas.inicio
import config
import display
import ctypes

try:
    import sys
    import pygame
    ctypes.windll.user32.SetProcessDPIAware()
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

def main():
    print("hello")
    
    # Initialise screen
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Grandy Grush")
    
    config.font = pygame.font.Font(None, display.text_height())
    pantallas.inicio.iniciar()
    eventq.start()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()