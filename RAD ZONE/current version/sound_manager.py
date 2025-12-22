import pygame
import random
from pathlib import Path

class SoundManager:
    def __init__(self):
        # ---------------------- GLOBAL VOLUMES ----------------------
        self.master_volume = 0.75
        self.music_volume = 0.6
        self.sfx_volume = 0.6

        self.weapon_volume = 0.3
        self.zombie_volume = 0.4
        self.player_volume = 0.5

        # ---------------------- BASE MIX LEVELS ----------------------
        self._BASE_WEAPON = 1
        self._BASE_ITEM = 1
        self._BASE_ZOMBIE = 1
        self._BASE_PLAYER = 1

        # ---------------------- WEAPON SOUNDS ----------------------
        self.weapon = {
            "pistol": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_pistol.wav"),
                "reload": pygame.mixer.Sound("RAD ZONE/current version/Audio/reload_pistol.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/equip_pistol.wav"),
            },
            "rifle": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_rifle_single_shot.wav"),
                "reload": pygame.mixer.Sound("RAD ZONE/current version/Audio/reload_rifle.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/equip_rifle.wav"),
            },
            "revolver": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_revolver.wav"),
                "reload": pygame.mixer.Sound("RAD ZONE/current version/Audio/revolver_reload.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/equip_revolver.wav"),
            },
            "shotgun": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_shotgun.wav"),
                "reload": pygame.mixer.Sound("RAD ZONE/current version/Audio/shotgun_reload.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/equip_shotgun.wav"),
            },
            "knife": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/knife_slash.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/knife_slash.wav"),
                "reload": None
            },
            "crossbow": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_crossbow.wav"),
                "equip": None,
                "reload": None,
            },
            "machine_gun": {
                "shoot": pygame.mixer.Sound("RAD ZONE/current version/Audio/shoot_rifle_single_shot.wav"),
                "reload": pygame.mixer.Sound("RAD ZONE/current version/Audio/reload_rifle.wav"),
                "equip": pygame.mixer.Sound("RAD ZONE/current version/Audio/equip_rifle.wav"),
            }
        }

        # ---------------------- ITEM SOUNDS ----------------------
        self.items = {
            "pickup_bandage": pygame.mixer.Sound("RAD ZONE/current version/Audio/pickup_bandages.wav"),
            "pickup_iodine_pills": pygame.mixer.Sound("RAD ZONE/current version/Audio/pickup_iodine_pills.wav"),
            "use_bandage": pygame.mixer.Sound("RAD ZONE/current version/Audio/use_bandages.wav"),
            "use_iodine": pygame.mixer.Sound("RAD ZONE/current version/Audio/use_iodine_pills.wav"),
        }

        # ---------------------- ZOMBIE SOUNDS ----------------------
        self.zombie_death = [
            pygame.mixer.Sound(f"RAD ZONE/current version/Audio/zomdie_die_{i}.wav")
            for i in range(1, 17)
        ]

        # ---------------------- PLAYER SOUNDS ----------------------
        self.player_hurt = [
            pygame.mixer.Sound(f"RAD ZONE/current version/Audio/player_take_damage_{i}.wav")
            for i in range(1, 11)
        ]
        self.player_death = pygame.mixer.Sound(
            "RAD ZONE/current version/Audio/scream_wilhelm.wav"
        )

        #----------------------AUDIO INITIALIZATION----------------------
        self._player_hurt_index = 0
        self._player_hurt_channel = pygame.mixer.Channel(31)

        # ---------------------- CHANNELS ----------------------
        self._weapon_channels = [pygame.mixer.Channel(i) for i in range(8, 24)]
        self._channels = {
            "item": pygame.mixer.Channel(32),
            "zombie": pygame.mixer.Channel(33),
            "player_death": pygame.mixer.Channel(34),
        }

        self._current_equip_sound = None
        self._current_music_file = None  # NEW: track currently playing music

    # ====================== MUSIC CONTROL ======================
    def play_music(self, path, loop=True, start=0.0, volume=None):
        path = str(path)
        if self._current_music_file == path and pygame.mixer.music.get_busy():
            return  # already playing, do nothing

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0, start=start)
        if volume is not None:
            pygame.mixer.music.set_volume(volume * self.master_volume)
        else:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        self._current_music_file = path

    def stop_music(self):
        pygame.mixer.music.stop()
        self._current_music_file = None

    # ====================== OTHER METHODS ======================
    # (play_weapon, play_item, play_zombie_death, play_player_hurt, etc.)
    # ... (keep your previous methods exactly the same)
