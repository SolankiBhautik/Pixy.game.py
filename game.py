import pygame
import sys
from config import WIDTH, HEIGHT
from simulation import Simulation
from ui import UI

# Initialize Pygame
pygame.init()

# Set default window dimensions and make it resizable
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Initialize Simulation and UI
simulation = Simulation(screen)
ui = UI(screen)

# Fullscreen flag
fullscreen = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle resizing the window
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            ui.update_buttons(screen)  # Update button positions based on new screen size

        # Toggle fullscreen on F11 key press
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if fullscreen:
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                fullscreen = False
            else:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                fullscreen = True

        # Pass event to UI for handling
        ui.handle_event(event, simulation)

    # Update simulation state
    simulation.update()

    # Draw everything
    screen.fill((0, 0, 0))
    for pixy in simulation.population:
        pixy.draw(screen)

    # Draw generation indicator and UI buttons
    font = pygame.font.Font(None, 36)
    text = font.render(f"Generation: {simulation.generation}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    ui.draw_buttons()

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)
