import pygame
from sys import exit

from player import Player
from camera import Camera
from world import World
from ui import UI
from minimap import Minimap
from assets import ImageLoader
from sound_manager import SoundManager
from inventory import Inventory
from hoofdscherm import Menu
from zombie import ZombieSpawner
from scoreboard import Scoreboard
from pause_menu import PauseMenu
from death_screen import DeathScreen
from commit_score import CommitScoreScreen


def load_building(path, size, x, y):
    surf = ImageLoader.load(path, size=size)[0]
    return surf, pygame.Vector2(x, y)


def load_char_weapon(path):
    return ImageLoader.load(path, size=(96, 96))[0]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)

        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        self._clock = pygame.time.Clock()
        self.sound = SoundManager()
        self._menu = Menu(
            self._screen,
            ["Play", "Scoreboard", "Settings", "Credits", "Quit"]
        )

        self.state = "MENU"

        self._player = None
        self._world = None
        self._camera = None
        self._ui = None
        self._inventory = None
        self._zombie_spawner = None
        self._minimap = None

        w, h = self._screen.get_size()

        self.map_surf, _ = ImageLoader.load(
            "RAD ZONE/current version/Graphics/Final map game.png",
            size=(7680, 6400)
        )

        self.char_surf, self.char_rect = ImageLoader.load(
            "RAD ZONE/current version/Graphics/AChar.png",
            size=(150, 150),
            center=(3840, 3200)
        )

        self.health = ImageLoader.load(
            "RAD ZONE/current version/Graphics/Health-bar.png",
            size=(512, 35),
            center=(260, 30)
        )

        self.stamina = ImageLoader.load(
            "RAD ZONE/current version/Graphics/Stamina-bar.png",
            size=(512, 35),
            center=(260, 70)
        )

        self.outline = ImageLoader.load(
            "RAD ZONE/current version/Graphics/Border-bar.png",
            size=(512, 35)
        )

        self.buildings = [
            load_building("RAD ZONE/current version/Graphics/building 7 V2.png", (400, 768), 763, 515),
            load_building("RAD ZONE/current version/Graphics/building 7 V3.png", (400, 768), 1150, 515),
            load_building("RAD ZONE/current version/Graphics/Building7.png", (400, 768), 1527, 513),
            load_building("RAD ZONE/current version/Graphics/Building2 v3.png", (644, 704), 1920, 514),
            load_building("RAD ZONE/current version/Graphics/Building3.png", (408, 652), 2558, 573),
            load_building("RAD ZONE/current version/Graphics/Building6.png", (1432, 844), 3210, 438),
            load_building("RAD ZONE/current version/Graphics/van1.png", (256, 128), 3074, 1176),
            load_building("RAD ZONE/current version/Graphics/Building5.png", (972, 584), 5312, 620),
            load_building("RAD ZONE/current version/Graphics/Building1.png", (392, 648), 6520, 564),
            load_building("RAD ZONE/current version/Graphics/Building2.png", (644, 704), 1224, 1660),
            load_building("RAD ZONE/current version/Graphics/Building1.png", (392, 648), 2570, 1728),
            load_building("RAD ZONE/current version/Graphics/Building1.png", (392, 648), 2962, 1728),
            load_building("RAD ZONE/current version/Graphics/kerk.png", (716, 1292), 3451, 1452),
            load_building("RAD ZONE/current version/Graphics/building 7 V3.png", (400, 768), 4676, 1616),
            load_building("RAD ZONE/current version/Graphics/beenhouwer.png", (408, 652), 6062, 1674),
            load_building("RAD ZONE/current version/Graphics/pizzavan2.png", (256, 128), 5794, 2182),
            load_building("RAD ZONE/current version/Graphics/pizzavan2.png", (256, 128), 5794, 2065),
            load_building("RAD ZONE/current version/Graphics/Building2_v3_flip.png", (644, 704), 1844, 1660),
            load_building("RAD ZONE/current version/Graphics/Building2_v2_flip.png", (644, 704), 5064, 1616),
            load_building("RAD ZONE/current version/Graphics/dead tree.png", (400, 400), 4084, 1790),
            load_building("RAD ZONE/current version/Graphics/autumn tree.png", (400, 400), 4246, 1830),
            load_building("RAD ZONE/current version/Graphics/Fontein.png", (600, 600), 3514, 2756),
            load_building("RAD ZONE/current version/Graphics/Building7_flip.png", (400, 768), 4740, 2694),
            load_building("RAD ZONE/current version/Graphics/Building7.png", (400, 768), 5136, 2692)
        ]

        self._inventory_key_down = False

    # ---------------- INVENTORY CREATION ----------------
    def _create_inventory(self, screen_size):
        def load_icon(path):
            return ImageLoader.load(path, size=(48, 48))[0]

        def load_weapon(path):
            return ImageLoader.load(path, size=(96, 96))[0]

        item_data = {
            "pistol": {
                "icon": load_icon("RAD ZONE/current version/Graphics/pistool.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/pistool.png"),
                "char_weapon": load_char_weapon("RAD ZONE/current version/Graphics/char_pistool.png"),
                "owned": True
            },
            "knife": {
                "icon": load_icon("RAD ZONE/current version/Graphics/knife.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/knife.png"),
                "owned": True
            },
            "revolver": {
                "icon": load_icon("RAD ZONE/current version/Graphics/revolver.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/revolver.png"),
                "char_weapon": load_char_weapon("RAD ZONE/current version/Graphics/char_revolver.png"),
                "owned": True
            },
            "shotgun": {
                "icon": load_icon("RAD ZONE/current version/Graphics/shotgun.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/shotgun.png"),
                "char_weapon": load_char_weapon("RAD ZONE/current version/Graphics/char_shotgun.png"),
                "owned": True
            },
            "crossbow": {
                "icon": load_icon("RAD ZONE/current version/Graphics/crossbow.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/crossbow.png"),
                "char_weapon": load_char_weapon("RAD ZONE/current version/Graphics/char_crossbow.png"),
                "owned": True
            },
            "machine_gun": {
                "icon": load_icon("RAD ZONE/current version/Graphics/machine_gun.png"),
                "weapon_surf": load_weapon("RAD ZONE/current version/Graphics/machine_gun.png"),
                "char_weapon": load_char_weapon("RAD ZONE/current version/Graphics/char_machine_gun.png"),
                "owned": True
            }
        }

        socket_surf = ImageLoader.load("RAD ZONE/current version/Graphics/Inventory_box.png", size=(64, 64))[0]
        inventory_bg = ImageLoader.load("RAD ZONE/current version/Graphics/Inventory_background.png")[0]
        hotbar_bg = ImageLoader.load("RAD ZONE/current version/Graphics/Hotbar_background.png")[0]

        return Inventory(socket_surf, item_data, screen_size, inventory_bg, hotbar_bg, self._player)

    # ---------------- START GAME ----------------
    def start_game(self):
        w, h = self._screen.get_size()
        start_pos = self.char_rect.center
        self._player = Player(self.char_surf, self.sound, pos=start_pos)

        self._zombie_spawner = ZombieSpawner(self.sound)
        self._player._zombie_spawner = self._zombie_spawner

        self._camera = Camera(w, h)
        self._world = World(self.map_surf, self.buildings)
        self._ui = UI(self.health, self.stamina, self.outline)
        self._minimap = Minimap(self.map_surf, self.buildings, (w, h))

        self._inventory = self._create_inventory((w, h))
        self._inventory_key_down = False

    # ---------------- GAME LOOP ----------------
    def run(self):
        while True:
            if self.state == "MENU":
                choice = self._menu.run()

                if choice == "Quit":
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

                elif choice == "Scoreboard":
                    Scoreboard(self._screen).run()
                    continue

                elif choice == "Play":
                    pygame.mixer.music.stop()
                    Menu.current_music_file = None
                    self.start_game()
                    self.state = "PLAYING"

                elif choice == "Credits":
                    from credits import CreditsScreen
                    CreditsScreen(self._screen).run()
                    continue

                elif choice == "Settings":
                    from settings import SettingsMenu
                    SettingsMenu(self._screen, self.sound).run()
                    continue

            elif self.state == "PLAYING":
                self._game_loop()

            elif self.state == "DEAD":
                self._death_loop()


    # ---------------- GAMEPLAY LOOP ----------------
    def _game_loop(self):
        paused = False
        while self.state == "PLAYING":
            dt = self._clock.tick(120) / 1000
            current_time = pygame.time.get_ticks() / 1000
            keys = pygame.key.get_pressed()
            player_pos = pygame.Vector2(self._player.get_rect().center)
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_down = mouse_pressed[0]
            mouse_up = not mouse_pressed[0]

            # ---------------- EVENT HANDLING ----------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self._inventory and event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self._inventory.select_next()
                    else:
                        self._inventory.select_previous()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and self._inventory and not self._inventory_key_down:
                        self._inventory.toggle()
                        self._inventory_key_down = True

                    if event.key == pygame.K_ESCAPE:
                        paused = True  # Enter pause loop

                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    self._inventory_key_down = False

            # ---------------- PAUSE LOOP ----------------
            if paused:
                # Capture a snapshot of the current game screen
                game_surface = self._screen.copy()
                pause_menu = PauseMenu(self._screen, self.sound)
                
                # Run pause menu in a blocking loop
                while paused:
                    dt_pause = self._clock.tick(120) / 1000

                    # Draw the pause menu overlay
                    pause_menu.draw(game_surface)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                paused = False  # Resume gameplay

                        # Handle pause menu buttons
                        action = pause_menu.handle_event(event)
                        if action == "Resume":
                            paused = False
                        elif action == "Quit":
                            paused = False
                            self.state = "MENU"  # Return to main menu
                            return  # Exit _game_loop
                        elif action == "Audio Settings":
                            paused = False  # Temporarily exit pause loop
                            from audio_menu import Audio_Menu
                            Audio_Menu(self._screen, self.sound).run()
                            paused = True   # Return to pause loop
                            pause_menu = PauseMenu(self._screen, self.sound)  # Redraw buttons
                        elif action == "Controls":
                            paused = False
                            from controls_menu import ControlsMenu
                            ControlsMenu(self._screen, self.sound).run()
                            paused = True
                            pause_menu = PauseMenu(self._screen, self.sound)  # Redraw buttons


            # ---------------- GAMEPLAY UPDATES ----------------
            self._camera.update(player_pos)
            mouse_world = pygame.Vector2(pygame.mouse.get_pos()) + self._camera.get_position()
            self._player.update(keys, dt, current_time, mouse_world)
            self._zombie_spawner.update(player_pos, dt, current_time)
            self._handle_attack(current_time, player_pos)
            self._handle_zombie_attacks(player_pos, dt)

            # ---------------- DRAW ----------------
            self._screen.fill((0, 0, 0))
            if self._world:
                self._world.draw(self._screen, self._camera)

            # Draw player & zombies
            drawables = [("player", self._player, player_pos.y)]
            for z in self._zombie_spawner.get_zombies():
                drawables.append(("zombie", z, z.get_position().y))
            for _, obj, _ in sorted(drawables, key=lambda x: x[2]):
                obj.draw(self._screen, self._camera)

            if self._ui:
                self._ui.draw(
                    self._screen,
                    self._player.get_health(),
                    self._player.get_max_health(),
                    self._player.get_stamina(),
                    100,
                    self._zombie_spawner.current_wave
                )

            if self._minimap:
                self._minimap.draw(self._screen, player_pos)

            if self._inventory:
                self._inventory.draw(self._screen)
                self._inventory.update(pygame.mouse.get_pos(), mouse_down, mouse_up)

            # ---------------- CHECK PLAYER DEATH ----------------
            if self._player.get_health() <= 0:
                pygame.time.delay(100)
                self.state = "DEAD"
                return

            pygame.display.flip()


    # ---------------- KNIFE LOGIC ----------------
    def _handle_attack(self, current_time, player_pos):
        player = self._player
        if player._equipped_item and player._equipped_item.get_id() == "knife":
            if current_time - player._attack_last_time > 0.5:
                player.animator.play_stab()
                for zombie in self._zombie_spawner.get_zombies():
                    if zombie not in player._attack_targets_hit and not zombie._is_dead:
                        if (zombie.get_position() - player_pos).length() < 100:
                            zombie.take_damage(50, zombie.get_position() - player_pos, current_time)
                            player._attack_targets_hit.add(zombie)
                player._attack_last_time = current_time

    # ---------------- ZOMBIE DAMAGE ----------------
    def _handle_zombie_attacks(self, player_pos, dt):
        for zombie in self._zombie_spawner.get_zombies():
            if zombie.is_attacking() and (zombie.get_position() - player_pos).length() < 80:
                self._player.take_damage(zombie._damage_per_second * dt)

    # ---------------- DEATH SCREEN ----------------
    def _death_loop(self):
        kills = self._zombie_spawner.get_kill_count()
        game_surface = self._screen.copy()
        while True:
            from commit_score import CommitScoreScreen
            action = DeathScreen(self._screen, kills).run(game_surface)
            if action == "Play":
                self._reset_game()
                self.start_game()
                self.state = "PLAYING"
                return
            elif action == "CommitScore":
                name = CommitScoreScreen(self._screen, kills).run()
                print(f"Score opgeslagen voor: {name}")
                self._reset_game()
                self.state = "MENU"
                return
            elif action == "Quit":
                self._reset_game()
                self.state = "MENU"
                return

    # ---------------- RESET GAME ----------------
    def _reset_game(self):
        self._player = None
        self._world = None
        self._camera = None
        self._ui = None
        self._inventory = None
        self._zombie_spawner = None
        self._minimap = None
