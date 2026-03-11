import math
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PROJECTILE_SPEED_BULLET, PROJECTILE_SPEED_LASER,
    PROJECTILE_SPEED_MISSILE, PROJECTILE_SPEED_HEAVY_MISSILE,
    PROJECTILE_SPEED_PLASMA, PROJECTILE_SPEED_HOMING,
    PROJECTILE_DAMAGE, ENEMY_PROJECTILE_SPEED,
)


class Projectile(pygame.sprite.Sprite):
    """Base projectile class."""

    def __init__(self, frames, x, y, speed, damage, direction=-1):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_rate = 0.05
        self.image = self.frames[0]
        if direction > 0:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_y = float(y)
        self.pos_x = float(x)
        self.speed = speed
        self.damage = damage
        self.direction = direction  # -1 = up (player), 1 = down (enemy)
        self.vel_x = 0

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            img = self.frames[self.frame_index]
            if self.direction > 0:
                img = pygame.transform.flip(img, False, True)
            self.image = img

        self.pos_y += self.speed * self.direction * dt
        self.pos_x += self.vel_x * dt
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        if (self.rect.bottom < -20 or self.rect.top > SCREEN_HEIGHT + 20
                or self.rect.right < -20 or self.rect.left > SCREEN_WIDTH + 20):
            self.kill()


class HomingProjectile(Projectile):
    """Projectile that tracks the nearest target."""

    def __init__(self, frames, x, y, speed, damage, targets, direction=-1):
        super().__init__(frames, x, y, speed, damage, direction)
        self.targets = targets
        self.turn_speed = 3.0
        angle = -90 if direction == -1 else 90
        self.angle = math.radians(angle)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        target = self._find_nearest()
        if target:
            dx = target.rect.centerx - self.pos_x
            dy = target.rect.centery - self.pos_y
            desired_angle = math.atan2(dy, dx)
            angle_diff = desired_angle - self.angle
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            self.angle += angle_diff * self.turn_speed * dt

        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        rot_angle = -math.degrees(self.angle) - 90
        self.image = pygame.transform.rotate(self.frames[self.frame_index], rot_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if (self.rect.bottom < -50 or self.rect.top > SCREEN_HEIGHT + 50
                or self.rect.right < -50 or self.rect.left > SCREEN_WIDTH + 50):
            self.kill()

    def _find_nearest(self):
        nearest = None
        min_dist = float("inf")
        for sprite in self.targets:
            if sprite.alive():
                dx = sprite.rect.centerx - self.pos_x
                dy = sprite.rect.centery - self.pos_y
                dist = dx * dx + dy * dy
                if dist < min_dist:
                    min_dist = dist
                    nearest = sprite
        return nearest


class Bomb(pygame.sprite.Sprite):
    """Screen-clearing bomb effect. Expands outward and damages all enemies."""

    def __init__(self, x, y):
        super().__init__()
        self.pos_x = x
        self.pos_y = y
        self.radius = 10
        self.max_radius = 400
        self.expand_speed = 800
        self.damage = PROJECTILE_DAMAGE["bomb"]
        self.damaged_sprites = set()
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.radius += self.expand_speed * dt
        if self.radius >= self.max_radius:
            self.kill()
            return
        self.image.fill((0, 0, 0, 0))
        alpha = max(0, int(180 * (1 - self.radius / self.max_radius)))
        pygame.draw.circle(
            self.image, (100, 200, 255, alpha),
            (self.max_radius, self.max_radius), int(self.radius), 4
        )
        pygame.draw.circle(
            self.image, (200, 230, 255, alpha // 2),
            (self.max_radius, self.max_radius), int(self.radius * 0.7)
        )


def create_player_bullet(assets, x, y):
    frames = assets.images["player_bullet"]
    return Projectile(frames, x, y, PROJECTILE_SPEED_BULLET, PROJECTILE_DAMAGE["bullet"])


def create_player_laser(assets, x, y):
    frames = assets.images["player_laser"]
    return Projectile(frames, x, y, PROJECTILE_SPEED_LASER, PROJECTILE_DAMAGE["laser"])


def create_player_missile(assets, x, y):
    frames = assets.images["player_missile"]
    return Projectile(frames, x, y, PROJECTILE_SPEED_MISSILE, PROJECTILE_DAMAGE["missile"])


def create_player_heavy_missile(assets, x, y):
    frames = assets.images["player_heavy_missile"]
    return Projectile(frames, x, y, PROJECTILE_SPEED_HEAVY_MISSILE, PROJECTILE_DAMAGE["heavy_missile"])


def create_player_plasma(assets, x, y):
    frames = assets.images["player_plasma"]
    return Projectile(frames, x, y, PROJECTILE_SPEED_PLASMA, PROJECTILE_DAMAGE["plasma"])


def create_homing_missile(assets, x, y, targets):
    frames = assets.images["player_missile"]
    return HomingProjectile(
        frames, x, y, PROJECTILE_SPEED_HOMING,
        PROJECTILE_DAMAGE["homing_missile"], targets
    )


def create_homing_laser(assets, x, y, targets):
    frames = assets.images["player_laser"]
    return HomingProjectile(
        frames, x, y, PROJECTILE_SPEED_HOMING * 1.2,
        PROJECTILE_DAMAGE["homing_laser"], targets
    )


def create_enemy_projectile(assets, x, y, weapon_type="laser"):
    weapon_map = {
        "laser": ("enemy_laser", PROJECTILE_SPEED_LASER * 0.6),
        "missile": ("enemy_missile", PROJECTILE_SPEED_MISSILE * 0.6),
        "plasma": ("enemy_plasma", PROJECTILE_SPEED_PLASMA * 0.6),
    }
    key, speed = weapon_map.get(weapon_type, weapon_map["laser"])
    frames = assets.images[key]
    return Projectile(frames, x, y, speed, 1, direction=1)
