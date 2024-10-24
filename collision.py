import pygame

class CollisionObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 0, 0)  # Red color for collision objects

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, pixy):
        # Check if the pixy's rectangle collides with this collision object
        return (self.x < pixy.x < self.x + self.width and
                self.y < pixy.y < self.y + self.height)
