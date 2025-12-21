import pygame
import random


class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

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

        self._player_hurt_index = 0
        self._player_hurt_channel = pygame.mixer.Channel(31)

        # ---------------------- CHANNELS ----------------------
        pygame.mixer.set_num_channels(64)
        self._channels = {
            "weapon": pygame.mixer.Channel(30),
            "item": pygame.mixer.Channel(32),
            "zombie": pygame.mixer.Channel(33),
            "player_death": pygame.mixer.Channel(34),
        }

        self._current_equip_sound = None

        # Apply initial volumes ONCE
        self._apply_volumes()

    # ====================== VOLUME APPLICATION ======================
    def _apply_volumes(self):
        # Weapons
        for weapon_actions in self.weapon.values():
            for sound in weapon_actions.values():
                if sound:
                    sound.set_volume(
                        self._BASE_WEAPON
                        * self.weapon_volume
                        * self.sfx_volume
                        * self.master_volume
                    )

        # Items
        for sound in self.items.values():
            sound.set_volume(
                self._BASE_ITEM
                * self.sfx_volume
                * self.master_volume
            )

        # Zombies
        for sound in self.zombie_death:
            sound.set_volume(
                self._BASE_ZOMBIE
                * self.zombie_volume
                * self.sfx_volume
                * self.master_volume
            )

        # Player
        for sound in self.player_hurt:
            sound.set_volume(
                self._BASE_PLAYER
                * self.player_volume
                * self.sfx_volume
                * self.master_volume
            )

        self.player_death.set_volume(
            self._BASE_PLAYER
            * self.player_volume
            * self.sfx_volume
            * self.master_volume
        )

        pygame.mixer.music.set_volume(
            self.music_volume * self.master_volume
        )

    # ====================== SETTERS ======================
    def set_master_volume(self, value):
        self.master_volume = value
        self._apply_volumes()

    def set_music_volume(self, value):
        self.music_volume = value
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def set_sfx_volume(self, value):
        self.sfx_volume = value
        self._apply_volumes()

    def set_weapon_volume(self, value):
        self.weapon_volume = value
        self._apply_volumes()

    def set_zombie_volume(self, value):
        self.zombie_volume = value
        self._apply_volumes()

    def set_player_volume(self, value):
        self.player_volume = value
        self._apply_volumes()

    # ====================== PLAYBACK ======================
    def play_weapon(self, weapon, action):
        sound = self.weapon.get(weapon, {}).get(action)
        if not sound:
            return

        if action == "equip":
            if self._current_equip_sound and self._channels["weapon"].get_busy():
                self._channels["weapon"].stop()
            self._current_equip_sound = sound

        self._channels["weapon"].play(sound)

    def play_item(self, item_name):
        sound = self.items.get(item_name)
        if sound:
            self._channels["item"].play(sound)

    def play_zombie_death(self):
        self._channels["zombie"].play(random.choice(self.zombie_death))

    def play_player_hurt(self):
        if not self._player_hurt_channel.get_busy():
            sound = self.player_hurt[self._player_hurt_index]
            self._player_hurt_channel.play(sound)
            self._player_hurt_index = (self._player_hurt_index + 1) % len(self.player_hurt)

    def play_player_death(self):
        self._channels["player_death"].play(self.player_death)
