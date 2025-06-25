import pygame
import math
from constants import PLAYER_SIZE, BULLET_SPEED, COOLDOWN, FRICTION, screen, CUBE_COLOR, CIRCLE_COLOR, BULLET_COLOR
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = CUBE_COLOR
        self.angle = 0
        self.cooldown_timer = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.circle_radius = PLAYER_SIZE // 4  # Initial radius of the circle inside the player
        self.circle_color = CIRCLE_COLOR

    def draw(self):
        # Draw the rotating cube
        cube_surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(cube_surface, self.color, (0, 0, PLAYER_SIZE, PLAYER_SIZE))
        rotated_cube = pygame.transform.rotate(cube_surface, self.angle)
        cube_rect = rotated_cube.get_rect(center=(self.x, self.y))
        screen.blit(rotated_cube, cube_rect.topleft)

        # Draw the regenerating circle inside the cube
        pygame.draw.circle(screen, self.circle_color, (int(self.x), int(self.y)), self.circle_radius)

    def shoot(self, mouse_pos, bullets):
        if self.cooldown_timer <= 0:
            # Calculate direction and power
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            power = min(distance / 80, 3.0)  # Increase power scaling (was 100, now 80)

            # Normalize direction
            direction_x = dx / distance
            direction_y = dy / distance

            # Create a bullet with the current circle radius
            bullets.append(Bullet(self.x, self.y, direction_x * BULLET_SPEED * power, direction_y * BULLET_SPEED * power, self.circle_radius, BULLET_COLOR))

            # Apply recoil to the player
            self.velocity_x -= direction_x * power * 10  # Increased recoil multiplier
            self.velocity_y -= direction_y * power * 10  # Increased recoil multiplier

            # Apply rotation
            self.angle += power * 40  # Increased rotation effect

            # Shrink the circle to simulate firing
            self.circle_radius = 0

            # Reset cooldown
            self.cooldown_timer = COOLDOWN

    def update(self, dt, platforms):
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Apply gravity
        self.velocity_y += 0.5  # Gravity strength

        # Check for collisions with platforms
        player_rect = pygame.Rect(self.x - PLAYER_SIZE // 2, self.y - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
        for platform in platforms:
            if player_rect.colliderect(platform):
                # Land on the platform
                if self.velocity_y > 0:  # Falling
                    self.y = platform.top - PLAYER_SIZE // 2
                    self.velocity_y = 0

        # Apply friction
        self.velocity_x *= FRICTION

        # Update cooldown timer and regenerate the circle
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
            # Regenerate the circle based on the cooldown progress
            self.circle_radius = int((1 - self.cooldown_timer / COOLDOWN) * (PLAYER_SIZE // 4))
        else:
            self.cooldown_timer = 0
            self.circle_radius = PLAYER_SIZE // 4  # Fully regenerate the circle

    def reset(self, x, y):
        """Reset the player's position and velocity."""
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 0
        self.cooldown_timer = 0  # Reset cooldown