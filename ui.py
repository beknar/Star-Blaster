import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, RED, GREEN, CYAN, BLACK


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 20)
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_large = pygame.font.SysFont("consolas", 48)
        self.font_title = pygame.font.SysFont("consolas", 64)
        self.font_medium = pygame.font.SysFont("consolas", 28)

    def draw_gameplay_hud(self, screen, player, stage_manager):
        # Score
        score_text = self.font.render(f"Score: {player.score:,}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Stage / Wave
        stage_text = self.font_small.render(
            f"Stage {stage_manager.stage_number} - Wave {stage_manager.wave_number}",
            True, CYAN
        )
        screen.blit(stage_text, (10, 35))

        # Lives
        lives_text = self.font.render(f"Lives: {player.lives}", True, GREEN)
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        # HP bar
        hp_bar_x = SCREEN_WIDTH - 120
        hp_bar_y = 35
        hp_bar_w = 100
        hp_bar_h = 10
        pygame.draw.rect(screen, (60, 60, 60), (hp_bar_x, hp_bar_y, hp_bar_w, hp_bar_h))
        hp_frac = max(0, player.hp / 3)
        hp_color = GREEN if hp_frac > 0.5 else YELLOW if hp_frac > 0.25 else RED
        pygame.draw.rect(screen, hp_color, (hp_bar_x, hp_bar_y, int(hp_bar_w * hp_frac), hp_bar_h))

        # Bombs
        if player.bombs > 0:
            bomb_text = self.font_small.render(f"Bombs: {player.bombs}", True, YELLOW)
            screen.blit(bomb_text, (SCREEN_WIDTH - 120, 50))

        # Active upgrades
        upgrades = []
        if player.weapon_level > 0:
            upgrades.append(f"WPN Lv{player.weapon_level}")
        if player.shield_hp > 0:
            upgrades.append(f"SHIELD:{player.shield_hp}")
        if player.has_homing_missiles:
            upgrades.append("HOMING")
        if player.has_homing_lasers:
            upgrades.append("H-LASER")

        if upgrades:
            upgrade_text = self.font_small.render("  ".join(upgrades), True, CYAN)
            screen.blit(upgrade_text, (10, SCREEN_HEIGHT - 25))

    def draw_menu(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        title = self.font_title.render("SPACE SHOOTER", True, CYAN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        instructions = [
            "Arrow Keys / WASD - Move",
            "SPACE - Fire",
            "B - Bomb",
            "P - Pause",
            "",
            "Press ENTER to Start",
        ]
        for i, line in enumerate(instructions):
            color = GREEN if line.startswith("Press") else WHITE
            text = self.font.render(line, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 35))

    def draw_pause(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))

        text = self.font_large.render("PAUSED", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))

        resume = self.font.render("Press P to Resume", True, GREEN)
        screen.blit(resume, (SCREEN_WIDTH // 2 - resume.get_width() // 2, 330))

    def draw_game_over(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        go_text = self.font_title.render("GAME OVER", True, RED)
        screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 180))

        score_text = self.font_large.render(f"Score: {score:,}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))

        restart = self.font.render("Press ENTER to Restart", True, GREEN)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 370))

        quit_text = self.font.render("Press ESC to Quit", True, YELLOW)
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 410))

    def draw_stage_transition(self, screen, stage_number):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        text = self.font_large.render(f"STAGE {stage_number}", True, CYAN)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240))

        ready = self.font.render("Get Ready!", True, WHITE)
        screen.blit(ready, (SCREEN_WIDTH // 2 - ready.get_width() // 2, 310))

    def draw_wave_banner(self, screen, wave_number):
        text = self.font_medium.render(f"Wave {wave_number}", True, YELLOW)
        text.set_alpha(200)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 80))

    def draw_win(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        win_text = self.font_title.render("VICTORY!", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 180))

        score_text = self.font_large.render(f"Final Score: {score:,}", True, CYAN)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 280))

        restart = self.font.render("Press ENTER to Play Again", True, GREEN)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 370))

        quit_text = self.font.render("Press ESC to Quit", True, YELLOW)
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 410))
