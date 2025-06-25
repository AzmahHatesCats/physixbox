import pygame
from constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    def __init__(self, x, y, vx, vy, radius, color):
        """
        Initialize a bullet with its position, velocity, and size.
        :param x: Initial x-coordinate of the bullet.
        :param y: Initial y-coordinate of the bullet.
        :param vx: Velocity in the x-direction.
        :param vy: Velocity in the y-direction.
        :param radius: Radius of the bullet (inherited from the player's circle).
        :param color: Color of the bullet.
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def draw(self, screen):
        """
        Draw the bullet on the screen.
        :param screen: The pygame screen surface.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        """
        Update the bullet's position based on its velocity.
        Remove the bullet if it goes off-screen.
        """
        self.x += self.vx
        self.y += self.vy

        # Remove the bullet if it goes off-screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False  # Indicate that the bullet should be removed
        return True