import os
import sys

# Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Shooter"

# Paths — support both normal Python and PyInstaller frozen mode
if getattr(sys, 'frozen', False):
    # PyInstaller --onefile extracts to sys._MEIPASS; --onedir uses exe dir
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "SpaceShooter-Full")
ART_DIR = os.path.join(ASSET_DIR, "Art")
AUDIO_DIR = os.path.join(ASSET_DIR, "Audio")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Player settings
PLAYER_SPEED = 300
PLAYER_HP = 3
PLAYER_FIRE_RATE = 0.2
PLAYER_INVULN_TIME = 1.5
PLAYER_START_LIVES = 3

# Scale factors
SCALE_PLAYER = 0.25
SCALE_ENEMY_SCOUT = 0.19
SCALE_ENEMY_FIGHTER = 0.22
SCALE_ENEMY_HEAVY = 0.25
SCALE_ENEMY_TANK = 0.28
SCALE_TURRET = 0.22
SCALE_PICKUP = 0.175
SCALE_PROJECTILE = 0.07
SCALE_EXPLOSION_BIG = 0.16
SCALE_EXPLOSION_SMALL = 0.08
SCALE_SHIELD = 0.17
SCALE_THRUSTER = 0.12

# Background scroll speed (pixels per second)
BG_SCROLL_SPEED = 60

# Enemy base settings (before stage multipliers)
ENEMY_SETTINGS = {
    "scout": {
        "hp": 1,
        "speed": 180,
        "fire_rate": 1.5,
        "points": 100,
        "weapon": "laser",
    },
    "fighter": {
        "hp": 3,
        "speed": 120,
        "fire_rate": 1.0,
        "points": 250,
        "weapon": "plasma",
    },
    "heavy": {
        "hp": 6,
        "speed": 70,
        "fire_rate": 0.8,
        "points": 500,
        "weapon": "missile",
    },
    "tank": {
        "hp": 10,
        "speed": 30,
        "fire_rate": 0.6,
        "points": 750,
        "weapon": "plasma",
    },
    "turret": {
        "hp": 5,
        "speed": 0,
        "fire_rate": 0.7,
        "points": 400,
        "weapon": "laser",
    },
}

# Projectile settings
PROJECTILE_SPEED_BULLET = 500
PROJECTILE_SPEED_LASER = 600
PROJECTILE_SPEED_MISSILE = 350
PROJECTILE_SPEED_HEAVY_MISSILE = 300
PROJECTILE_SPEED_PLASMA = 400
PROJECTILE_SPEED_HOMING = 280

PROJECTILE_DAMAGE = {
    "bullet": 1,
    "laser": 1,
    "missile": 2,
    "heavy_missile": 4,
    "plasma": 2,
    "homing_missile": 2,
    "homing_laser": 1,
    "bomb": 50,
}

# Enemy projectile speed
ENEMY_PROJECTILE_SPEED = 250

# Powerup settings
POWERUP_SPEED = 100
POWERUP_DURATION = 10.0
SHIELD_HP = 3
BOMB_MAX = 3

# Extra life thresholds
EXTRA_LIFE_SCORES = [5000, 15000, 30000, 50000, 80000]

# Stage difficulty multipliers (applied to enemy base settings)
STAGE_MULTIPLIERS = {
    1: {"hp": 1.0, "speed": 1.0, "fire_rate": 1.0, "points": 1.0},
    2: {"hp": 1.3, "speed": 1.1, "fire_rate": 0.9, "points": 1.2},
    3: {"hp": 1.6, "speed": 1.2, "fire_rate": 0.8, "points": 1.5},
    4: {"hp": 2.0, "speed": 1.3, "fire_rate": 0.7, "points": 1.8},
    5: {"hp": 2.5, "speed": 1.4, "fire_rate": 0.6, "points": 2.0},
}

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_STAGE_TRANSITION = "stage_transition"
STATE_WAVE_TRANSITION = "wave_transition"
STATE_WIN = "win"
