import random
from settings import SCREEN_WIDTH
from enemies import spawn_enemy


# Each wave definition: list of (enemy_type, x_position, movement_pattern)
# x positions use fractions of screen width for flexibility

def _x(frac):
    return int(SCREEN_WIDTH * frac)


# --- STAGE 1: Introduction ---
STAGE_1_WAVES = [
    # Wave 1: Simple scouts in a line
    {
        "enemies": [
            ("scout", _x(0.2), "straight"),
            ("scout", _x(0.4), "straight"),
            ("scout", _x(0.6), "straight"),
            ("scout", _x(0.8), "straight"),
        ],
        "delay": 0.3,
    },
    # Wave 2: Scouts in zigzag
    {
        "enemies": [
            ("scout", _x(0.15), "zigzag"),
            ("scout", _x(0.35), "zigzag"),
            ("scout", _x(0.55), "zigzag"),
            ("scout", _x(0.75), "zigzag"),
            ("scout", _x(0.5), "straight"),
        ],
        "delay": 0.4,
    },
    # Wave 3: Introducing fighters
    {
        "enemies": [
            ("scout", _x(0.2), "zigzag"),
            ("scout", _x(0.8), "zigzag"),
            ("fighter", _x(0.5), "straight"),
        ],
        "delay": 0.5,
    },
    # Wave 4: Mixed scouts and fighters
    {
        "enemies": [
            ("fighter", _x(0.3), "sine"),
            ("fighter", _x(0.7), "sine"),
            ("scout", _x(0.1), "straight"),
            ("scout", _x(0.5), "straight"),
            ("scout", _x(0.9), "straight"),
        ],
        "delay": 0.3,
    },
    # Wave 5: First challenge
    {
        "enemies": [
            ("fighter", _x(0.3), "zigzag"),
            ("fighter", _x(0.5), "straight"),
            ("fighter", _x(0.7), "zigzag"),
            ("scout", _x(0.15), "dive"),
            ("scout", _x(0.85), "dive"),
            ("scout", _x(0.5), "sine"),
        ],
        "delay": 0.4,
    },
]

# --- STAGE 2: Escalation ---
STAGE_2_WAVES = [
    # Wave 1: Fighters in formation
    {
        "enemies": [
            ("fighter", _x(0.2), "straight"),
            ("fighter", _x(0.4), "straight"),
            ("fighter", _x(0.6), "straight"),
            ("fighter", _x(0.8), "straight"),
        ],
        "delay": 0.3,
    },
    # Wave 2: Swooping scouts with fighter support
    {
        "enemies": [
            ("scout", _x(0.1), "swoop"),
            ("scout", _x(0.3), "swoop"),
            ("scout", _x(0.7), "swoop"),
            ("scout", _x(0.9), "swoop"),
            ("fighter", _x(0.5), "hover"),
        ],
        "delay": 0.25,
    },
    # Wave 3: Introducing heavies
    {
        "enemies": [
            ("heavy", _x(0.5), "straight"),
            ("scout", _x(0.2), "zigzag"),
            ("scout", _x(0.8), "zigzag"),
            ("fighter", _x(0.35), "sine"),
            ("fighter", _x(0.65), "sine"),
        ],
        "delay": 0.5,
    },
    # Wave 4: Turret defense
    {
        "enemies": [
            ("turret", _x(0.3), "stationary"),
            ("turret", _x(0.7), "stationary"),
            ("scout", _x(0.15), "dive"),
            ("scout", _x(0.5), "dive"),
            ("scout", _x(0.85), "dive"),
        ],
        "delay": 0.4,
    },
    # Wave 5: Stage 2 climax
    {
        "enemies": [
            ("heavy", _x(0.3), "hover"),
            ("heavy", _x(0.7), "hover"),
            ("fighter", _x(0.15), "zigzag"),
            ("fighter", _x(0.85), "zigzag"),
            ("scout", _x(0.4), "dive"),
            ("scout", _x(0.6), "dive"),
            ("scout", _x(0.5), "straight"),
        ],
        "delay": 0.35,
    },
]

# --- STAGE 3: Deep Space ---
STAGE_3_WAVES = [
    # Wave 1: Dive bombers
    {
        "enemies": [
            ("scout", _x(0.15), "dive"),
            ("scout", _x(0.3), "dive"),
            ("scout", _x(0.5), "dive"),
            ("scout", _x(0.7), "dive"),
            ("scout", _x(0.85), "dive"),
            ("fighter", _x(0.4), "hover"),
            ("fighter", _x(0.6), "hover"),
        ],
        "delay": 0.2,
    },
    # Wave 2: Tank introduction
    {
        "enemies": [
            ("tank", _x(0.5), "hover"),
            ("fighter", _x(0.2), "zigzag"),
            ("fighter", _x(0.8), "zigzag"),
            ("scout", _x(0.35), "swoop"),
            ("scout", _x(0.65), "swoop"),
        ],
        "delay": 0.5,
    },
    # Wave 3: Mixed assault
    {
        "enemies": [
            ("heavy", _x(0.3), "sine"),
            ("heavy", _x(0.7), "sine"),
            ("fighter", _x(0.5), "straight"),
            ("scout", _x(0.1), "dive"),
            ("scout", _x(0.9), "dive"),
            ("turret", _x(0.4), "stationary"),
            ("turret", _x(0.6), "stationary"),
        ],
        "delay": 0.3,
    },
    # Wave 4: Turret fortress
    {
        "enemies": [
            ("turret", _x(0.2), "stationary"),
            ("turret", _x(0.4), "stationary"),
            ("turret", _x(0.6), "stationary"),
            ("turret", _x(0.8), "stationary"),
            ("fighter", _x(0.3), "swoop"),
            ("fighter", _x(0.7), "swoop"),
        ],
        "delay": 0.3,
    },
    # Wave 5: Stage 3 boss wave
    {
        "enemies": [
            ("tank", _x(0.3), "hover"),
            ("tank", _x(0.7), "hover"),
            ("heavy", _x(0.5), "hover"),
            ("fighter", _x(0.15), "zigzag"),
            ("fighter", _x(0.85), "zigzag"),
            ("scout", _x(0.4), "dive"),
            ("scout", _x(0.6), "dive"),
            ("scout", _x(0.5), "swoop"),
        ],
        "delay": 0.3,
    },
]

# --- STAGE 4: Enemy Territory ---
STAGE_4_WAVES = [
    {
        "enemies": [
            ("fighter", _x(0.1), "sine"),
            ("fighter", _x(0.3), "sine"),
            ("fighter", _x(0.5), "sine"),
            ("fighter", _x(0.7), "sine"),
            ("fighter", _x(0.9), "sine"),
            ("heavy", _x(0.4), "straight"),
            ("heavy", _x(0.6), "straight"),
        ],
        "delay": 0.25,
    },
    {
        "enemies": [
            ("tank", _x(0.5), "hover"),
            ("turret", _x(0.2), "stationary"),
            ("turret", _x(0.8), "stationary"),
            ("scout", _x(0.3), "dive"),
            ("scout", _x(0.4), "dive"),
            ("scout", _x(0.6), "dive"),
            ("scout", _x(0.7), "dive"),
        ],
        "delay": 0.2,
    },
    {
        "enemies": [
            ("heavy", _x(0.2), "hover"),
            ("heavy", _x(0.5), "hover"),
            ("heavy", _x(0.8), "hover"),
            ("fighter", _x(0.35), "swoop"),
            ("fighter", _x(0.65), "swoop"),
            ("scout", _x(0.1), "zigzag"),
            ("scout", _x(0.9), "zigzag"),
        ],
        "delay": 0.3,
    },
    {
        "enemies": [
            ("tank", _x(0.3), "hover"),
            ("tank", _x(0.7), "hover"),
            ("turret", _x(0.1), "stationary"),
            ("turret", _x(0.5), "stationary"),
            ("turret", _x(0.9), "stationary"),
            ("fighter", _x(0.2), "dive"),
            ("fighter", _x(0.8), "dive"),
        ],
        "delay": 0.3,
    },
    {
        "enemies": [
            ("tank", _x(0.5), "hover"),
            ("heavy", _x(0.2), "sine"),
            ("heavy", _x(0.8), "sine"),
            ("fighter", _x(0.3), "zigzag"),
            ("fighter", _x(0.4), "zigzag"),
            ("fighter", _x(0.6), "zigzag"),
            ("fighter", _x(0.7), "zigzag"),
            ("scout", _x(0.15), "dive"),
            ("scout", _x(0.85), "dive"),
        ],
        "delay": 0.25,
    },
]

# --- STAGE 5: Final Assault ---
STAGE_5_WAVES = [
    {
        "enemies": [
            ("heavy", _x(0.2), "zigzag"),
            ("heavy", _x(0.4), "zigzag"),
            ("heavy", _x(0.6), "zigzag"),
            ("heavy", _x(0.8), "zigzag"),
            ("scout", _x(0.1), "dive"),
            ("scout", _x(0.5), "dive"),
            ("scout", _x(0.9), "dive"),
        ],
        "delay": 0.2,
    },
    {
        "enemies": [
            ("tank", _x(0.3), "hover"),
            ("tank", _x(0.7), "hover"),
            ("turret", _x(0.15), "stationary"),
            ("turret", _x(0.5), "stationary"),
            ("turret", _x(0.85), "stationary"),
            ("fighter", _x(0.25), "swoop"),
            ("fighter", _x(0.75), "swoop"),
        ],
        "delay": 0.3,
    },
    {
        "enemies": [
            ("heavy", _x(0.3), "hover"),
            ("heavy", _x(0.5), "hover"),
            ("heavy", _x(0.7), "hover"),
            ("fighter", _x(0.1), "dive"),
            ("fighter", _x(0.2), "dive"),
            ("fighter", _x(0.8), "dive"),
            ("fighter", _x(0.9), "dive"),
            ("turret", _x(0.4), "stationary"),
            ("turret", _x(0.6), "stationary"),
        ],
        "delay": 0.2,
    },
    {
        "enemies": [
            ("tank", _x(0.2), "hover"),
            ("tank", _x(0.5), "hover"),
            ("tank", _x(0.8), "hover"),
            ("heavy", _x(0.35), "sine"),
            ("heavy", _x(0.65), "sine"),
            ("scout", _x(0.15), "dive"),
            ("scout", _x(0.3), "dive"),
            ("scout", _x(0.7), "dive"),
            ("scout", _x(0.85), "dive"),
        ],
        "delay": 0.25,
    },
    {
        "enemies": [
            ("tank", _x(0.3), "hover"),
            ("tank", _x(0.5), "hover"),
            ("tank", _x(0.7), "hover"),
            ("heavy", _x(0.15), "zigzag"),
            ("heavy", _x(0.85), "zigzag"),
            ("fighter", _x(0.25), "swoop"),
            ("fighter", _x(0.4), "dive"),
            ("fighter", _x(0.6), "dive"),
            ("fighter", _x(0.75), "swoop"),
            ("turret", _x(0.1), "stationary"),
            ("turret", _x(0.9), "stationary"),
        ],
        "delay": 0.2,
    },
]

ALL_STAGES = [
    STAGE_1_WAVES,
    STAGE_2_WAVES,
    STAGE_3_WAVES,
    STAGE_4_WAVES,
    STAGE_5_WAVES,
]

# Background assignment per stage (index into backgrounds list)
STAGE_BACKGROUNDS = [0, 2, 4, 6, 8]


class StageManager:
    def __init__(self, assets, groups):
        self.assets = assets
        self.groups_ref = groups
        self.current_stage = 0  # 0-indexed
        self.current_wave = 0
        self.wave_active = False
        self.wave_enemies_spawned = False
        self.spawn_timer = 0
        self.spawn_index = 0
        self.spawn_delay = 0
        self.wave_delay_timer = 0  # Delay between waves
        self.stage_complete = False
        self.all_stages_complete = False
        self.current_wave_data = None

    @property
    def stage_number(self):
        return self.current_stage + 1

    @property
    def wave_number(self):
        return self.current_wave + 1

    @property
    def total_stages(self):
        return len(ALL_STAGES)

    def get_background(self):
        bg_list = self.assets.images.get("backgrounds", [])
        if not bg_list:
            return None
        idx = STAGE_BACKGROUNDS[self.current_stage % len(STAGE_BACKGROUNDS)]
        return bg_list[idx % len(bg_list)]

    def start_stage(self, stage_index=None):
        if stage_index is not None:
            self.current_stage = stage_index
        self.current_wave = 0
        self.stage_complete = False
        self.start_wave()

    def start_wave(self):
        stage_waves = ALL_STAGES[self.current_stage]
        if self.current_wave >= len(stage_waves):
            self.stage_complete = True
            return

        self.current_wave_data = stage_waves[self.current_wave]
        self.wave_active = True
        self.wave_enemies_spawned = False
        self.spawn_index = 0
        self.spawn_timer = 0
        self.spawn_delay = self.current_wave_data.get("delay", 0.3)

    def update(self, dt, enemy_group):
        if self.stage_complete or self.all_stages_complete:
            return

        if not self.wave_active:
            self.wave_delay_timer -= dt
            if self.wave_delay_timer <= 0:
                self.start_wave()
            return

        # Spawn enemies with staggered delay
        if not self.wave_enemies_spawned and self.current_wave_data:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                enemies_list = self.current_wave_data["enemies"]
                if self.spawn_index < len(enemies_list):
                    etype, x, movement = enemies_list[self.spawn_index]
                    y = -40 - self.spawn_index * 20
                    enemy = spawn_enemy(
                        self.assets, etype, x, y,
                        self.stage_number, self.groups_ref, movement
                    )
                    enemy_group.add(enemy)
                    self.spawn_index += 1
                    self.spawn_timer = self.spawn_delay
                else:
                    self.wave_enemies_spawned = True

        # Check if wave is clear (all enemies dead or off screen)
        if self.wave_enemies_spawned and len(enemy_group) == 0:
            self.wave_active = False
            self.current_wave += 1
            if self.current_wave >= len(ALL_STAGES[self.current_stage]):
                self.stage_complete = True
            else:
                self.wave_delay_timer = 2.0  # 2 second pause between waves

    def advance_stage(self):
        self.current_stage += 1
        if self.current_stage >= len(ALL_STAGES):
            self.all_stages_complete = True
            return False
        self.start_stage()
        return True
