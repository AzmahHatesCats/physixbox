import os
import pygame
import json

# Initialize pygame
pygame.init()

# Screen dimensions (fullscreen mode)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Physix Box")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
NAVY_BLUE = (2, 86, 166)
CYAN = (0, 191, 255)
PURPLE = (128, 0, 255)
PASTEL_PEACH = (245, 214, 206)
SKY_BLUE = (135, 206, 235)
ROYAL_BLUE = (65, 105, 225)
BUTTON_BORDER_BLUE = (0, 62, 128)
DEFAULT_COLOR = (245, 214, 206)
# Background color
BACKGROUND_COLOR = (245, 212, 203)  # RGB color for the background

# Default colors (can be customized)
try:
    with open("color_settings.json", "r") as f:
        color_data = json.load(f)
        CUBE_COLOR = tuple(color_data.get("cube_color", RED))
        CIRCLE_COLOR = tuple(color_data.get("circle_color", BLUE))
        BULLET_COLOR = tuple(color_data.get("bullet_color", WHITE))
except Exception:
    CUBE_COLOR = RED
    CIRCLE_COLOR = BLUE
    BULLET_COLOR = WHITE

COLOR_SETTINGS_FILE = "color_settings.json"

def save_color_settings(cube_color, circle_color, bullet_color):
    with open(COLOR_SETTINGS_FILE, "w") as f:
        json.dump({
            "cube_color": cube_color,
            "circle_color": circle_color,
            "bullet_color": bullet_color
        }, f)

def reload_colors():
    global CUBE_COLOR, CIRCLE_COLOR, BULLET_COLOR
    try:
        with open(COLOR_SETTINGS_FILE, "r") as f:
            color_data = json.load(f)
            CUBE_COLOR = tuple(color_data.get("cube_color", RED))
            CIRCLE_COLOR = tuple(color_data.get("circle_color", BLUE))
            BULLET_COLOR = tuple(color_data.get("bullet_color", WHITE))
    except Exception:
        CUBE_COLOR = RED
        CIRCLE_COLOR = BLUE
        BULLET_COLOR = WHITE

# Player and Bullet Constants
PLAYER_SIZE = 50  # Size of the player's cube
BULLET_RADIUS = 10  # Radius of the bullets
BULLET_SPEED = 10  # Speed of the bullets
COOLDOWN = 0.5  # Cooldown time for shooting (in seconds)
FRICTION = 0.85  # Adjusted from 0.9 to 0.85
# Fonts
FONT_PATH = os.path.join("assets", "fonts", "Inkfree.ttf")
HANDWRITTEN_FONT = pygame.font.Font(FONT_PATH, 33)

# Assets
BACKGROUND_IMAGE_PATH = os.path.join("assets", "images", "letsgo.png")

# Maximum distance between platforms (horizontal and vertical)
MAX_PLATFORM_DISTANCE = 300  # Adjust this value based on gameplay testing

# Flag icon (placeholder path, replace with actual flag icon when provided)
FLAG_ICON_PATH = os.path.join("assets", "images", "flag.png")

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Button offsets
BUTTON_HORIZONTAL_OFFSET = 100
BUTTON_VERTICAL_SPACING = 50

# Save file
SAVE_FILE = "save_data.json"  # File to store progress and settings