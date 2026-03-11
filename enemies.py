import math
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SETTINGS, STAGE_MULTIPLIERS,
)
from weapons import create_enemy_projectile
from effects import ThrusterEffect


class Enemy(pygame.sprite.Sprite):
    """Base enemy class."""

    def __init__(self, assets, enemy_type, x, y, stage, groups, movement="straight"):
        super().__init__()
        self.assets = assets
        self.enemy_type = enemy_type
        self.groups_ref = groups
        self.movement = movement

        # Get base settings and apply stage multipliers
        base = ENEMY_SETTINGS[enemy_type]
        mult = STAGE_MULTIPLIERS.get(stage, STAGE_MULTIPLIERS[5])

        self.hp = int(base["hp"] * mult["hp"])
        self.max_hp = self.hp
        self.speed = base["speed"] * mult["speed"]
        self.fire_rate = base["fire_rate"] * mult["fire_rate"]
        self.points = int(base["points"] * mult["points"])
        self.weapon_type = base["weapon"]

        # Image selection
        self.image = self._get_image(assets, enemy_type)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(x)
        self.pos_y = float(y)

        # Fire timer with random offset to prevent synchronized volleys
        self.fire_timer = random.uniform(0.5, self.fire_rate)

        # Movement state
        self.move_timer = 0
        self.move_phase = random.uniform(0, math.pi * 2)
        self.entered_screen = False

        # Thruster
        thruster_frames = assets.images.get("thruster_enemy", [])
        if thruster_frames and enemy_type != "turret":
            self.thruster = ThrusterEffect(thruster_frames, self, -5)
            # Flip thruster for enemies (they face downward)
            for i, frame in enumerate(self.thruster.frames):
                self.thruster.frames[i] = pygame.transform.flip(frame, False, True)
            self.thruster.offset_y = -self.rect.height // 2 - 5
            groups["effects"].add(self.thruster)

    def _get_image(self, assets, enemy_type):
        image_map = {
            "scout": "enemy_ship1_base",
            "fighter": "enemy_ship2_base",
            "heavy": "enemy_ship3_base",
            "tank": "enemy_tank",
            "turret": "turret_base",
        }
        key = image_map.get(enemy_type, "enemy_ship1_base")
        img = assets.images[key]
        # Rotate enemies to face downward (they come from top)
        if enemy_type != "turret":
            img = pygame.transform.flip(img, False, True)
        return img

    def update(self, dt):
        self.move_timer += dt
        self._move(dt)
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        # Check if entered screen
        if not self.entered_screen and self.rect.top > 0:
            self.entered_screen = True

        # Fire timer
        if self.entered_screen:
            self.fire_timer -= dt

        # Remove if far off screen bottom
        if self.rect.top > SCREEN_HEIGHT + 100:
            self.kill()

    def _move(self, dt):
        if self.movement == "straight":
            self.pos_y += self.speed * dt
        elif self.movement == "zigzag":
            self.pos_y += self.speed * dt
            self.pos_x += math.sin(self.move_timer * 2 + self.move_phase) * 120 * dt
            self.pos_x = max(20, min(SCREEN_WIDTH - 20, self.pos_x))
        elif self.movement == "sine":
            self.pos_y += self.speed * 0.7 * dt
            self.pos_x += math.sin(self.move_timer * 1.5 + self.move_phase) * 150 * dt
            self.pos_x = max(20, min(SCREEN_WIDTH - 20, self.pos_x))
        elif self.movement == "swoop":
            # Swoop down then curve away
            t = self.move_timer
            self.pos_y += self.speed * dt
            if t > 1.5:
                self.pos_x += math.cos(self.move_phase) * self.speed * 0.8 * dt
        elif self.movement == "hover":
            # Move down to a position then hover
            target_y = 100 + random.Random(id(self)).random() * 200
            if self.pos_y < target_y:
                self.pos_y += self.speed * dt
            else:
                self.pos_x += math.sin(self.move_timer * 0.8 + self.move_phase) * 60 * dt
                self.pos_x = max(30, min(SCREEN_WIDTH - 30, self.pos_x))
        elif self.movement == "dive":
            # Fast dive toward player position
            self.pos_y += self.speed * 1.5 * dt
        elif self.movement == "stationary":
            # Just scroll slowly
            self.pos_y += 30 * dt

    def try_fire(self, projectile_group):
        if self.fire_timer <= 0 and self.entered_screen:
            self.fire_timer = self.fire_rate
            proj = create_enemy_projectile(
                self.assets, self.rect.centerx, self.rect.bottom, self.weapon_type
            )
            projectile_group.add(proj)
            sfx_key = f"enemy_{self.weapon_type}"
            self.assets.play_sound(sfx_key)
            return proj
        return None

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            return True
        return False


class Turret(Enemy):
    """Turret that rotates to aim at the player."""

    def __init__(self, assets, x, y, stage, groups):
        super().__init__(assets, "turret", x, y, stage, groups, movement="stationary")
        self.base_image = self.image
        self.turret_angle = 0

    def update(self, dt):
        super().update(dt)

    def try_fire_at(self, target, projectile_group):
        if self.fire_timer <= 0 and self.entered_screen and target.alive():
            self.fire_timer = self.fire_rate
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            angle = math.atan2(dy, dx)
            self.turret_angle = -math.degrees(angle) - 90

            proj = create_enemy_projectile(
                self.assets, self.rect.centerx, self.rect.bottom, self.weapon_type
            )
            proj.vel_x = math.cos(angle) * proj.speed
            proj.speed = abs(math.sin(angle) * proj.speed) if dy > 0 else proj.speed
            proj.direction = 1 if dy > 0 else -1
            projectile_group.add(proj)
            self.assets.play_sound("turret_laser")
            return proj
        return None


def spawn_enemy(assets, enemy_type, x, y, stage, groups, movement="straight"):
    if enemy_type == "turret":
        return Turret(assets, x, y, stage, groups)
    return Enemy(assets, enemy_type, x, y, stage, groups, movement)
