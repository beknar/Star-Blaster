# Star Blaster

A vertical-scrolling space shooter built with Python and pygame. Fight through waves of increasingly dangerous enemies across multiple stages, collect power-ups, and rack up the highest score you can.

## Running the Game

### Option 1: Single Executable (Windows)

Download and run `dist/StarBlaster.exe` — no installation required. Note that the first launch may take a few seconds while the game unpacks its assets.

### Option 2: From Source

**Requirements:** Python 3, pygame

```bash
pip install pygame
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move ship |
| Space | Fire primary weapon |
| B | Drop bomb |
| P / Escape | Pause |

## Gameplay

You pilot a spaceship from the bottom of the screen while enemies descend from the top. Destroy enemies to earn points, collect pickups to upgrade your ship, and survive through all stages to win.

### Stages & Waves

- The game is divided into stages of increasing difficulty
- Each stage contains up to 5 waves of enemies
- Each stage has a distinct background and enemy composition
- Between stages, enemies become faster, tougher, and more aggressive

### Enemies

| Enemy | HP | Speed | Weapon | Points |
|-------|----|-------|--------|--------|
| Scout | 1 | Fast | Laser | 100 |
| Fighter | 3 | Medium | Plasma | 250 |
| Heavy | 6 | Slow | Missile | 500 |
| Tank | 10 | Very slow | Plasma | 750 |
| Turret | 5 | Stationary | Laser | 400 |

Point values scale up in later stages.

### Power-ups & Upgrades

Pick up dropped items or hit score thresholds to earn upgrades:

- **Multi-shot** — Spread shot (double/triple fire)
- **Shield** — Absorbs one hit without losing a life
- **Homing Missiles** — Lock onto and track the nearest enemy
- **Homing Lasers** — Laser beams that bend toward enemies
- **Bombs** — Area-clearing weapon (limited stock, press B to use)
- **Extra Lives** — Awarded at 5,000 / 15,000 / 30,000 / 50,000 / 80,000 points

## Project Structure

```
Star-Blaster/
├── main.py        # Game loop and state management
├── settings.py    # Constants, paths, difficulty values
├── player.py      # Player ship
├── enemies.py     # Enemy types
├── weapons.py     # Projectiles and weapons
├── powerups.py    # Pickups and upgrades
├── effects.py     # Explosions, shield animations
├── stages.py      # Stage/wave definitions
├── ui.py          # HUD, menus, score display
├── assets.py      # Asset loading and caching
└── SpaceShooter-Full/
    ├── Art/       # Sprites and backgrounds
    └── Audio/     # Music (OGG) and sound effects (WAV)
```

## Building the Executable

Requires [PyInstaller](https://pyinstaller.org):

```bash
pip install pyinstaller
pyinstaller StarBlaster.spec
```

Output: `dist/StarBlaster.exe`
