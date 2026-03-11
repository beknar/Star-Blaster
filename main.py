import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED,
    STATE_GAME_OVER, STATE_STAGE_TRANSITION, STATE_WIN,
    BG_SCROLL_SPEED, EXTRA_LIFE_SCORES,
)
from assets import AssetManager
from player import Player
from enemies import Enemy, Turret
from weapons import Bomb
from powerups import maybe_drop_powerup
from effects import Explosion, ScreenShake, DamageFlash
from stages import StageManager
from ui import HUD


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Load all assets
        self.assets = AssetManager()
        self.assets.load_all()

        # Effects
        self.screen_shake = ScreenShake()
        self.damage_flash = DamageFlash()
        self.hud = HUD()

        # Background scrolling
        self.bg_image = None
        self.bg_y1 = 0
        self.bg_y2 = 0

        self.state = STATE_MENU
        self.transition_timer = 0
        self.wave_banner_timer = 0
        self.score = 0
        self.extra_life_index = 0

        # Sprite groups
        self.groups = {
            "player": pygame.sprite.GroupSingle(),
            "enemies": pygame.sprite.Group(),
            "player_projectiles": pygame.sprite.Group(),
            "enemy_projectiles": pygame.sprite.Group(),
            "powerups": pygame.sprite.Group(),
            "effects": pygame.sprite.Group(),
            "bombs": pygame.sprite.Group(),
        }

        self.player = None
        self.stage_manager = None

    def new_game(self):
        # Clear all groups
        for group in self.groups.values():
            group.empty()

        self.score = 0
        self.extra_life_index = 0

        # Create player
        self.player = Player(self.assets, self.groups)
        self.player.score = 0
        self.groups["player"].add(self.player)

        # Stage manager
        self.stage_manager = StageManager(self.assets, self.groups)
        self.stage_manager.start_stage(0)

        # Set background
        self._update_background()

        # Music
        self.assets.play_music("track1")

        self.state = STATE_STAGE_TRANSITION
        self.transition_timer = 2.0
        self.wave_banner_timer = 2.0

    def _update_background(self):
        self.bg_image = self.stage_manager.get_background()
        if self.bg_image:
            self.bg_y1 = 0
            self.bg_y2 = -self.bg_image.get_height()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # Cap delta time

            self._handle_events()

            if self.state == STATE_MENU:
                self._update_menu(dt)
            elif self.state == STATE_PLAYING:
                self._update_playing(dt)
            elif self.state == STATE_PAUSED:
                pass
            elif self.state == STATE_GAME_OVER:
                pass
            elif self.state == STATE_STAGE_TRANSITION:
                self._update_stage_transition(dt)
            elif self.state == STATE_WIN:
                pass

            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                    elif event.key == pygame.K_b:
                        self.player.fire_bomb(
                            self.groups["bombs"], self.groups["enemies"]
                        )
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                elif self.state == STATE_PAUSED:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = STATE_PLAYING

                elif self.state in (STATE_GAME_OVER, STATE_WIN):
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def _update_menu(self, dt):
        self._scroll_background(dt)

    def _update_stage_transition(self, dt):
        self._scroll_background(dt)
        self.transition_timer -= dt
        if self.transition_timer <= 0:
            self.state = STATE_PLAYING
            self.wave_banner_timer = 2.0

    def _update_playing(self, dt):
        if not self.player.alive():
            self.state = STATE_GAME_OVER
            self.assets.play_music("track1_lose")
            return

        # Background scroll
        self._scroll_background(dt)

        # Player input and update
        self.player.handle_input(dt)
        self.player.update(dt)

        # Continuous fire while space held
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.fire(self.groups["player_projectiles"], self.groups["enemies"])

        # Update stage/wave spawning
        self.stage_manager.update(dt, self.groups["enemies"])

        # Update all sprite groups
        self.groups["player_projectiles"].update(dt)
        self.groups["enemy_projectiles"].update(dt)
        self.groups["enemies"].update(dt)
        self.groups["powerups"].update(dt)
        self.groups["effects"].update(dt)
        self.groups["bombs"].update(dt)

        # Enemy firing
        for enemy in self.groups["enemies"]:
            if isinstance(enemy, Turret):
                enemy.try_fire_at(self.player, self.groups["enemy_projectiles"])
            else:
                enemy.try_fire(self.groups["enemy_projectiles"])

        # --- Collisions ---
        self._handle_collisions()

        # --- Bomb damage ---
        self._handle_bomb_damage()

        # --- Extra lives ---
        self._check_extra_lives()

        # --- Stage progression ---
        if self.stage_manager.stage_complete:
            if self.stage_manager.all_stages_complete:
                self.state = STATE_WIN
                self.assets.play_music("track1_win")
            elif len(self.groups["enemies"]) == 0:
                self.stage_manager.advance_stage()
                if self.stage_manager.all_stages_complete:
                    self.state = STATE_WIN
                    self.assets.play_music("track1_win")
                else:
                    self._update_background()
                    self.state = STATE_STAGE_TRANSITION
                    self.transition_timer = 2.5

        # Wave banner timer
        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

        # Screen effects
        self.screen_shake.update(dt)
        self.damage_flash.update(dt)

    def _handle_collisions(self):
        # Player projectiles vs enemies
        hits = pygame.sprite.groupcollide(
            self.groups["player_projectiles"], self.groups["enemies"],
            False, False
        )
        for proj, enemies_hit in hits.items():
            for enemy in enemies_hit:
                killed = enemy.take_damage(proj.damage)
                proj.kill()
                if killed:
                    self._on_enemy_killed(enemy)
                break  # Each projectile hits one enemy

        # Enemy projectiles vs player
        if self.player.alive():
            hits = pygame.sprite.spritecollide(
                self.player, self.groups["enemy_projectiles"], True
            )
            if hits and self.player.invuln_timer <= 0:
                self.player.take_damage(1)
                self.damage_flash.start()
                self.screen_shake.start(0.2, 5)

        # Enemy ships vs player (collision damage)
        if self.player.alive():
            hits = pygame.sprite.spritecollide(
                self.player, self.groups["enemies"], False
            )
            for enemy in hits:
                if self.player.invuln_timer <= 0:
                    self.player.take_damage(1)
                    enemy.take_damage(2)
                    self.damage_flash.start()
                    self.screen_shake.start(0.3, 8)
                    if enemy.hp <= 0:
                        self._on_enemy_killed(enemy)
                    break

        # Player vs powerups
        if self.player.alive():
            hits = pygame.sprite.spritecollide(
                self.player, self.groups["powerups"], False
            )
            for powerup in hits:
                powerup.apply(self.player)

    def _handle_bomb_damage(self):
        for bomb in self.groups["bombs"]:
            for enemy in self.groups["enemies"]:
                if id(enemy) not in bomb.damaged_sprites:
                    dx = enemy.rect.centerx - bomb.pos_x
                    dy = enemy.rect.centery - bomb.pos_y
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist <= bomb.radius:
                        bomb.damaged_sprites.add(id(enemy))
                        killed = enemy.take_damage(bomb.damage)
                        if killed:
                            self._on_enemy_killed(enemy)

        # Bombs also clear enemy projectiles
        for bomb in self.groups["bombs"]:
            for proj in list(self.groups["enemy_projectiles"]):
                dx = proj.rect.centerx - bomb.pos_x
                dy = proj.rect.centery - bomb.pos_y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist <= bomb.radius:
                    proj.kill()

    def _on_enemy_killed(self, enemy):
        self.score += enemy.points
        self.player.score = self.score

        # Explosion
        is_big = enemy.enemy_type in ("heavy", "tank")
        exp_key = "explosion_big" if is_big else "explosion_small"
        sfx_key = "explosion_big" if is_big else "explosion_small"
        frames = self.assets.images.get(exp_key, [])
        if frames:
            exp = Explosion(frames, enemy.rect.centerx, enemy.rect.centery)
            self.groups["effects"].add(exp)
        self.assets.play_sound(sfx_key)

        if is_big:
            self.screen_shake.start(0.3, 6)

        # Maybe drop powerup
        drop_chance = 0.15 if enemy.enemy_type == "scout" else 0.25
        powerup = maybe_drop_powerup(self.assets, enemy.rect.centerx, enemy.rect.centery, drop_chance)
        if powerup:
            self.groups["powerups"].add(powerup)

    def _check_extra_lives(self):
        while (self.extra_life_index < len(EXTRA_LIFE_SCORES)
               and self.score >= EXTRA_LIFE_SCORES[self.extra_life_index]):
            self.player.add_life()
            self.extra_life_index += 1

    def _scroll_background(self, dt):
        if self.bg_image is None:
            return
        self.bg_y1 += BG_SCROLL_SPEED * dt
        self.bg_y2 += BG_SCROLL_SPEED * dt
        bg_h = self.bg_image.get_height()
        if self.bg_y1 >= bg_h:
            self.bg_y1 = self.bg_y2 - bg_h
        if self.bg_y2 >= bg_h:
            self.bg_y2 = self.bg_y1 - bg_h

    def _draw(self):
        self.screen.fill((5, 5, 15))

        # Background
        shake_x, shake_y = self.screen_shake.offset
        if self.bg_image:
            self.screen.blit(self.bg_image, (shake_x, int(self.bg_y1) + shake_y))
            self.screen.blit(self.bg_image, (shake_x, int(self.bg_y2) + shake_y))

        if self.state == STATE_MENU:
            self.hud.draw_menu(self.screen)
        else:
            # Draw game objects with shake offset
            self._draw_group(self.groups["powerups"], shake_x, shake_y)
            self._draw_group(self.groups["enemies"], shake_x, shake_y)
            self._draw_group(self.groups["player"], shake_x, shake_y)
            self._draw_group(self.groups["player_projectiles"], shake_x, shake_y)
            self._draw_group(self.groups["enemy_projectiles"], shake_x, shake_y)
            self._draw_group(self.groups["effects"], shake_x, shake_y)
            self._draw_group(self.groups["bombs"], shake_x, shake_y)

            # Damage flash overlay
            self.damage_flash.draw(self.screen)

            # HUD
            if self.player and self.player.alive():
                self.hud.draw_gameplay_hud(self.screen, self.player, self.stage_manager)

            # Wave banner
            if self.wave_banner_timer > 0 and self.state == STATE_PLAYING:
                self.hud.draw_wave_banner(self.screen, self.stage_manager.wave_number)

            # State overlays
            if self.state == STATE_PAUSED:
                self.hud.draw_pause(self.screen)
            elif self.state == STATE_GAME_OVER:
                self.hud.draw_game_over(self.screen, self.score)
            elif self.state == STATE_STAGE_TRANSITION:
                self.hud.draw_stage_transition(self.screen, self.stage_manager.stage_number)
            elif self.state == STATE_WIN:
                self.hud.draw_win(self.screen, self.score)

        pygame.display.flip()

    def _draw_group(self, group, offset_x=0, offset_y=0):
        if offset_x == 0 and offset_y == 0:
            group.draw(self.screen)
        else:
            for sprite in group:
                self.screen.blit(sprite.image, (
                    sprite.rect.x + offset_x,
                    sprite.rect.y + offset_y,
                ))


if __name__ == "__main__":
    game = Game()
    game.run()
