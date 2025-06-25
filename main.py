import pygame
import sys
import json  # For saving and loading progress
from constants import *
from menus import main_menu, level_menu, retry_menu, settings_menu  # Import settings_menu
from level import Level
from player import Player
from bullet import Bullet
from constants import reload_colors

SAVE_FILE = "save_data.json"  # File to store progress

def save_progress(current_level, unlocked_levels):
    """Save the current level and unlocked levels to a file."""
    save_data = {
        "current_level": current_level,
        "unlocked_levels": unlocked_levels
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(save_data, file)

def load_progress():
    """Load the saved progress from a file."""
    try:
        with open(SAVE_FILE, "r") as file:
            save_data = json.load(file)
            return save_data["current_level"], save_data["unlocked_levels"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # If the save file doesn't exist or is corrupted, start fresh
        return 0, 1  # Default to level 1 unlocked

def load_save_file():
    """Display a file selection menu to load a save file."""
    import tkinter as tk
    from tkinter import filedialog

    # Use Tkinter to open a file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Save File",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    root.destroy()  # Destroy the tkinter root window

    if file_path:
        try:
            with open(file_path, "r") as file:
                save_data = json.load(file)
                return save_data["current_level"], save_data["unlocked_levels"]
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("Invalid save file.")
    return None, None  # Return None if no file is selected or invalid

def has_save_file():
    """Check if a save file exists."""
    try:
        with open(SAVE_FILE, "r") as file:
            json.load(file)
            return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False

def apply_current_colors(player):
    player.color = CUBE_COLOR
    player.circle_color = CIRCLE_COLOR

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Initialize player and bullets
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    bullets = []

    # Load progress
    current_level, unlocked_levels = load_progress()

    # Ensure enough levels are loaded for the current progress
    levels = [Level(i + 1) for i in range(max(current_level + 1, 1))]

    show_continue = has_save_file()
    while True:
        # Show the main menu and get the selected action
        menu_action = main_menu(show_continue)
        if menu_action == "NEW_GAME":
            # Start a new game
            current_level = 0
            unlocked_levels = 1
            levels = [Level(1)]  # Reset levels to start fresh
            run_game(player, bullets, levels, current_level, unlocked_levels, BULLET_COLOR)
            show_continue = True  # Now show CONTINUE button
        elif menu_action == "CONTINUE":
            # Reload progress from save file
            current_level, unlocked_levels = load_progress()
            reload_colors()  # Reload colors
            apply_current_colors(player)
            levels = [Level(i + 1) for i in range(max(current_level + 1, 1))]
            run_game(player, bullets, levels, current_level, unlocked_levels, BULLET_COLOR)
        elif menu_action == "SETTINGS":
            # Open the settings menu and pass the player
            settings_menu(player)
        elif menu_action == "EXIT":
            pygame.quit()
            sys.exit()

def run_game(player, bullets, levels, current_level, unlocked_levels, bullet_color):
    """Run the game loop for the current level."""
    clock = pygame.time.Clock()
    running = True

    # Load the home icon
    home_icon = pygame.image.load("assets/images/home.png")
    home_icon = pygame.transform.scale(home_icon, (50, 50))

    # Spawn the player on the topmost platform
    spawn_x, spawn_y = levels[current_level].get_spawn_position()
    player.reset(spawn_x, spawn_y)

    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save progress before quitting
                save_progress(current_level, unlocked_levels)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.shoot(pygame.mouse.get_pos(), bullets)

        # Update game objects
        player.update(dt, levels[current_level].platforms)
        for bullet in bullets:
            bullet.update()

        # Check if the player falls below the screen
        if player.y > SCREEN_HEIGHT + 200:  # If the player falls too far
            retry = retry_menu()
            if retry:
                # Retry the current level
                spawn_x, spawn_y = levels[current_level].get_spawn_position()
                player.reset(spawn_x, spawn_y)
                bullets.clear()
            else:
                # Save progress and exit to the main menu
                save_progress(current_level, unlocked_levels)
                return

        # Check level completion
        levels[current_level].check_completion(player)
        if levels[current_level].completed:
            unlocked_levels = max(unlocked_levels, current_level + 2)  # Unlock the next level
            current_level += 1

            # Dynamically generate a new level if it doesn't exist
            if current_level >= len(levels):
                levels.append(Level(current_level + 1))  # Create a new level dynamically

            # Reset player and bullets for the next level
            spawn_x, spawn_y = levels[current_level].get_spawn_position()
            player.reset(spawn_x, spawn_y)
            bullets.clear()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)  # Use the constant background color
        levels[current_level].draw()
        player.draw()
        for bullet in bullets:
            bullet.draw(screen)

        # Draw level counter
        level_counter_text = HANDWRITTEN_FONT.render(f"Level: {current_level + 1}", True, WHITE)
        screen.blit(level_counter_text, (SCREEN_WIDTH - level_counter_text.get_width() - 20, 20))

        # Draw home icon
        home_icon_rect = pygame.Rect(10, 10, 50, 50)
        screen.blit(home_icon, home_icon_rect.topleft)
        if home_icon_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            # Save progress and return to the main menu
            save_progress(current_level, unlocked_levels)
            return

        pygame.display.flip()

if __name__ == "__main__":
    main()