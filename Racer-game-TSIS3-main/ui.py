import pygame
import sys
from persistence import load_leaderboard, save_settings, load_settings

# Colors used across all screens
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (100, 100, 100)
YELLOW = (255, 220, 50)
RED    = (220, 50,  50)
GREEN  = (50,  200, 50)
DARK   = (20,  20,  20)
BLUE   = (50,  120, 220)


def draw_button(screen, text, rect, font, color=GRAY, text_color=WHITE):
    """Draw a simple filled rectangle button with centered text."""
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    screen.blit(label, (rect.centerx - label.get_width() // 2,
                        rect.centery - label.get_height() // 2))


def ask_username(screen, clock, width, height):
    """
    Simple text-input screen.
    Player types their name and presses Enter.
    Returns the typed name string.
    """
    font_big   = pygame.font.SysFont("Arial", 40, bold=True)
    font_small = pygame.font.SysFont("Arial", 28)
    name = ""

    while True:
        screen.fill(DARK)

        title = font_big.render("Enter your name:", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 200))

        # Draw the name the player is typing inside a box
        box_rect = pygame.Rect(width // 2 - 150, 270, 300, 50)
        pygame.draw.rect(screen, GRAY, box_rect, border_radius=6)
        name_surf = font_small.render(name + "|", True, WHITE)
        screen.blit(name_surf, (box_rect.x + 10, box_rect.y + 10))

        hint = font_small.render("Press Enter to start", True, GRAY)
        screen.blit(hint, (width // 2 - hint.get_width() // 2, 350))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Only allow printable characters, max 16 chars
                    if len(name) < 16 and event.unicode.isprintable():
                        name += event.unicode


def main_menu(screen, clock, width, height):
    """
    Main menu with Play, Leaderboard, Settings, Quit buttons.
    Returns: "play", "leaderboard", "settings", or "quit"
    """
    font_title  = pygame.font.SysFont("Arial", 52, bold=True)
    font_button = pygame.font.SysFont("Arial", 30)

    # Button rectangles: (x, y, w, h)
    btn_play   = pygame.Rect(width // 2 - 120, 220, 240, 55)
    btn_board  = pygame.Rect(width // 2 - 120, 295, 240, 55)
    btn_set    = pygame.Rect(width // 2 - 120, 370, 240, 55)
    btn_quit   = pygame.Rect(width // 2 - 120, 445, 240, 55)

    while True:
        screen.fill(DARK)

        title = font_title.render("RACER", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 130))

        draw_button(screen, "Play",        btn_play,  font_button, GREEN)
        draw_button(screen, "Leaderboard", btn_board, font_button, BLUE)
        draw_button(screen, "Settings",    btn_set,   font_button)
        draw_button(screen, "Quit",        btn_quit,  font_button, RED)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos):
                    return "play"
                if btn_board.collidepoint(event.pos):
                    return "leaderboard"
                if btn_set.collidepoint(event.pos):
                    return "settings"
                if btn_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def settings_screen(screen, clock, width, height):
    """
    Settings screen — player picks difficulty.
    Saves to settings.json and returns.
    """
    font_title  = pygame.font.SysFont("Arial", 42, bold=True)
    font_button = pygame.font.SysFont("Arial", 30)
    font_info   = pygame.font.SysFont("Arial", 22)

    settings = load_settings()
    current   = settings.get("difficulty", "normal")

    btn_easy   = pygame.Rect(width // 2 - 120, 220, 240, 55)
    btn_normal = pygame.Rect(width // 2 - 120, 295, 240, 55)
    btn_hard   = pygame.Rect(width // 2 - 120, 370, 240, 55)
    btn_back   = pygame.Rect(width // 2 - 120, 460, 240, 55)

    while True:
        screen.fill(DARK)

        title = font_title.render("Settings", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 130))

        # Highlight the currently selected difficulty in green
        draw_button(screen, "Easy",   btn_easy,   font_button,
                    GREEN if current == "easy"   else GRAY)
        draw_button(screen, "Normal", btn_normal, font_button,
                    GREEN if current == "normal" else GRAY)
        draw_button(screen, "Hard",   btn_hard,   font_button,
                    GREEN if current == "hard"   else GRAY)
        draw_button(screen, "Back",   btn_back,   font_button, BLUE)

        info = font_info.render(f"Current: {current.upper()}", True, WHITE)
        screen.blit(info, (width // 2 - info.get_width() // 2, 540))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_easy.collidepoint(event.pos):
                    current = "easy"
                    settings["difficulty"] = current
                    save_settings(settings)
                elif btn_normal.collidepoint(event.pos):
                    current = "normal"
                    settings["difficulty"] = current
                    save_settings(settings)
                elif btn_hard.collidepoint(event.pos):
                    current = "hard"
                    settings["difficulty"] = current
                    save_settings(settings)
                elif btn_back.collidepoint(event.pos):
                    return


def leaderboard_screen(screen, clock, width, height):
    """
    Shows top 10 scores with rank, name, score, and distance.
    """
    font_title  = pygame.font.SysFont("Arial", 42, bold=True)
    font_row    = pygame.font.SysFont("Arial", 24)
    font_button = pygame.font.SysFont("Arial", 30)

    btn_back = pygame.Rect(width // 2 - 100, 555, 200, 50)
    board    = load_leaderboard()

    while True:
        screen.fill(DARK)

        title = font_title.render("Leaderboard", True, YELLOW)
        screen.blit(title, (width // 2 - title.get_width() // 2, 30))

        # Column headers
        header = font_row.render("#   Name            Score   Dist", True, GRAY)
        screen.blit(header, (30, 90))

        # Draw each entry
        for i, entry in enumerate(board):
            color = YELLOW if i == 0 else WHITE
            line = f"{i+1:<4}{entry['name'][:14]:<16}{entry['score']:<8}{entry['distance']}m"
            row = font_row.render(line, True, color)
            screen.blit(row, (30, 120 + i * 38))

        if not board:
            empty = font_row.render("No scores yet!", True, GRAY)
            screen.blit(empty, (width // 2 - empty.get_width() // 2, 200))

        draw_button(screen, "Back", btn_back, font_button, BLUE)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return


def game_over_screen(screen, clock, width, height, score, distance, coins):
    """
    Game Over screen showing score, distance, coins collected.
    Returns: "retry" or "menu"
    """
    font_big    = pygame.font.SysFont("Arial", 52, bold=True)
    font_mid    = pygame.font.SysFont("Arial", 30)
    font_button = pygame.font.SysFont("Arial", 28)

    btn_retry = pygame.Rect(width // 2 - 130, 400, 240, 55)
    btn_menu  = pygame.Rect(width // 2 - 130, 470, 240, 55)

    while True:
        screen.fill(DARK)

        title = font_big.render("GAME OVER", True, RED)
        screen.blit(title, (width // 2 - title.get_width() // 2, 150))

        lines = [
            f"Score:    {score}",
            f"Distance: {distance} m",
            f"Coins:    {coins}",
        ]
        for i, line in enumerate(lines):
            surf = font_mid.render(line, True, WHITE)
            screen.blit(surf, (width // 2 - surf.get_width() // 2, 240 + i * 45))

        draw_button(screen, "Retry",     btn_retry, font_button, GREEN)
        draw_button(screen, "Main Menu", btn_menu,  font_button, BLUE)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos):
                    return "retry"
                if btn_menu.collidepoint(event.pos):
                    return "menu"
