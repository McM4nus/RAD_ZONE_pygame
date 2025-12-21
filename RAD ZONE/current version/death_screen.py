import pygame
from sys import exit
from ui import BoxButton  # Use BoxButton instead of ImageButton

class DeathScreen:
    def __init__(self, screen, zombies_killed):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.kills = zombies_killed
        self.width, self.height = screen.get_size()

        # ----------------------------
        # Overlay background
        # ----------------------------
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(150)  # semi-transparent
        self.overlay.fill((0, 0, 0))

        # ----------------------------
        # Buttons
        # ----------------------------
        center_x = self.width // 2
        start_y = 450
        spacing = int(self.height * 0.055)
        font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 48)

        self.buttons = {
            "Play": BoxButton(
                "PLAY",
                (center_x, start_y + spacing * 0),
                size=(160, 55),
                font=font,
                idle_color=(12, 32, 17, 220),          # more opaque idle
                hover_color=(52, 168, 34, 230),        # hover color
                pressed_color=(120, 120, 120, 255),    # pressed color
                text_color=(255, 255, 255),            # text color
                border_color=(74, 111, 5, 255),        # border color
                border_width=3,
                shadow_color=(0, 0, 0),                # shadow color
                shadow_offset=(2, 2)                   # shadow offset
            ),
            "CommitScore": BoxButton(
                "COMMIT SCORE",
                (center_x, start_y + spacing * 1),
                size=(350, 55),
                font=font,
                idle_color=(12, 32, 17, 220),
                hover_color=(52, 168, 34, 230),
                pressed_color=(120, 120, 120, 255),
                text_color=(255, 255, 255),
                border_color=(74, 111, 5, 255),
                border_width=3,
                shadow_color=(0, 0, 0),
                shadow_offset=(2, 2)
            ),
            "Quit": BoxButton(
                "MAIN MENU",
                (center_x, start_y + spacing * 2),
                size=(300, 55),
                font=font,
                idle_color=(12, 32, 17, 220),
                hover_color=(52, 168, 34, 230),
                pressed_color=(120, 120, 120, 255),
                text_color=(255, 255, 255),
                border_color=(74, 111, 5, 255),
                border_width=3,
                shadow_color=(0, 0, 0),
                shadow_offset=(2, 2)
            ),
        }


        # Fonts for title and score
        self.font_big = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 80)
        self.font_small = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 40)

    def draw(self, game_surface):
        # Draw background overlay
        self.screen.blit(game_surface, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        # Title and score
        title = self.font_big.render("YOU DIED", True, (200, 0, 0))
        score = self.font_small.render(f"Zombies killed: {self.kills}", True, (255, 255, 255))

        self.screen.blit(title, title.get_rect(center=(self.width // 2, 150)))
        self.screen.blit(score, score.get_rect(center=(self.width // 2, 250)))

        # Draw buttons
        for btn in self.buttons.values():
            btn.draw(self.screen)

        pygame.display.flip()

    def run(self, game_surface):
        while True:
            self.clock.tick(60)
            self.draw(game_surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Check button clicks
                for name, btn in self.buttons.items():
                    if btn.handle_event(event):
                        return name

                # Optional: Escape returns to Quit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "Quit"
