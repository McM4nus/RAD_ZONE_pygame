import pygame
from ui import BoxButton

class ControlsMenu:
    def __init__(self, screen, sound_manager, background_surf=None):
        self.screen = screen
        self.sound_manager = sound_manager
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Background setup
        if background_surf:
            self.background = background_surf.copy()
        else:
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((0, 0, 0))

        # Title font
        self.title_font = pygame.font.Font("RAD ZONE/current version/Fonts/Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf", 72)
        self.title_surf = self.title_font.render("CONTROLS", True, (141, 251, 45))
        self.title_rect = self.title_surf.get_rect(center=(self.width // 2, 100))

        # Text font
        self.text_font = pygame.font.Font("RAD ZONE/current version/Fonts/BitcountGridSingle_Roman-SemiBold.ttf", 48)

        # Buttons
        font = pygame.font.Font("RAD ZONE/current version/Fonts/Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf", 24)
        self.back_btn = BoxButton(
            "BACK", 
            (self.width // 2, self.height - 100), 
            size=(150, 60), 
            font=font
        )

        # Controls list (action, key)
        self.controls = [
            ("Move up", "Z"),
            ("Move down", "S"),
            ("Move left", "Q"),
            ("Move right", "D"),
            ("Aim", "Mouse"),
            ("Shoot", "Left Mouseclick"),
            ("Cycle Weapons", "Mouse Scroll up/down"),
            ("Open/Close Inventory", "E"),
        ]

        # Layout
        self.start_y = 250
        self.line_spacing = 60
        self.action_x = 300            # Left-aligned actions
        self.key_x = self.width // 2 + 200  # Right-aligned keys

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_surf, self.title_rect)

        y = self.start_y
        for action, key in self.controls:
            # Render action
            action_surf = self.text_font.render(action, True, (141, 251, 45))
            action_rect = action_surf.get_rect(topleft=(self.action_x, y))
            self.screen.blit(action_surf, action_rect)

            # Render key/button
            key_surf = self.text_font.render(key if isinstance(key, str) else ", ".join(key), True, (200, 200, 200))
            key_rect = key_surf.get_rect(topleft=(self.key_x, y))
            self.screen.blit(key_surf, key_rect)

            y += self.line_spacing

        # Draw back button
        self.back_btn.draw(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.back_btn.handle_event(event):
                    running = False
