import json
import os

# ---- FILE PATHS ----
LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

# Default settings if no file exists yet
DEFAULT_SETTINGS = {
    "difficulty": "normal"   # "easy", "normal", "hard"
}

# How difficulty affects enemy base speed
DIFFICULTY_SPEED = {
    "easy":   {"min": 2, "max": 4},
    "normal": {"min": 4, "max": 7},
    "hard":   {"min": 6, "max": 10},
}


# ---- SETTINGS ----

def load_settings():
    """Load settings from file. If no file, return defaults."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Save settings dict to file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


# ---- LEADERBOARD ----

def load_leaderboard():
    """Load leaderboard list from file. Returns empty list if no file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []


def save_score(name, score, distance):
    """Add a new entry and keep only top 10, sorted by score."""
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    # Sort by score descending, keep top 10
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=2)
