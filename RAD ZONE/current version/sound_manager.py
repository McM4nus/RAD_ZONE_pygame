import pygame
import random
from pathlib import Path

class SoundManager:
    def __init__(self):
        # ---------------------- GLOBAL VOLUMES ----------------------
        self.master_volume = 0.4
        self.music_volume = 0.5
        self.sfx_volume = 0.5  # SFX master volume

        self.weapon_volume = 0.3
        self.zombie_volume = 0.45
        self.player_volume = 0.6

        # ---------------------- BASE MIX LEVELS ----------------------
        self._BASE_WEAPON = 0.5
        self._BASE_ITEM = 0.5
        self._BASE_ZOMBIE = 0.5
        self._BASE_PLAYER = 0.5

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

        # ---------------------- AUDIO INITIALIZATION ----------------------
        self._player_hurt_index = 0
        self._player_hurt_channel = pygame.mixer.Channel(31)

        # ---------------------- CHANNELS ----------------------
        self._weapon_channels = [pygame.mixer.Channel(i) for i in range(8, 24)]
        self._zombie_channels = [pygame.mixer.Channel(i) for i in range(24, 28)]  # new
        self._channels = {
            "item": pygame.mixer.Channel(32),
            "player_death": pygame.mixer.Channel(33),
        }

        self._current_equip_sound = None
        self._current_music_file = None  # track currently playing music

    # ====================== MUSIC CONTROL ======================
    def play_music(self, path, loop=True, start=0.0, volume=None):
        path = str(path)
        if self._current_music_file == path and pygame.mixer.music.get_busy():
            return
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

    # ====================== VOLUME CONTROLS ======================
    def set_master_volume(self, value: float):
        self.master_volume = max(0.0, min(1.0, value))
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def set_music_volume(self, value: float):
        self.music_volume = max(0.0, min(1.0, value))
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def set_sfx_volume(self, value: float):
        self.sfx_volume = max(0.0, min(1.0, value))

    def set_weapon_volume(self, value: float):
        self.weapon_volume = max(0.0, min(1.0, value))

    def set_zombie_volume(self, value: float):
        self.zombie_volume = max(0.0, min(1.0, value))

    def set_player_volume(self, value: float):
        self.player_volume = max(0.0, min(1.0, value))

    # ====================== PLAYER SOUNDS ======================
    def play_player_hurt(self):
        sound = self.player_hurt[self._player_hurt_index]
        self._player_hurt_index = (self._player_hurt_index + 1) % len(self.player_hurt)
        self._player_hurt_channel.set_volume(
            self.master_volume * self.sfx_volume * self.player_volume
        )
        self._player_hurt_channel.play(sound)

    def play_player_death(self):
        ch = self._channels["player_death"]
        ch.set_volume(self.master_volume * self.sfx_volume * self.player_volume)
        ch.play(self.player_death)

    # ====================== WEAPON SOUNDS ======================
    def play_weapon(self, weapon_name, action):
        if weapon_name not in self.weapon: return
        sound = self.weapon[weapon_name].get(action)
        if not sound: return
        for ch in self._weapon_channels:
            if not ch.get_busy():
                ch.set_volume(self.master_volume * self.sfx_volume * self.weapon_volume)
                ch.play(sound)
                return

    # ====================== ITEM SOUNDS ======================
    def play_item(self, item_name):
        if item_name not in self.items: return
        ch = self._channels["item"]
        ch.set_volume(self.master_volume * self.sfx_volume * self._BASE_ITEM)
        ch.play(self.items[item_name])

    # ====================== ZOMBIE SOUNDS ======================
    def play_zombie_death(self):
        sound = random.choice(self.zombie_death)
        for ch in self._zombie_channels:
            if not ch.get_busy():
                ch.set_volume(self.master_volume * self.sfx_volume * self.zombie_volume * self._BASE_ZOMBIE)
                vol = self.master_volume * self.sfx_volume * self.zombie_volume * self._BASE_ZOMBIE
                # print(f"Zombie volume = {vol}")
                ch.play(sound)
                return
