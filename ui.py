import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)  # Smaller font size for the buttons
        self.button_width = 90
        self.button_height = 30
        self.button_color = (50, 50, 50)  # Button background color
        self.text_color = (255, 255, 255)  # Button text color
        self.hover_color = (70, 70, 70)  # Hover effect color

        # Set initial button positions based on screen size
        self.update_buttons(screen)

    def update_buttons(self, screen):
        """Update button positions based on the screen size."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Arrange buttons in one row at the bottom left
        self.buttons = {
            "Start": (10, screen_height - 40),
            "Pause": (10 + self.button_width + 10, screen_height - 40),  # 10 px gap between buttons
            "Reset": (10 + (self.button_width + 10) * 2, screen_height - 40),
            "Next Gen": (10 + (self.button_width + 10) * 3, screen_height - 40),
        }

    def draw_buttons(self):
        """Draw buttons on the screen."""
        for text, pos in self.buttons.items():
            rect = pygame.Rect(pos[0], pos[1], self.button_width, self.button_height)
            mouse_pos = pygame.mouse.get_pos()

            # Draw button background
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.hover_color, rect)
            else:
                pygame.draw.rect(self.screen, self.button_color, rect)

            # Draw button text
            label = self.font.render(text, True, self.text_color)
            self.screen.blit(label, (pos[0] + 10, pos[1] + 5))

    def handle_event(self, event, simulation):
        """Handle button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for text, pos in self.buttons.items():
                rect = pygame.Rect(pos[0], pos[1], self.button_width, self.button_height)
                if rect.collidepoint(x, y):
                    if text == "Start":
                        simulation.start()
                    elif text == "Pause":
                        simulation.pause()
                    elif text == "Reset":
                        simulation.reset(self.screen)
                    elif text == "Next Gen":
                        simulation.next_generation()
