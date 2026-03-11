# Space Shooter - Vertical Scrolling Shoot 'Em Up

## Project Goal

Build a vertical-scrolling space shooter in Python using the pygame library. The player controls a spaceship, shoots enemies, earns points, and progresses through increasingly difficult stages.

## Tech Stack

- **Language:** Python 3
- **Framework:** pygame
- **Platform:** Windows 10

## Game Design

### Core Gameplay
- Vertical scrolling space shooter (screen scrolls top-to-bottom)
- Player ship at the bottom of the screen, enemies come from the top
- Player moves in all directions and fires weapons upward
- Score-based progression with different enemy types worth different points

### Stage & Wave System
- The game is divided into **stages** of increasing difficulty
- Each stage has a **maximum of 5 waves** of enemies
- Between stages, difficulty escalates: enemy speed, fire rate, movement patterns, and HP increase
- Each stage should feel distinct (different backgrounds, enemy compositions, movement patterns)

### Enemy Types & Scoring
- **EnemyShip1 (Scout):** Fast, low HP, simple patterns — low points
- **EnemyShip2 (Fighter):** Medium speed, moderate HP, can fire back — medium points
- **EnemyShip3 (Heavy):** Slow, high HP, heavy firepower — high points
- **Enemy Tank:** Stationary/slow, very high HP, heavy weapons — high points
- **Turrets:** Mounted on space station segments, rotating fire — bonus points
- Point values should scale with difficulty (later stages = more points per kill)

### Player Upgrades (earned via pickups or score thresholds)
- **Multi-shot:** More projectiles per button press (spread shot, double/triple shot)
- **Shields:** Absorb a hit without losing a life (use Shield_Player animation)
- **Homing Missiles:** Lock onto nearest enemy and track them
- **Homing Lasers:** Laser beams that bend toward enemies
- **Bombs:** Screen-clearing or area-of-effect weapon (limited stock)
- **Extra Lives:** Earn additional lives at score milestones

### Player Ship Variants
The assets include three ship types (Light, Medium, Heavy) each with tilt and fire animations. Choose one as the default player ship, or allow selection.

## Asset Directory

All graphical and audio assets are in: `SpaceShooter-Full/`

### Directory Structure
```
SpaceShooter-Full/
├── Art/
│   ├── Effects/
│   │   ├── Explosion/          # Explosion1-11.png (11 frames)
│   │   ├── Explosion_Two/      # Explosion_Two1-10.png (10 frames)
│   │   └── Shield/             # Shield_Player1-10.png + Shield_Player.png
│   ├── Enemies/
│   │   ├── Ship/               # EnemyShip1-3 (Base, Upgraded, Tilt variants), Enemy_Tank_Base
│   │   │   └── ThrusterEmit/   # Thruster_Enemy1-6.png
│   │   ├── Turret/             # EnemyTurret (Base, Destroyed, Laser/Missile/Plasma variants)
│   │   └── Weapon/
│   │       ├── Laser/          # Projectile_Enemy_Laser1-5.png
│   │       ├── LaserEmit/      # Emitter_Enemy_Laser1-5.png
│   │       ├── Missile/        # Projectile_Enemy_Missile1-4.png
│   │       ├── MissileEmit/    # Emitter_Enemy_Missile1-6.png
│   │       ├── Plasma/         # Projectile_Enemy_Plasma1-7.png
│   │       └── PlasmaEmit/     # Emitter_Enemy_Plasma1-6.png
│   ├── Environment/
│   │   ├── Backgrounds/        # Background1-9 (PNG) — use for stage backgrounds
│   │   └── Space Station/
│   │       ├── Fixtures/       # SpaceStation_Fixture01-17.png
│   │       └── ShipTiles/      # SpaceStationTiles (Corner, Inner, Outer variants)
│   ├── Pickups/                # PickUp_Credits, Health, PowerUp, Shield (.png)
│   └── Player/
│       ├── Ship/               # PlayerShip_Heavy, Light, Medium (+ Tilt variants)
│       │   ├── PlayerShip_Heavy_Fire/   # 8 frames
│       │   ├── PlayerShip_Light_Fire/   # 12 frames
│       │   ├── PlayerShip_Medium_Fire/  # 8 frames
│       │   └── ThrusterEmit/            # Thruster_Player1-6.png
│       └── Weapon/
│           ├── Bullet/         # Projectile_Player_Bullet1-5.png
│           ├── BulletEmit/     # Emitter_Player_Bullet1-4.png
│           ├── HeavyMissile/   # Projectile_Player_HeavyMissile1-6.png
│           ├── Laser/          # Projectile_Player_Laser1-5.png
│           ├── LaserEmit/      # Emitter_Player_Laser1-4.png
│           ├── Missile/        # Projectile_Player_Missile1-6.png
│           ├── MissileEmit/    # Emitter_Player_Missile1-6.png
│           ├── Plasma/         # Projectile_Player_Plasma1-8.png
│           └── PlasmaEmit/     # Emitter_Player_Plasma1-6.png
└── Audio/
    ├── Music/
    │   ├── MP3/    # Track1.mp3, Track1_Lose.mp3, Track1_Win.mp3, Track2 variants
    │   ├── OGG/    # Same tracks in OGG format
    │   └── WAV/    # Same tracks in WAV format
    └── SFX/
        ├── Enemy Ship/    # Electrodes, Laser, Missile, Plasma, Thruster SFX
        ├── Misc/          # Engine loops, Explosion_Big/Small, Pickup_Powerup
        ├── Player Ship/   # Blaster, Bullet, HeavyRocket, Plasma, Rocket fire SFX
        │                  # Shield loops (3 variants), Thruster, Upgrade sounds
        └── Turrets/       # Laser, Missile, Plasma (normal + upgraded), Swivel SFX
```

### Asset Usage Guidelines
- Use **OGG** format for music (best pygame compatibility)
- Use **WAV** for sound effects
- Numbered image sequences are animation frames — load them in order for sprite animations
- "Emit" folders contain muzzle flash / firing effect frames
- "ThrusterEmit" folders contain engine exhaust animations
- Tilt variants are for when the ship moves left/right
- Fire variants are damage states (ship on fire when taking damage)
- No font files included — use pygame's default font or a system font

## Architecture Guidelines

### Code Organization
- Use a modular structure with separate files/modules for:
  - `main.py` — entry point, game loop, state management
  - `settings.py` — constants (screen size, FPS, colors, file paths)
  - `player.py` — player ship class
  - `enemies.py` — enemy classes
  - `weapons.py` — projectile and weapon classes
  - `powerups.py` — pickup/upgrade classes
  - `effects.py` — explosions, shield effects, animations
  - `stages.py` — stage/wave definitions and progression logic
  - `ui.py` — HUD, score display, menus
  - `assets.py` — asset loading and caching

### Key Patterns
- Use pygame sprite groups for efficient rendering and collision detection
- Implement an asset manager that loads and caches images/sounds on startup
- Use a state machine for game states (menu, playing, paused, game over, stage transition)
- Keep game logic frame-rate independent using delta time
- Scrolling background: tile the background image and scroll it continuously downward

### Screen & Performance
- Target resolution: 800x600 or similar vertical-friendly aspect ratio
- Target frame rate: 60 FPS
- Use `convert_alpha()` on all loaded images for performance

## Build & Run

```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

## Do's and Don'ts

### Do
- Use relative paths from the project root for all asset references
- Animate sprites using the numbered frame sequences in the asset folders
- Play sound effects on weapon fire, explosions, pickups, and enemy deaths
- Show a HUD with score, lives, current stage/wave, and active powerups
- Add screen shake or flash effects on big explosions for game feel
- Make enemy waves feel hand-crafted, not purely random

### Don't
- Don't hardcode absolute paths for assets
- Don't load assets inside the game loop — preload everything
- Don't use blocking operations in the game loop
- Don't ignore collision detection edge cases (off-screen cleanup, etc.)
