import pygame
import sys
import config

# Initialize Pygame
pygame.init()

# Set up the display

WINDOW = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Gandy Grush")

# Define colors


# Set up a clock for frame rate
clock = pygame.time.Clock()

# Define a player (a moving rectangle)
player_pos = [config.WIDTH // 2, config.HEIGHT // 2]
player_speed = 5

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Draw everything
    WINDOW.fill(config.BACKGROUND)
    pygame.draw.rect(WINDOW, config.MAINCOLOR, (*player_pos, 50, 50))  # (x, y, width, height)
    
    # Update display
    pygame.display.flip()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
