import pygame
import random
import sys

# Start pygame engine
pygame.init()

# Window size
WIDTH = 400
HEIGHT = 600

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

# Clock controls how fast the game runs
clock = pygame.time.Clock()

# Font for drawing text on screen
font = pygame.font.SysFont("Arial", 28)

# Load images from the same folder
road_img = pygame.image.load("road.png")
player_img = pygame.image.load("me.png")
enemy_img = pygame.image.load("enemy.png")
coin_img = pygame.image.load("coin.png")

# Score counter
score = 0

# Enemy speeds up every time player collects this many points
SPEED_UP_EVERY = 5

# How much extra speed the enemy gets each time
SPEED_BOOST = 1

# ---- COIN WEIGHT TABLE ----
# Each coin type has: worth (points), color (tint), weight (spawn chance)
# Higher weight = spawns more often
COIN_TYPES = [
    {"worth": 1, "color": (255, 215,   0), "weight": 60},  # Gold   — common,   1 point
    {"worth": 2, "color": (0, 192, 0), "weight": 30},  # Silver — uncommon, 2 points
    {"worth": 3, "color": (0,   0, 128), "weight": 10},  # Blue   — rare,     3 points
]


# ---- CLASSES ----

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        # Place player at the bottom center of the screen
        self.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        # Move left, but don't go off screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        # Move right, but don't go off screen
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        # Spawn above the screen at a random x
        self.rect.center = (random.randint(50, WIDTH - 50), -60)
        # Base speed (will increase as player scores points)
        self.speed = random.randint(4, 7)

    def update(self):
        # Move down every frame
        self.rect.y += self.speed
        # If enemy goes off the bottom, reset to the top with current speed bonus
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -60)
            self.speed = random.randint(4, 7) + speed_bonus

    def apply_speed_boost(self):
        # Add one speed boost to this enemy right now
        self.speed += SPEED_BOOST


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Pick a random coin type based on weights (60/30/10 chance)
        # random.choices() returns a list so we take [0] to get the item
        coin_type = random.choices(COIN_TYPES, weights=[t["weight"] for t in COIN_TYPES])[0]

        # Save how many points this coin gives
        self.worth = coin_type["worth"]

        # Copy the coin image so we can tint it without affecting the original
        self.image = coin_img.copy()

        # BLEND_MULT multiplies each pixel color with the tint color
        # Gold stays gold, silver makes it gray, blue makes it blue
        self.image.fill(coin_type["color"], special_flags=pygame.BLEND_MULT)

        self.rect = self.image.get_rect()
        # Spawn above the screen at a random x
        self.rect.center = (random.randint(30, WIDTH - 30), -40)
        self.speed = 3

    def update(self):
        # Move down every frame
        self.rect.y += self.speed
        # If coin falls off the bottom, respawn at the top
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(30, WIDTH - 30), -40)


# ---- GAME OVER SCREEN ----

def show_game_over(final_score):
    screen.fill((20, 20, 20))

    big_font = pygame.font.SysFont("Arial", 52, bold=True)
    msg = big_font.render("GAME OVER", True, (220, 50, 50))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 180))

    small_font = pygame.font.SysFont("Arial", 32)
    score_msg = small_font.render(f"Score: {final_score}", True, (255, 220, 50))
    screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, 270))

    quit_msg = small_font.render("Press Q to quit", True, (180, 180, 180))
    screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, 340))

    pygame.display.update()

    # Wait until player presses Q or closes the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()


# ---- CREATE GAME OBJECTS ----

player = Player()
enemy = Enemy()

enemies_group = pygame.sprite.Group()
enemies_group.add(enemy)

# Start with 3 coins spread at different heights so they trickle in naturally
coins_group = pygame.sprite.Group()
for i in range(3):
    c = Coin()
    c.rect.center = (random.randint(30, WIDTH - 30), random.randint(-400, -40))
    coins_group.add(c)

# Group with everything — update() and draw() work on the whole group at once
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)
all_sprites.add(*coins_group)

# Total extra speed enemies have gained so far (used when a new enemy respawns)
speed_bonus = 0

# The last milestone we already boosted at (so we don't boost twice at the same score)
last_milestone = 0


# ---- MAIN GAME LOOP ----

while True:

    # 1. CHECK EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 2. UPDATE LOGIC

    player.move()

    # Calls update() on every sprite — enemies and coins move down automatically
    all_sprites.update()

    # Check if player touched any coins
    collected = pygame.sprite.spritecollide(player, coins_group, True)
    for c in collected:
        # Add this coin's worth (1, 2, or 3 points) to score
        score += c.worth

        # Spawn a fresh coin to replace the one that was collected
        new_coin = Coin()
        coins_group.add(new_coin)
        all_sprites.add(new_coin)

    # Check if player crossed a new speed-up milestone
    # Example: score=5 → milestone 1, score=10 → milestone 2, etc.
    current_milestone = score // SPEED_UP_EVERY
    if current_milestone > last_milestone:
        last_milestone = current_milestone
        speed_bonus += SPEED_BOOST  # remember total bonus so respawned enemies get it too

        # Instantly boost every enemy currently on screen
        for e in enemies_group:
            e.apply_speed_boost()

    # Check if player crashed into an enemy
    if pygame.sprite.spritecollideany(player, enemies_group):
        show_game_over(score)

    # 3. DRAW EVERYTHING

    # Draw the road background first (wipes the previous frame)
    screen.blit(road_img, (0, 0))

    # Draw all sprites on top of the background
    all_sprites.draw(screen)

    # Draw score in the top right corner
    score_text = font.render(f"Score: {score}", True, (255, 220, 50))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Show the finished frame on screen
    pygame.display.update()

    # Cap at 60 frames per second
    clock.tick(60)