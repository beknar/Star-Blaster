import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class AnimatedSprite(pygame.sprite.Sprite):
    """Base class for frame-based animations."""

    def __init__(self, frames, x, y, frame_rate=0.05, loop=False):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_rate = frame_rate
        self.loop = loop
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.kill()
                    return
            self.image = self.frames[self.frame_index]
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)


class Explosion(AnimatedSprite):
    def __init__(self, frames, x, y, sound=None):
        super().__init__(frames, x, y, frame_rate=0.04)
        if sound:
            sound.play()


class ShieldEffect(pygame.sprite.Sprite):
    """Shield visual overlay that follows the player."""

    def __init__(self, frames, owner):
        super().__init__()
        self.frames = frames
        self.owner = owner
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_rate = 0.06
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=self.owner.rect.center)

    def update(self, dt):
        if not self.owner.alive() or not self.owner.shield_hp:
            self.kill()
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.owner.rect.center)


class ThrusterEffect(pygame.sprite.Sprite):
    """Looping thruster animation attached to a ship."""

    def __init__(self, frames, owner, offset_y):
        super().__init__()
        self.frames = frames
        self.owner = owner
        self.offset_y = offset_y
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_rate = 0.05
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def update(self, dt):
        if not self.owner.alive():
            self.kill()
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(
            centerx=self.owner.rect.centerx,
            top=self.owner.rect.bottom + self.offset_y,
        )


class MuzzleFlash(AnimatedSprite):
    """Brief muzzle flash at weapon fire point."""

    def __init__(self, frames, x, y):
        super().__init__(frames, x, y, frame_rate=0.03)


class ScreenShake:
    """Manages screen shake offset."""

    def __init__(self):
        self.duration = 0
        self.intensity = 0
        self.offset_x = 0
        self.offset_y = 0

    def start(self, duration=0.3, intensity=8):
        self.duration = duration
        self.intensity = intensity

    def update(self, dt):
        if self.duration > 0:
            self.duration -= dt
            import random
            self.offset_x = random.randint(-self.intensity, self.intensity)
            self.offset_y = random.randint(-self.intensity, self.intensity)
        else:
            self.offset_x = 0
            self.offset_y = 0

    @property
    def offset(self):
        return (self.offset_x, self.offset_y)


class DamageFlash:
    """Brief screen tint when player takes damage."""

    def __init__(self):
        self.duration = 0
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.fill((255, 0, 0))

    def start(self, duration=0.1):
        self.duration = duration

    def update(self, dt):
        if self.duration > 0:
            self.duration -= dt

    def draw(self, screen):
        if self.duration > 0:
            alpha = int(80 * (self.duration / 0.1))
            self.surface.set_alpha(min(alpha, 80))
            screen.blit(self.surface, (0, 0))
