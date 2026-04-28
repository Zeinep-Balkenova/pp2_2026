import pygame
import random
from persistence import DIFFICULTY_SPEED

# ---- CONSTANTS ----
WIDTH  = 400
HEIGHT = 600

WHITE  = (255, 255, 255)
YELLOW = (255, 220, 50)
RED    = (220, 50,  50)
GREEN  = (50,  200, 50)
CYAN   = (0,   220, 220)

# Score thresholds that trigger an enemy speed boost
SPEED_UP_EVERY = 5
SPEED_BOOST    = 1

# Coin types: worth (points), tint color, spawn weight
COIN_TYPES = [
    {"worth": 1, "color": (255, 215,   0), "weight": 60},  # gold   — common
    {"worth": 2, "color": (0,   192,   0), "weight": 30},  # green  — uncommon
    {"worth": 3, "color": (0,     0, 128), "weight": 10},  # blue   — rare
]

# How long powerup effects last (in milliseconds)
SHIELD_DURATION  = 0        # shield has no timer — lasts until hit
BARRIER_DURATION = 3000     # slow lasts 3 seconds
NITRO_DURATION   = 3000     # speed boost lasts 3 seconds

NORMAL_PLAYER_SPEED  = 5
BARRIER_PLAYER_SPEED = 2    # slower when hit by barrier
NITRO_PLAYER_SPEED   = 9    # faster when nitro is active


# ---- SPRITE CLASSES ----

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.speed = NORMAL_PLAYER_SPEED

        # Powerup state
        self.has_shield  = False        # True = immune to next crash
        self.barrier_end = 0            # pygame.time.get_ticks() when barrier ends
        self.nitro_end   = 0            # pygame.time.get_ticks() when nitro ends

    def move(self):
        keys = pygame.key.get_pressed()

        # Figure out current speed based on active effects
        now = pygame.time.get_ticks()
        if now < self.nitro_end:
            spd = NITRO_PLAYER_SPEED
        elif now < self.barrier_end:
            spd = BARRIER_PLAYER_SPEED
        else:
            spd = NORMAL_PLAYER_SPEED

        if keys[pygame.K_LEFT]  and self.rect.left  > 0:
            self.rect.x -= spd
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += spd

    def activate_barrier(self):
        """Player drove over a barrier — slow them down for 3 s."""
        self.barrier_end = pygame.time.get_ticks() + BARRIER_DURATION

    def activate_nitro(self):
        """Player picked up nitro — speed boost for 3 s."""
        self.nitro_end = pygame.time.get_ticks() + NITRO_DURATION

    def get_active_effect(self):
        """Return a string describing what effect is active right now."""
        now = pygame.time.get_ticks()
        if self.has_shield:
            return "SHIELD"
        if now < self.nitro_end:
            return "NITRO"
        if now < self.barrier_end:
            return "SLOW"
        return ""


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_range, speed_bonus=0):
        super().__init__()
        # img is set by racer after loading
        self.image = None
        self._speed_range = speed_range
        self._speed_bonus = speed_bonus
        self.speed = random.randint(*speed_range) + speed_bonus
        self.rect  = None   # set after image is assigned

    def setup(self, img):
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(50, WIDTH - 50), -60)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(50, WIDTH - 50), -60)
            # Reset speed (applies current bonus)
            self.speed = random.randint(*self._speed_range) + self._speed_bonus

    def apply_speed_boost(self):
        self.speed += SPEED_BOOST
        self._speed_bonus += SPEED_BOOST


class Coin(pygame.sprite.Sprite):
    def __init__(self, coin_img):
        super().__init__()
        coin_type  = random.choices(COIN_TYPES, weights=[t["weight"] for t in COIN_TYPES])[0]
        self.worth = coin_type["worth"]
        self.image = coin_img.copy()
        self.image.fill(coin_type["color"], special_flags=pygame.BLEND_MULT)
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), -40)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(30, WIDTH - 30), -40)


class Shield(pygame.sprite.Sprite):
    """Picking this up gives 1 hit of immunity."""
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), -80)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(30, WIDTH - 30), -80)


class Barrier(pygame.sprite.Sprite):
    """Hitting this slows the player for 3 s."""
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), -80)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(30, WIDTH - 30), -80)


class Nitro(pygame.sprite.Sprite):
    """Picking this up boosts player speed for 3 s."""
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), -80)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(30, WIDTH - 30), -80)


# ---- HUD ----

def draw_hud(screen, font, score, distance, coins_collected, effect):
    """Draw score, distance, and active powerup effect on screen."""
    # Score — top right
    score_surf = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_surf, (WIDTH - score_surf.get_width() - 10, 10))

    # Distance — top left
    dist_surf = font.render(f"{distance} m", True, WHITE)
    screen.blit(dist_surf, (10, 10))

    # Coins — top left below distance
    coin_surf = font.render(f"Coins: {coins_collected}", True, YELLOW)
    screen.blit(coin_surf, (10, 40))

    # Active effect indicator
    if effect == "SHIELD":
        eff_surf = font.render("[ SHIELD ]", True, CYAN)
        screen.blit(eff_surf, (WIDTH // 2 - eff_surf.get_width() // 2, 10))
    elif effect == "NITRO":
        eff_surf = font.render("[ NITRO ]", True, GREEN)
        screen.blit(eff_surf, (WIDTH // 2 - eff_surf.get_width() // 2, 10))
    elif effect == "SLOW":
        eff_surf = font.render("[ SLOW ]", True, RED)
        screen.blit(eff_surf, (WIDTH // 2 - eff_surf.get_width() // 2, 10))


# ---- MAIN GAME FUNCTION ----

def run_game(screen, clock, username, settings):
    """
    Run one session of the game.
    Returns (score, distance, coins_collected) when the player crashes.
    """

    # Load images
    road_img   = pygame.image.load("assets/road.png")
    player_img = pygame.image.load("assets/me.png")
    enemy_img  = pygame.image.load("assets/enemy.png")
    coin_img   = pygame.image.load("assets/coin.png")
    shield_img = pygame.image.load("assets/shield.png")
    barrier_img= pygame.image.load("assets/barrier.png")
    nitro_img  = pygame.image.load("assets/nitro.png")

    font = pygame.font.SysFont("Arial", 24)

    # Speed range based on difficulty setting
    difficulty   = settings.get("difficulty", "normal")
    speed_range  = DIFFICULTY_SPEED[difficulty]
    sr           = (speed_range["min"], speed_range["max"])

    # Game state
    score           = 0
    distance        = 0          # increases every frame
    coins_collected = 0
    speed_bonus     = 0          # total extra speed enemies have gained
    last_milestone  = 0
    road_y          = 0          # for scrolling background

    # Create player
    player = Player(player_img)

    # Create one enemy
    enemy = Enemy(sr)
    enemy.setup(enemy_img)

    enemies_group = pygame.sprite.Group(enemy)

    # Create 3 coins spread out vertically so they trickle in
    coins_group = pygame.sprite.Group()
    for _ in range(3):
        c = Coin(coin_img)
        c.rect.center = (random.randint(30, WIDTH - 30), random.randint(-400, -40))
        coins_group.add(c)

    # One of each powerup on the road at a time
    shield_group  = pygame.sprite.Group(Shield(shield_img))
    barrier_group = pygame.sprite.Group(Barrier(barrier_img))
    nitro_group   = pygame.sprite.Group(Nitro(nitro_img))

    # All sprites in one group for drawing
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, enemy)
    all_sprites.add(*coins_group)
    all_sprites.add(*shield_group, *barrier_group, *nitro_group)

    # ---- GAME LOOP ----
    while True:

        # 1. EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys
                pygame.quit()
                sys.exit()

        # 2. UPDATE

        player.move()
        all_sprites.update()

        # Scroll road background downward to feel like movement
        road_y = (road_y + 5) % HEIGHT

        # Distance goes up every frame (~60 fps, we divide to get meters)
        distance += 1

        # -- Coin collection --
        collected = pygame.sprite.spritecollide(player, coins_group, True)
        for c in collected:
            score           += c.worth
            coins_collected += 1
            # Spawn a replacement coin
            new_coin = Coin(coin_img)
            coins_group.add(new_coin)
            all_sprites.add(new_coin)

        # -- Shield pickup --
        if pygame.sprite.spritecollideany(player, shield_group):
            player.has_shield = True
            # Respawn the shield far above
            for s in shield_group:
                s.rect.center = (random.randint(30, WIDTH - 30), -200)

        # -- Barrier hit --
        if pygame.sprite.spritecollideany(player, barrier_group):
            player.activate_barrier()
            for b in barrier_group:
                b.rect.center = (random.randint(30, WIDTH - 30), -200)

        # -- Nitro pickup --
        if pygame.sprite.spritecollideany(player, nitro_group):
            player.activate_nitro()
            for n in nitro_group:
                n.rect.center = (random.randint(30, WIDTH - 30), -200)

        # -- Speed milestone check --
        current_milestone = score // SPEED_UP_EVERY
        if current_milestone > last_milestone:
            last_milestone = current_milestone
            speed_bonus += SPEED_BOOST
            for e in enemies_group:
                e.apply_speed_boost()

        # -- Enemy collision --
        if pygame.sprite.spritecollideany(player, enemies_group):
            if player.has_shield:
                # Shield absorbs the crash — remove shield, push enemies away
                player.has_shield = False
                for e in enemies_group:
                    e.rect.y = -100   # teleport enemy off screen
            else:
                # Real crash — game over
                return score, distance // 10, coins_collected

        # 3. DRAW

        # Scrolling road: draw it twice so it tiles seamlessly
        screen.blit(road_img, (0, road_y - HEIGHT))
        screen.blit(road_img, (0, road_y))

        all_sprites.draw(screen)

        draw_hud(screen, font, score, distance // 10, coins_collected,
                 player.get_active_effect())

        pygame.display.update()
        clock.tick(60)
