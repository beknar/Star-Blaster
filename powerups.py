import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPEED


POWERUP_TYPES = [
    "weapon_upgrade",
    "shield",
    "homing_missile",
    "homing_laser",
    "bomb",
    "health",
]

# Weighted probabilities for each powerup type
POWERUP_WEIGHTS = {
    "weapon_upgrade": 30,
    "shield": 20,
    "homing_missile": 15,
    "homing_laser": 10,
    "bomb": 15,
    "health": 10,
}


class Powerup(pygame.sprite.Sprite):
    def __init__(self, assets, x, y, powerup_type=None):
        super().__init__()
        self.assets = assets

        if powerup_type is None:
            types = list(POWERUP_WEIGHTS.keys())
            weights = [POWERUP_WEIGHTS[t] for t in types]
            powerup_type = random.choices(types, weights=weights, k=1)[0]

        self.powerup_type = powerup_type
        self.image = self._get_image(powerup_type)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_y = float(y)
        self.speed = POWERUP_SPEED
        self.bob_timer = 0

    def _get_image(self, powerup_type):
        image_map = {
            "weapon_upgrade": "pickup_powerup",
            "shield": "pickup_shield",
            "homing_missile": "pickup_powerup",
            "homing_laser": "pickup_powerup",
            "bomb": "pickup_credits",
            "health": "pickup_health",
        }
        key = image_map.get(powerup_type, "pickup_powerup")
        return self.assets.images[key]

    def update(self, dt):
        self.bob_timer += dt
        self.pos_y += self.speed * dt
        # Gentle horizontal bob
        bob_x = self.rect.centerx
        self.rect.center = (bob_x, int(self.pos_y))

        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()

    def apply(self, player):
        self.assets.play_sound("pickup")
        if self.powerup_type == "weapon_upgrade":
            player.upgrade_weapon()
        elif self.powerup_type == "shield":
            player.activate_shield()
        elif self.powerup_type == "homing_missile":
            player.add_homing_missiles()
        elif self.powerup_type == "homing_laser":
            player.add_homing_lasers()
        elif self.powerup_type == "bomb":
            player.add_bomb()
        elif self.powerup_type == "health":
            if player.hp < 3:
                player.hp += 1
                player.is_damaged = player.hp < 3
        self.kill()


def maybe_drop_powerup(assets, x, y, drop_chance=0.2):
    if random.random() < drop_chance:
        return Powerup(assets, x, y)
    return None
