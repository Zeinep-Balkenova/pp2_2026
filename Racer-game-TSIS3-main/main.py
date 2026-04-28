import pygame
import sys

# Our own modules
from ui          import main_menu, ask_username, settings_screen, leaderboard_screen, game_over_screen
from racer       import run_game
from persistence import load_settings, save_score

# ---- SETUP ----
pygame.init()

WIDTH  = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Load settings once at startup
settings = load_settings()

# Ask for username once at startup
username = ask_username(screen, clock, WIDTH, HEIGHT)

# ---- MAIN LOOP ----
# We loop between screens until the player quits

while True:

    # Show main menu — returns what the player clicked
    choice = main_menu(screen, clock, WIDTH, HEIGHT)

    if choice == "leaderboard":
        leaderboard_screen(screen, clock, WIDTH, HEIGHT)

    elif choice == "settings":
        settings_screen(screen, clock, WIDTH, HEIGHT)
        settings = load_settings()   # reload after saving

    elif choice == "play":
        # Keep letting the player retry without going back to the menu
        while True:
            score, distance, coins = run_game(screen, clock, username, settings)

            # Save this run to leaderboard
            save_score(username, score, distance)

            # Show game over screen
            result = game_over_screen(screen, clock, WIDTH, HEIGHT, score, distance, coins)

            if result == "retry":
                continue        # play again immediately
            else:
                break           # go back to main menu
