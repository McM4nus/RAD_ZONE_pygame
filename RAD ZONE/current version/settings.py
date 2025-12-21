import pygame
from ui import BoxButton
from audio_menu import Audio_Menu


class SettingsMenu:
    def __init__(self, screen, sound_manager, background_surf=None):
        self.screen = screen
        self.sound_manager = sound_manager
        self.width, self.height = screen.get_size()

        # Use passed background, otherwise default to main menu background
        if background_surf:
            self.background = background_surf.copy()
            # Overlay dark semi-transparent layer for pause menu effect
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.background.blit(overlay, (0, 0))
            self.bg_rect = self.background.get_rect(topleft=(0, 0))
        else:
            # Load main menu background image
            self.background = pygame.image.load(
                "RAD ZONE/UI/Menu/achtergrond menu.png"
            ).convert_alpha()
            # Scale and round corners as in main menu
            orig_width, orig_height = self.background.get_size()
            self.background = pygame.transform.scale(self.background, (orig_width // 2, orig_height // 2))
            self.background = self.round_corners(self.background, 30)
            # Center the background
            self.bg_rect = self.background.get_rect(center=(self.width // 2, self.height // 2))

        # Buttons
        start_y = 500
        spacing = int(self.height * 0.12)
        center_x = self.width // 2
        font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 48)

        self.buttons = {
            "Audio": BoxButton("AUDIO", (center_x, start_y), size=(140, 60), font=font),
            "Controls": BoxButton("CONTROLS", (center_x, start_y + spacing), size=(210, 60), font=font),
            "Back": BoxButton("BACK", (center_x, start_y + spacing*2), size=(130, 60), font=font),
        }

    def round_corners(self, image, radius):
        """Return a copy of the image with rounded corners"""
        size = image.get_size()
        rounded_surf = pygame.Surface(size, pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, *size)
        pygame.draw.rect(rounded_surf, (255, 255, 255, 255), rect, border_radius=radius)
        rounded_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return rounded_surf

    def draw(self):
        # Use bg_rect to correctly position the background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.bg_rect)
        for btn in self.buttons.values():
            btn.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                for name, btn in self.buttons.items():
                    if btn.handle_event(event):
                        if name == "Audio":
                            audio_menu_screen = Audio_Menu(self.screen, self.sound_manager)
                            audio_menu_screen.run()
                            return self.run()

                            # After Audio_Menu closes, continue showing settings menu
                            return self.run()  # restart the settings menu loop
                        else:
                            # For "Controls" or "Back", return button name as usual
                            return name
