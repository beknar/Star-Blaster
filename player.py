import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_HP,
    PLAYER_FIRE_RATE, PLAYER_INVULN_TIME, PLAYER_START_LIVES,
    SHIELD_HP, BOMB_MAX,
)
from weapons import (
    create_player_bullet, create_player_laser, create_player_missile,
    create_player_heavy_missile, create_player_plasma,
    create_homing_missile, create_homing_laser, Bomb,
)
from effects import ShieldEffect, ThrusterEffect, MuzzleFlash


class Player(pygame.sprite.Sprite):
    def __init__(self, assets, groups):
        super().__init__()
        self.assets = assets
        self.groups_ref = groups

        # Ship images
        self.img_normal = assets.images["player_medium"]
        self.img_tilt = assets.images.get("player_medium_tilt")
        self.fire_frames = assets.images.get("player_medium_fire", [])

        self.image = self.img_normal
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 20)
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

        # Stats
        self.hp = PLAYER_HP
        self.lives = PLAYER_START_LIVES
        self.speed = PLAYER_SPEED
        self.fire_rate = PLAYER_FIRE_RATE
        self.fire_timer = 0

        # Invulnerability
        self.invuln_timer = 0
        self.invuln_blink = 0

        # Upgrades
        self.weapon_level = 0  # 0=single, 1=double, 2=triple, 3=spread
        self.has_homing_missiles = False
        self.has_homing_lasers = False
        self.shield_hp = 0
        self.bombs = 0
        self.bomb_max = BOMB_MAX

        # Thruster effect
        thruster_frames = assets.images.get("thruster_player", [])
        if thruster_frames:
            self.thruster = ThrusterEffect(thruster_frames, self, -5)
            groups["effects"].add(self.thruster)
        else:
            self.thruster = None

        # Shield visual
        self.shield_effect = None

        # Damage state
        self.damage_frame_index = 0
        self.damage_frame_timer = 0
        self.is_damaged = False

    def update(self, dt):
        # Fire timer cooldown
        if self.fire_timer > 0:
            self.fire_timer -= dt

        # Invulnerability
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
            self.invuln_blink += dt
            if self.invuln_blink > 0.1:
                self.invuln_blink = 0
                self.image.set_alpha(100 if self.image.get_alpha() == 255 else 255)
        else:
            self.image.set_alpha(255)

        # Damage animation
        if self.is_damaged and self.fire_frames:
            self.damage_frame_timer += dt
            if self.damage_frame_timer >= 0.08:
                self.damage_frame_timer = 0
                self.damage_frame_index = (self.damage_frame_index + 1) % len(self.fire_frames)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.pos_x += dx * self.speed * dt
        self.pos_y += dy * self.speed * dt

        # Clamp to screen
        half_w = self.rect.width // 2
        half_h = self.rect.height // 2
        self.pos_x = max(half_w, min(SCREEN_WIDTH - half_w, self.pos_x))
        self.pos_y = max(half_h, min(SCREEN_HEIGHT - half_h, self.pos_y))

        self.rect.center = (int(self.pos_x), int(self.pos_y))

        # Pick correct image based on tilt
        if dx < 0 and self.img_tilt:
            self.image = pygame.transform.flip(self.img_tilt, True, False)
        elif dx > 0 and self.img_tilt:
            self.image = self.img_tilt
        elif self.is_damaged and self.fire_frames:
            self.image = self.fire_frames[self.damage_frame_index]
        else:
            self.image = self.img_normal

    def fire(self, projectile_group, enemy_group):
        if self.fire_timer > 0:
            return []

        self.fire_timer = self.fire_rate
        new_projectiles = []
        cx = self.rect.centerx
        top = self.rect.top

        # Base weapon
        if self.weapon_level == 0:
            p = create_player_bullet(self.assets, cx, top)
            new_projectiles.append(p)
        elif self.weapon_level == 1:
            p1 = create_player_bullet(self.assets, cx - 12, top)
            p2 = create_player_bullet(self.assets, cx + 12, top)
            new_projectiles.extend([p1, p2])
        elif self.weapon_level == 2:
            p1 = create_player_bullet(self.assets, cx - 16, top)
            p2 = create_player_bullet(self.assets, cx, top)
            p3 = create_player_bullet(self.assets, cx + 16, top)
            new_projectiles.extend([p1, p2, p3])
        else:  # level 3+ spread
            p1 = create_player_bullet(self.assets, cx, top)
            p2 = create_player_bullet(self.assets, cx - 16, top)
            p3 = create_player_bullet(self.assets, cx + 16, top)
            p2.vel_x = -60
            p3.vel_x = 60
            p4 = create_player_bullet(self.assets, cx - 28, top + 5)
            p5 = create_player_bullet(self.assets, cx + 28, top + 5)
            p4.vel_x = -120
            p5.vel_x = 120
            new_projectiles.extend([p1, p2, p3, p4, p5])

        # Homing missiles
        if self.has_homing_missiles:
            hm = create_homing_missile(self.assets, cx, top, enemy_group)
            new_projectiles.append(hm)

        # Homing lasers
        if self.has_homing_lasers:
            hl = create_homing_laser(self.assets, cx, top, enemy_group)
            new_projectiles.append(hl)

        for p in new_projectiles:
            projectile_group.add(p)

        self.assets.play_sound("player_bullet")

        # Muzzle flash
        emit_frames = self.assets.images.get("player_bullet_emit")
        if emit_frames:
            flash = MuzzleFlash(emit_frames, cx, top - 5)
            self.groups_ref["effects"].add(flash)

        return new_projectiles

    def fire_bomb(self, bomb_group, enemy_group):
        if self.bombs <= 0:
            return None
        self.bombs -= 1
        bomb = Bomb(self.rect.centerx, self.rect.centery)
        bomb_group.add(bomb)
        self.assets.play_sound("explosion_big")
        return bomb

    def take_damage(self, amount=1):
        if self.invuln_timer > 0:
            return False

        # Shield absorbs damage first
        if self.shield_hp > 0:
            self.shield_hp -= amount
            if self.shield_hp <= 0:
                self.shield_hp = 0
                if self.shield_effect:
                    self.shield_effect.kill()
                    self.shield_effect = None
                self.assets.play_sound("shield_end")
            return True

        self.hp -= amount
        self.is_damaged = self.hp < PLAYER_HP
        self.invuln_timer = PLAYER_INVULN_TIME

        if self.hp <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.kill()
            return True
        return True

    def respawn(self):
        self.hp = PLAYER_HP
        self.is_damaged = False
        self.pos_x = SCREEN_WIDTH // 2
        self.pos_y = SCREEN_HEIGHT - 60
        self.rect.center = (int(self.pos_x), int(self.pos_y))
        self.invuln_timer = PLAYER_INVULN_TIME * 2
        self.image = self.img_normal

    def activate_shield(self):
        self.shield_hp = SHIELD_HP
        self.assets.play_sound("shield_start")
        shield_frames = self.assets.images.get("shield_effect")
        if shield_frames:
            self.shield_effect = ShieldEffect(shield_frames, self)
            self.groups_ref["effects"].add(self.shield_effect)

    def upgrade_weapon(self):
        if self.weapon_level < 3:
            self.weapon_level += 1
            self.assets.play_sound("player_upgrade")

    def add_bomb(self):
        if self.bombs < self.bomb_max:
            self.bombs += 1

    def add_homing_missiles(self):
        self.has_homing_missiles = True
        self.assets.play_sound("player_upgrade")

    def add_homing_lasers(self):
        self.has_homing_lasers = True
        self.assets.play_sound("player_upgrade")

    def add_life(self):
        self.lives += 1
