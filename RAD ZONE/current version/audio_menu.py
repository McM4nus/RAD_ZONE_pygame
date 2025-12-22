import pygame
from ui import BoxButton


class Slider:
    """Horizontal slider with rectangular handle."""
    def __init__(self, pos, width, min_val=0, max_val=100, initial=50):
        self.pos = pygame.Vector2(pos)
        self.width = width
        self.track_height = 12
        self.handle_width = 20
        self.handle_height = 40
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.dragging = False

        self.rect = pygame.Rect(
            self.pos.x - width // 2,
            self.pos.y - self.track_height // 2,
            width,
            self.track_height
        )

        self.track_color = (50, 50, 50)
        self.filled_color = (137, 251, 45)
        self.handle_color = (54, 164, 34)

    def handle_event(self, event):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        filled_width = (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        handle_x = self.rect.left + filled_width

        handle_rect = pygame.Rect(
            handle_x - self.handle_width // 2,
            self.pos.y - self.handle_height // 2,
            self.handle_width,
            self.handle_height
        )

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if handle_rect.collidepoint(mouse_pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        if self.dragging:
            rel_x = mouse_pos.x - self.rect.left
            rel_x = max(0, min(self.width, rel_x))
            self.value = int(self.min_val + (rel_x / self.width) * (self.max_val - self.min_val))

    def draw(self, surface):
        pygame.draw.rect(surface, self.track_color, self.rect, border_radius=6)

        filled_width = (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.track_height)
        pygame.draw.rect(surface, self.filled_color, filled_rect, border_radius=6)

        handle_rect = pygame.Rect(
            self.rect.left + filled_width - self.handle_width // 2,
            self.pos.y - self.handle_height // 2,
            self.handle_width,
            self.handle_height
        )
        pygame.draw.rect(surface, self.handle_color, handle_rect)
        pygame.draw.rect(surface, (100, 100, 100), handle_rect, 2)


# =====================================================================


class Audio_Menu:
    def __init__(self, screen, sound_manager, background_surf=None):
        self.screen = screen
        self.sound_manager = sound_manager
        self.width, self.height = screen.get_size()

        self.background = background_surf.copy() if background_surf else pygame.Surface((self.width, self.height))
        self.background.fill((30, 30, 30))

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.background.blit(overlay, (0, 0))

        start_y = 280
        spacing = int(self.height * 0.085)
        center_x = self.width // 2

        self.sliders = {
            "Master": Slider((center_x, start_y), 300, 0, 100, int(self.sound_manager.master_volume * 100)),
            "Music": Slider((center_x, start_y + spacing), 300, 0, 100, int(self.sound_manager.music_volume * 100)),
            "SFX": Slider((center_x, start_y + spacing * 2), 300, 0, 100, int(self.sound_manager.sfx_volume * 100)),
            "Weapons": Slider((center_x, start_y + spacing * 3), 300, 0, 100, int(self.sound_manager.weapon_volume * 100)),
            "Zombies": Slider((center_x, start_y + spacing * 4), 300, 0, 100, int(self.sound_manager.zombie_volume * 100)),
            "Player": Slider((center_x, start_y + spacing * 5), 300, 0, 100, int(self.sound_manager.player_volume * 100)),
        }

        font = pygame.font.Font("RAD ZONE/current version/Fonts/Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf", 24)
        self.back_button = BoxButton("BACK", (center_x, start_y + spacing * 6.5), size=(150, 60), font=font)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        font = pygame.font.Font("RAD ZONE/current version/Fonts/BitcountGridSingle_Roman-SemiBold.ttf", 24)
        for name, slider in self.sliders.items():
            slider.draw(self.screen)
            label = font.render(f"{name}: {slider.value}", True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=(slider.pos.x, slider.pos.y - 30)))

        self.back_button.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                for name, slider in self.sliders.items():
                    slider.handle_event(event)
                    v = slider.value / 100.0

                    if name == "Master":
                        self.sound_manager.set_master_volume(v)
                    elif name == "Music":
                        self.sound_manager.set_music_volume(v)
                    elif name == "SFX":
                        self.sound_manager.set_sfx_volume(v)
                    elif name == "Weapons":
                        self.sound_manager.set_weapon_volume(v)
                    elif name == "Zombies":
                        self.sound_manager.set_zombie_volume(v)
                    elif name == "Player":
                        self.sound_manager.set_player_volume(v)

                if self.back_button.handle_event(event):
                    return
