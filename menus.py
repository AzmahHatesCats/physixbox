import pygame
import sys
import json
from constants import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_COLOR
from constants import DARK_GRAY
from constants import BUTTON_BORDER_BLUE, BACKGROUND_IMAGE_PATH
from constants import HANDWRITTEN_FONT, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, WHITE, NAVY_BLUE, SKY_BLUE, ROYAL_BLUE, CYAN, PURPLE, RED
import constants
import tkinter as tk
from tkinter import colorchooser
from constants import save_color_settings, CUBE_COLOR, CIRCLE_COLOR, BULLET_COLOR, reload_colors

def draw_button(screen, text, font, bg_color, text_color, rect, border_color=None, is_hovered=False, is_clicked=False):
    shadow_offset = 5
    shadow_color = (50, 50, 50)
    # Shadow
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=20)
    # Animate color
    color = bg_color
    if is_clicked:
        color = tuple(max(0, c - 40) for c in bg_color)
    elif is_hovered:
        color = tuple(min(255, c + 30) for c in bg_color)
    pygame.draw.rect(screen, color, rect, border_radius=20)
    if border_color:
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=20)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_slider(screen, x, y, value, label, color, is_active=False):
    """Draws a horizontal slider and returns the new value if dragged."""
    slider_rect = pygame.Rect(x, y, 200, 10)
    knob_x = x + int((value / 255) * 200)
    knob_rect = pygame.Rect(knob_x - 8, y - 6, 16, 22)
    # Draw label
    font = HANDWRITTEN_FONT
    label_surf = font.render(f"{label}: {value}", True, color)
    screen.blit(label_surf, (x - 120, y - 8))
    # Draw slider bar
    pygame.draw.rect(screen, (180, 180, 180), slider_rect, border_radius=5)
    # Draw knob
    knob_color = tuple(min(255, c + 40) if is_active else c for c in color)
    pygame.draw.rect(screen, knob_color, knob_rect, border_radius=8)
    return slider_rect, knob_rect

def main_menu(show_continue=None):
    """Display the main menu."""
    clock = pygame.time.Clock()

    # Load the background image for the main menu
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Define buttons (aligned to the right side of the screen)
    button_width = 300
    button_height = 80
    button_gap = 20
    start_y = SCREEN_HEIGHT // 3  # Start higher on the screen
    start_x = SCREEN_WIDTH - button_width - 50  # Align to the right side with padding

    # Only show CONTINUE if save exists or after new game
    buttons = [
        {"rect": pygame.Rect(start_x, start_y, button_width, button_height), "text": "NEW GAME", "bg_color": NAVY_BLUE, "border_color": BUTTON_BORDER_BLUE},
    ]
    y_offset = button_height + button_gap

    if show_continue is None:
        show_continue = has_save_file()
    if show_continue:
        buttons.append({"rect": pygame.Rect(start_x, start_y + y_offset, button_width, button_height), "text": "CONTINUE", "bg_color": SKY_BLUE, "border_color": None})
        y_offset += button_height + button_gap

    # Only add SETTINGS and EXIT
    buttons += [
        {"rect": pygame.Rect(start_x, start_y + y_offset, button_width, button_height), "text": "SETTINGS", "bg_color": PURPLE, "border_color": None},
        {"rect": pygame.Rect(start_x, start_y + y_offset + button_height + button_gap, button_width, button_height), "text": "EXIT", "bg_color": RED, "border_color": None},
    ]

    while True:
        # Draw the background image
        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["text"] == "NEW GAME":
                            return "NEW_GAME"
                        elif button["text"] == "CONTINUE":
                            return "CONTINUE"
                        elif button["text"] == "SETTINGS":
                            return "SETTINGS"
                        elif button["text"] == "EXIT":
                            pygame.quit()
                            sys.exit()

        for button in buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            is_clicked = mouse_pressed[0] and is_hovered
            draw_button(screen, button["text"], HANDWRITTEN_FONT, button["bg_color"], WHITE, button["rect"], button["border_color"], is_hovered, is_clicked)

        pygame.display.flip()
        clock.tick(60)

def level_menu(unlocked_levels):
    """Display the level selection menu."""
    clock = pygame.time.Clock()

    # Button dimensions
    button_width = 150
    button_height = 50
    button_gap = 20
    start_x = (SCREEN_WIDTH - (button_width + button_gap) * 5) // 2
    start_y = SCREEN_HEIGHT // 3

    while True:
        screen.fill(BACKGROUND_COLOR)  # Use the constant background color
        title_text = HANDWRITTEN_FONT.render("Level Menu", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw level buttons
        buttons = []
        for i in range(1, 51):  # 50 levels
            col = (i - 1) % 5
            row = (i - 1) // 5
            x = start_x + col * (button_width + button_gap)
            y = start_y + row * (button_height + button_gap)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((rect, i))

            # Check if the level is unlocked
            if i <= unlocked_levels:
                pygame.draw.rect(screen, SKY_BLUE, rect, border_radius=10)
                level_text = HANDWRITTEN_FONT.render(f"Level {i}", True, WHITE)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=10)
                level_text = HANDWRITTEN_FONT.render(f"Locked", True, WHITE)

            text_rect = level_text.get_rect(center=rect.center)
            screen.blit(level_text, text_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, level in buttons:
                    if rect.collidepoint(mouse_pos) and level <= unlocked_levels:
                        return level  # Return the selected level

        pygame.display.flip()
        clock.tick(60)

def retry_menu():
    """Display a retry menu when the player falls too far."""
    clock = pygame.time.Clock()
    font = HANDWRITTEN_FONT  # Use Inkfree.ttf for consistency

    # Define buttons
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)

    while True:
        screen.fill(BACKGROUND_COLOR)  # Use the constant background color
        title_text = font.render("You Fell! Retry?", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Retry button
        retry_hovered = retry_button.collidepoint(mouse_pos)
        draw_button(screen, "Retry", HANDWRITTEN_FONT, NAVY_BLUE, WHITE, retry_button, BUTTON_BORDER_BLUE, retry_hovered, mouse_pressed[0])

        # Main menu button
        main_menu_hovered = main_menu_button.collidepoint(mouse_pos)
        draw_button(screen, "Main Menu", HANDWRITTEN_FONT, PURPLE, WHITE, main_menu_button, BUTTON_BORDER_BLUE, main_menu_hovered, mouse_pressed[0])

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if retry_button.collidepoint(mouse_pos):
                        return True  # Retry the current level
                    elif main_menu_button.collidepoint(mouse_pos):
                        return False  # Return to the main menu

        pygame.display.flip()
        clock.tick(60)

def settings_menu(player=None):
    clock = pygame.time.Clock()
    font = HANDWRITTEN_FONT
    customize_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)
    back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 60)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if customize_btn.collidepoint(mouse):
                    customization_menu(player)
                elif back_btn.collidepoint(mouse):
                    return

        screen.fill(BACKGROUND_COLOR)
        title = font.render("Settings", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        draw_button(screen, "Customize Colors", font, CYAN, WHITE, customize_btn, border_color=BUTTON_BORDER_BLUE, is_hovered=customize_btn.collidepoint(mouse), is_clicked=customize_btn.collidepoint(mouse) and click)
        draw_button(screen, "Back", font, DARK_GRAY, WHITE, back_btn, border_color=BUTTON_BORDER_BLUE, is_hovered=back_btn.collidepoint(mouse), is_clicked=back_btn.collidepoint(mouse) and click)
        pygame.display.flip()
        clock.tick(60)

def customization_tool():
    """Display the customization tool to change cube and bullet colors using Tkinter."""
    import tkinter as tk
    from tkinter import colorchooser

    # Load saved colors or use defaults
    try:
        with open(SAVE_FILE, "r") as file:
            save_data = json.load(file)
            cube_color = tuple(save_data.get("cube_color", RED))
            bullet_color = tuple(save_data.get("bullet_color", WHITE))
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        cube_color = RED
        bullet_color = WHITE

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Customization Tool")
    root.geometry("400x300")
    root.resizable(False, False)

    # Function to choose a color for the cube
    def choose_cube_color():
        nonlocal cube_color
        color_code = colorchooser.askcolor(title="Choose Cube Color")[0]
        if color_code:
            cube_color = tuple(map(int, color_code))
            cube_color_label.config(bg=_rgb_to_hex(cube_color))

    # Function to choose a color for the bullet
    def choose_bullet_color():
        nonlocal bullet_color
        color_code = colorchooser.askcolor(title="Choose Bullet Color")[0]
        if color_code:
            bullet_color = tuple(map(int, color_code))
            bullet_color_label.config(bg=_rgb_to_hex(bullet_color))

    # Function to save the selected colors
    def save_colors():
        try:
            with open(SAVE_FILE, "r") as file:
                save_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            save_data = {}

        save_data["cube_color"] = cube_color
        save_data["bullet_color"] = bullet_color

        with open(SAVE_FILE, "w") as file:
            json.dump(save_data, file)

        root.destroy()  # Close the Tkinter window

    # Helper function to convert RGB to HEX
    def _rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    # Cube color selection
    tk.Label(root, text="Cube Color:", font=("Arial", 14)).pack(pady=10)
    cube_color_label = tk.Label(root, bg=_rgb_to_hex(cube_color), width=20, height=2)
    cube_color_label.pack(pady=5)
    tk.Button(root, text="Choose Cube Color", command=choose_cube_color).pack(pady=5)

    # Bullet color selection
    tk.Label(root, text="Bullet Color:", font=("Arial", 14)).pack(pady=10)
    bullet_color_label = tk.Label(root, bg=_rgb_to_hex(bullet_color), width=20, height=2)
    bullet_color_label.pack(pady=5)
    tk.Button(root, text="Choose Bullet Color", command=choose_bullet_color).pack(pady=5)

    # Save button
    tk.Button(root, text="Save and Exit", command=save_colors, bg="green", fg="white").pack(pady=20)

    # Run the Tkinter main loop
    root.mainloop()

def color_picker():
    """Open a color picker dialog to select a color."""
    import tkinter as tk
    from tkinter import colorchooser

    # Pause pygame while using tkinter
    pygame.display.iconify()  # Minimize the pygame window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    color_code = colorchooser.askcolor(title="Choose a color")[0]  # Returns (R, G, B)
    root.destroy()  # Destroy the tkinter root window
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Restore pygame window

    if color_code:
        return tuple(map(int, color_code))  # Convert to integer RGB tuple
    return DEFAULT_COLOR  # Use the imported constant directly

def customization_menu(player=None):
    clock = pygame.time.Clock()
    font = HANDWRITTEN_FONT

    # Load current colors
    cube_color = list(CUBE_COLOR)
    circle_color = list(CIRCLE_COLOR)
    bullet_color = list(BULLET_COLOR)

    # Button rects
    save_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, 600, 300, 60)
    back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 150, 680, 300, 60)

    # Load checkmark image
    checkmark_img = pygame.image.load("assets/images/green.png")
    checkmark_img = pygame.transform.scale(checkmark_img, (40, 40))

    # Slider state
    dragging = None  # (color_type, channel)
    show_checkmark = False
    checkmark_time = 0

    disclaimer_text = "For changes to take effect, the game need to be restarted!"
    disclaimer_font = HANDWRITTEN_FONT
    disclaimer_height = 50
    disclaimer_rect = pygame.Rect(0, 0, SCREEN_WIDTH, disclaimer_height)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check sliders
                for idx, (label, color, arr) in enumerate([
                    ("Cube", (255, 80, 80), cube_color),
                    ("Circle", (80, 160, 255), circle_color),
                    ("Bullet", (255, 255, 80), bullet_color)
                ]):
                    for ch, ch_label in enumerate(["R", "G", "B"]):
                        sx = SCREEN_WIDTH // 2 - 20
                        sy = 220 + idx * 120 + ch * 30
                        _, knob_rect = draw_slider(screen, sx, sy, arr[ch], ch_label, color)
                        if knob_rect.collidepoint(mouse):
                            dragging = (idx, ch)
                # Check buttons
                if save_btn.collidepoint(mouse):
                    save_color_settings(cube_color, circle_color, bullet_color)
                    reload_colors()  # Reload colors from file
                    # Update the player colors if player is provided
                    if player is not None:
                        player.color = CUBE_COLOR
                        player.circle_color = CIRCLE_COLOR
                        # Update all bullets' color if you have access to the bullets list
                        if hasattr(player, 'bullets'):
                            for bullet in player.bullets:
                                bullet.color = BULLET_COLOR
                    show_checkmark = True
                    checkmark_time = pygame.time.get_ticks()
                elif back_btn.collidepoint(mouse):
                    return
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None
            elif event.type == pygame.MOUSEMOTION and dragging and click:
                idx, ch = dragging
                sx = SCREEN_WIDTH // 2 - 20
                mx = mouse[0]
                # Clamp mouse x to slider range
                rel = min(200, max(0, mx - sx))
                val = int((rel / 200) * 255)
                if idx == 0:
                    cube_color[ch] = val
                elif idx == 1:
                    circle_color[ch] = val
                elif idx == 2:
                    bullet_color[ch] = val

        # Hide checkmark after 5 seconds
        if show_checkmark and pygame.time.get_ticks() - checkmark_time > 5000:
            show_checkmark = False

        screen.fill(BACKGROUND_COLOR)
        title = font.render("Customize Colors", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Draw disclaimer at the top
        pygame.draw.rect(screen, (0, 0, 0), disclaimer_rect)
        text_surface = disclaimer_font.render(disclaimer_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, disclaimer_height // 2))
        screen.blit(text_surface, text_rect)

        # Draw color previews and sliders
        for idx, (label, color, arr) in enumerate([
            ("Cube", (255, 80, 80), cube_color),
            ("Circle", (80, 160, 255), circle_color),
            ("Bullet", (255, 255, 80), bullet_color)
        ]):
            pygame.draw.rect(screen, arr, (SCREEN_WIDTH // 2 + 200, 210 + idx * 120, 60, 60), border_radius=12)
            label_surf = font.render(label, True, color)
            screen.blit(label_surf, (SCREEN_WIDTH // 2 - 320, 220 + idx * 120))
            for ch, ch_label in enumerate(["R", "G", "B"]):
                sx = SCREEN_WIDTH // 2 - 20
                sy = 220 + idx * 120 + ch * 30
                is_active = dragging == (idx, ch)
                draw_slider(screen, sx, sy, arr[ch], ch_label, color, is_active=is_active)

        # Draw buttons with animation
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        draw_button(screen, "Save", font, ROYAL_BLUE, WHITE, save_btn, border_color=BUTTON_BORDER_BLUE, is_hovered=save_btn.collidepoint(mouse), is_clicked=save_btn.collidepoint(mouse) and click)
        draw_button(screen, "Back", font, DARK_GRAY, WHITE, back_btn, border_color=BUTTON_BORDER_BLUE, is_hovered=back_btn.collidepoint(mouse), is_clicked=back_btn.collidepoint(mouse) and click)

        # Draw checkmark if needed
        if show_checkmark:
            checkmark_x = save_btn.right + 10
            checkmark_y = save_btn.centery - 20
            screen.blit(checkmark_img, (checkmark_x, checkmark_y))

        pygame.display.flip()

        # After showing checkmark for 1 second, restart the game
        if show_checkmark and pygame.time.get_ticks() - checkmark_time > 300:
            pygame.quit()
            os.execl(sys.executable, sys.executable, *sys.argv)

        clock.tick(60)

import os

def color_picker_menu(current_color):
    """A simple color picker using a palette image."""
    palette_path = os.path.join("assets", "images", "palette.png")
    palette = pygame.image.load(palette_path)
    palette = pygame.transform.scale(palette, (300, 200))
    palette_rect = palette.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

    running = True
    selected_color = current_color
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return current_color
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (palette_rect.collidepoint(event.pos)):
                    rel_x = event.pos[0] - palette_rect.x
                    rel_y = event.pos[1] - palette_rect.y
                    selected_color = palette.get_at((rel_x, rel_y))[:3]
                    running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BACKGROUND_COLOR)
        screen.blit(palette, palette_rect)
        pygame.draw.rect(screen, selected_color, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 120, 80, 40), border_radius=10)
        text = HANDWRITTEN_FONT.render("Pick a color", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 180))
        pygame.display.flip()
    return selected_color

def has_save_file():
    return os.path.exists("save_data.json")
