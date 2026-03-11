import os
import pygame
from settings import (
    ART_DIR, AUDIO_DIR,
    SCALE_PLAYER, SCALE_ENEMY_SCOUT, SCALE_ENEMY_FIGHTER,
    SCALE_ENEMY_HEAVY, SCALE_ENEMY_TANK, SCALE_TURRET,
    SCALE_PICKUP, SCALE_PROJECTILE, SCALE_EXPLOSION_BIG,
    SCALE_EXPLOSION_SMALL, SCALE_SHIELD, SCALE_THRUSTER,
    SCREEN_WIDTH,
)


def load_image(path, scale=None):
    img = pygame.image.load(path).convert_alpha()
    if scale is not None:
        w = int(img.get_width() * scale)
        h = int(img.get_height() * scale)
        img = pygame.transform.scale(img, (w, h))
    return img


def load_sequence(folder, prefix, count, scale=None):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join(folder, f"{prefix}{i}.png")
        frames.append(load_image(path, scale))
    return frames


def load_background(path):
    img = pygame.image.load(path).convert()
    scale = SCREEN_WIDTH / img.get_width()
    w = SCREEN_WIDTH
    h = int(img.get_height() * scale)
    return pygame.transform.scale(img, (w, h))


class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = {}

    def load_all(self):
        self._load_player_images()
        self._load_enemy_images()
        self._load_weapon_images()
        self._load_effect_images()
        self._load_pickup_images()
        self._load_backgrounds()
        self._load_sounds()
        self._load_music()

    # --- Player ---
    def _load_player_images(self):
        ship_dir = os.path.join(ART_DIR, "Player", "Ship")
        thruster_dir = os.path.join(ship_dir, "ThrusterEmit")

        for variant in ("Light", "Medium", "Heavy"):
            key = f"player_{variant.lower()}"
            self.images[key] = load_image(
                os.path.join(ship_dir, f"PlayerShip_{variant}.png"), SCALE_PLAYER
            )
            tilt_path = os.path.join(ship_dir, f"PlayerShip_{variant}_Tilt.png")
            if os.path.exists(tilt_path):
                self.images[f"{key}_tilt"] = load_image(tilt_path, SCALE_PLAYER)

            fire_dir = os.path.join(ship_dir, f"PlayerShip_{variant}_Fire")
            if os.path.isdir(fire_dir):
                count = len([f for f in os.listdir(fire_dir) if f.endswith(".png")])
                self.images[f"{key}_fire"] = load_sequence(
                    fire_dir, f"PlayerShip_{variant}_Fire", count, SCALE_PLAYER
                )

        self.images["thruster_player"] = load_sequence(
            thruster_dir, "Thruster_Player", 6, SCALE_THRUSTER
        )

    # --- Enemies ---
    def _load_enemy_images(self):
        ship_dir = os.path.join(ART_DIR, "Enemies", "Ship")
        thruster_dir = os.path.join(ship_dir, "ThrusterEmit")
        turret_dir = os.path.join(ART_DIR, "Enemies", "Turret")

        for i in range(1, 4):
            scales = {1: SCALE_ENEMY_SCOUT, 2: SCALE_ENEMY_FIGHTER, 3: SCALE_ENEMY_HEAVY}
            sc = scales[i]
            key = f"enemy_ship{i}"
            self.images[f"{key}_base"] = load_image(
                os.path.join(ship_dir, f"EnemyShip{i}_Base.png"), sc
            )
            tilt_path = os.path.join(ship_dir, f"EnemyShip{i}_Base_Tilt.png")
            if os.path.exists(tilt_path):
                self.images[f"{key}_tilt"] = load_image(tilt_path, sc)
            tilt2_path = os.path.join(ship_dir, f"EnemyShip{i}_Base_Tilt2.png")
            if os.path.exists(tilt2_path):
                self.images[f"{key}_tilt2"] = load_image(tilt2_path, sc)
            upgraded_path = os.path.join(ship_dir, f"EnemyShip{i}_Upgraded.png")
            if os.path.exists(upgraded_path):
                self.images[f"{key}_upgraded"] = load_image(upgraded_path, sc)

        self.images["enemy_tank"] = load_image(
            os.path.join(ship_dir, "Enemy_Tank_Base.png"), SCALE_ENEMY_TANK
        )

        self.images["thruster_enemy"] = load_sequence(
            thruster_dir, "Thruster_Enemy", 6, SCALE_THRUSTER
        )

        self.images["turret_base"] = load_image(
            os.path.join(turret_dir, "EnemyTurret_Base.png"), SCALE_TURRET
        )
        self.images["turret_destroyed"] = load_image(
            os.path.join(turret_dir, "EnemyTurret_Destroyed.png"), SCALE_TURRET
        )
        for wtype in ("Laser", "Missile", "Plasma"):
            for j in (1, 2):
                path = os.path.join(turret_dir, f"EnemyTurret_{wtype}{j}.png")
                if os.path.exists(path):
                    self.images[f"turret_{wtype.lower()}{j}"] = load_image(path, SCALE_TURRET)

    # --- Weapons ---
    def _load_weapon_images(self):
        player_wep = os.path.join(ART_DIR, "Player", "Weapon")
        enemy_wep = os.path.join(ART_DIR, "Enemies", "Weapon")

        weapon_configs = {
            "player_bullet": (player_wep, "Bullet", "Projectile_Player_Bullet", 5),
            "player_bullet_emit": (player_wep, "BulletEmit", "Emitter_Player_Bullet", 4),
            "player_laser": (player_wep, "Laser", "Projectile_Player_Laser", 5),
            "player_laser_emit": (player_wep, "LaserEmit", "Emitter_Player_Laser", 4),
            "player_missile": (player_wep, "Missile", "Projectile_Player_Missile", 6),
            "player_missile_emit": (player_wep, "MissileEmit", "Emitter_Player_Missile", 6),
            "player_heavy_missile": (player_wep, "HeavyMissile", "Projectile_Player_HeavyMissile", 6),
            "player_plasma": (player_wep, "Plasma", "Projectile_Player_Plasma", 8),
            "player_plasma_emit": (player_wep, "PlasmaEmit", "Emitter_Player_Plasma", 6),
            "enemy_laser": (enemy_wep, "Laser", "Projectile_Enemy_Laser", 5),
            "enemy_laser_emit": (enemy_wep, "LaserEmit", "Emitter_Enemy_Laser", 5),
            "enemy_missile": (enemy_wep, "Missile", "Projectile_Enemy_Missile", 4),
            "enemy_missile_emit": (enemy_wep, "MissileEmit", "Emitter_Enemy_Missile", 6),
            "enemy_plasma": (enemy_wep, "Plasma", "Projectile_Enemy_Plasma", 7),
            "enemy_plasma_emit": (enemy_wep, "PlasmaEmit", "Emitter_Enemy_Plasma", 6),
        }
        for key, (base, subfolder, prefix, count) in weapon_configs.items():
            self.images[key] = load_sequence(
                os.path.join(base, subfolder), prefix, count, SCALE_PROJECTILE
            )

    # --- Effects ---
    def _load_effect_images(self):
        effects_dir = os.path.join(ART_DIR, "Effects")
        self.images["explosion_big"] = load_sequence(
            os.path.join(effects_dir, "Explosion"), "Explosion", 11, SCALE_EXPLOSION_BIG
        )
        self.images["explosion_small"] = load_sequence(
            os.path.join(effects_dir, "Explosion_Two"), "Explosion_Two", 10, SCALE_EXPLOSION_SMALL
        )
        self.images["shield_effect"] = load_sequence(
            os.path.join(effects_dir, "Shield"), "Shield_Player", 10, SCALE_SHIELD
        )

    # --- Pickups ---
    def _load_pickup_images(self):
        pickup_dir = os.path.join(ART_DIR, "Pickups")
        for name in ("Credits", "Health", "PowerUp", "Shield"):
            self.images[f"pickup_{name.lower()}"] = load_image(
                os.path.join(pickup_dir, f"PickUp_{name}.png"), SCALE_PICKUP
            )

    # --- Backgrounds ---
    def _load_backgrounds(self):
        bg_dir = os.path.join(ART_DIR, "Environment", "Backgrounds")
        self.images["backgrounds"] = []
        for i in range(1, 10):
            ext = ".PNG" if i <= 5 else ".png"
            path = os.path.join(bg_dir, f"Background{i}{ext}")
            if os.path.exists(path):
                self.images["backgrounds"].append(load_background(path))

    # --- Sounds ---
    def _load_sounds(self):
        sfx_dir = os.path.join(AUDIO_DIR, "SFX")

        sound_map = {
            "player_bullet": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_BulletFire1.wav"),
            "player_blaster": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_BlasterFire1.wav"),
            "player_rocket": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_RocketFire1.wav"),
            "player_heavy_rocket": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_HeavyRocketFire1.wav"),
            "player_plasma": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_PlasmaFire1.wav"),
            "player_upgrade": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_Upgrade.wav"),
            "shield_start": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_Shield1_LoopStart.wav"),
            "shield_end": os.path.join(sfx_dir, "Player Ship", "SFX_PlayerShip_Shield1_LoopEnd.wav"),
            "enemy_laser": os.path.join(sfx_dir, "Enemy Ship", "SFX_EnemyShip_Laser1.wav"),
            "enemy_missile": os.path.join(sfx_dir, "Enemy Ship", "SFX_EnemyShip_Missile1.wav"),
            "enemy_plasma": os.path.join(sfx_dir, "Enemy Ship", "SFX_EnemyShip_Plasma1.wav"),
            "explosion_big": os.path.join(sfx_dir, "Misc", "SFX_Explosion_Big.wav"),
            "explosion_small": os.path.join(sfx_dir, "Misc", "SFX_Explosion_Small.wav"),
            "pickup": os.path.join(sfx_dir, "Misc", "SFX_Pickup_Powerup.wav"),
            "turret_laser": os.path.join(sfx_dir, "Turrets", "SFX_Turret_Laser1.wav"),
            "turret_missile": os.path.join(sfx_dir, "Turrets", "SFX_Turret_Missile1.wav"),
            "turret_plasma": os.path.join(sfx_dir, "Turrets", "SFX_Turret_Plasma1.wav"),
        }
        for key, path in sound_map.items():
            if os.path.exists(path):
                self.sounds[key] = pygame.mixer.Sound(path)
                self.sounds[key].set_volume(0.3)

    # --- Music ---
    def _load_music(self):
        music_dir = os.path.join(AUDIO_DIR, "Music", "OGG")
        for name in ("Track1", "Track1_Lose", "Track1_Win", "Track2", "Track2_Lose", "Track2_Win"):
            path = os.path.join(music_dir, f"{name}.ogg")
            if os.path.exists(path):
                self.music[name.lower()] = path

    def play_sound(self, key):
        if key in self.sounds:
            self.sounds[key].play()

    def play_music(self, key, loops=-1):
        if key in self.music:
            pygame.mixer.music.load(self.music[key])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()
