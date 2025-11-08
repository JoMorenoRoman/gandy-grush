from events import EventQueue


try:
    import sys
    import pygame
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

def main():
    print("hello")
        # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Basic Pong")
    
        # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    events = EventQueue()
    events.start()

if __name__ == "__main__":
    main()