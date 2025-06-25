import pygame
from constants import PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GRAY, RED, screen, MAX_PLATFORM_DISTANCE, FLAG_ICON_PATH
import random

class Level:
    def __init__(self, number):
        self.number = number
        self.completed = False
        self.platforms = []  # List of platform rectangles
        self.flag = None  # Rectangle for the flag
        self.flag_icon = pygame.image.load(FLAG_ICON_PATH)  # Load the flag icon
        self.flag_icon = pygame.transform.scale(self.flag_icon, (30, 50))  # Resize the flag icon
        self.spawn_platform_index = 0
        self.flag_platform_index = 0
        self.create_level()

    def create_level(self):
        """Create fixed platforms and the flag for the level."""
        platform_height = 20
        platform_width = 150  # Default platform width

        # Start with the first platform at a random position near the bottom
        start_x = random.randint(50, SCREEN_WIDTH - platform_width - 50)
        start_y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 100)
        self.platforms.append(pygame.Rect(start_x, start_y, platform_width, platform_height))

        # Generate additional platforms
        for i in range(1, 5 + self.number):  # Increase platform count with level number
            prev_platform = self.platforms[-1]
            x = prev_platform.x + random.randint(-MAX_PLATFORM_DISTANCE, MAX_PLATFORM_DISTANCE)
            y = prev_platform.y - random.randint(50, MAX_PLATFORM_DISTANCE)

            # Ensure platforms stay within screen bounds
            x = max(50, min(x, SCREEN_WIDTH - platform_width - 50))
            y = max(50, min(y, SCREEN_HEIGHT - 100))

            # Ensure platforms are reachable diagonally and vertically
            if abs(x - prev_platform.x) > MAX_PLATFORM_DISTANCE or abs(y - prev_platform.y) > MAX_PLATFORM_DISTANCE:
                x = prev_platform.x + random.randint(-MAX_PLATFORM_DISTANCE // 2, MAX_PLATFORM_DISTANCE // 2)
                y = prev_platform.y - random.randint(50, MAX_PLATFORM_DISTANCE // 2)

            self.platforms.append(pygame.Rect(x, y, platform_width, platform_height))

        # Randomly select spawn and flag platforms (ensure they are not the same)
        platform_indices = list(range(len(self.platforms)))
        self.spawn_platform_index = random.choice(platform_indices)
        platform_indices.remove(self.spawn_platform_index)
        self.flag_platform_index = random.choice(platform_indices)

        # Place the flag at a position above the chosen platform
        flag_platform = self.platforms[self.flag_platform_index]
        self.flag = pygame.Rect(
            flag_platform.x + flag_platform.width // 2 - 15,
            flag_platform.y - 50,
            30, 50
        )

    def get_spawn_position(self):
        """Get the position of the spawn platform for player spawn."""
        if self.platforms:
            spawn_platform = self.platforms[self.spawn_platform_index]
            return spawn_platform.x + spawn_platform.width // 2, spawn_platform.y - PLAYER_SIZE // 2
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE  # Default spawn position if no platforms

    def draw(self):
        """Draw platforms and the flag."""
        for platform in self.platforms:
            pygame.draw.rect(screen, DARK_GRAY, platform)  # Draw platforms
        # Draw the flag icon
        screen.blit(self.flag_icon, (self.flag.x, self.flag.y))

    def check_completion(self, player):
        """Check if the player has reached the flag."""
        if self.flag.colliderect(pygame.Rect(player.x - PLAYER_SIZE // 2, player.y - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)):
            self.completed = True