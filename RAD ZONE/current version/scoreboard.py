import pygame
import sys
import json
import os
from ui import BoxButton

# -----------------------------
#       HELPER FUNCTION
# -----------------------------
def round_corners(image, radius):
    """Return a copy of the image with rounded corners of given radius."""
    size = image.get_size()
    rounded_surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, *size)
    pygame.draw.rect(rounded_surf, (255, 255, 255, 255), rect, border_radius=radius)
    rounded_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded_surf

# -----------------------------
#        SCOREBOARD CLASS
# -----------------------------
class Scoreboard:
    def __init__(self, screen, score_file=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.score_file = score_file or os.path.join(
            "RAD ZONE", "current version", "scores.json"
        )


        # -----------------------------
        # Background
        # -----------------------------
        bg_path = os.path.join(
            "RAD ZONE", "UI", "Menu", "achtergrond_scoreboard.png"
        )
        self.background = pygame.image.load(bg_path).convert_alpha()
        orig_width, orig_height = self.background.get_size()
        self.background = pygame.transform.scale(
            self.background, (orig_width // 2, orig_height // 2)
        )
        self.background = round_corners(self.background, radius=30)
        self.bg_rect = self.background.get_rect(
            center=(self.width // 2, self.height // 2)
        )

        # -----------------------------
        # Font
        # -----------------------------
        font_path = os.path.join(
            "RAD ZONE", "current version", "Fonts", "Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf"
        )
        self.font = pygame.font.Font(font_path, 24)

        # -----------------------------
        # Score box styling
        # -----------------------------
        self.box_padding = 20
        self.box_bg_color = (10, 25, 10, 180)   # RGBA (opacity!)
        self.box_border_color = (141, 251, 45, 200)
        self.box_border_width = 3
        self.box_radius = 18

        # -----------------------------
        # Score text layout
        # -----------------------------
        self.score_start_y = 400
        self.score_spacing = 35

        # Shadow settings (easy tweak)
        self.shadow_offset = (2, 2)       # (x, y)
        self.shadow_color = (255, 255, 255)     # black shadow
        self.score_color = (141, 251, 45) # main text color
        

        # -----------------------------
        # Return button
        # -----------------------------
        self.return_btn = BoxButton(
            "RETURN",
            (self.width // 2, self.height - 100),
            font=self.font
        )


    # -----------------------------
    #   LOAD SCORES FROM FILE
    # -----------------------------
    def load_scores(self):
        """Always reload the scores from the file."""
        if not os.path.exists(self.score_file):
            self.scores = []
            return
        try:
            with open(self.score_file, "r") as f:
                self.scores = json.load(f)
        except json.JSONDecodeError:
            self.scores = []

        # Sort descending and keep top 10
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]

    # -----------------------------
    #   DRAW SCREEN
    # -----------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.bg_rect)

        start_y = 400
        spacing = 35
        column_padding_x = 0

        column_width = 350
        column_left_x = (self.width - column_width) // 2 + column_padding_x

        # -----------------------------
        # SCORE BOX CONFIG
        # -----------------------------
        box_padding = 20
        box_bg_color = (10, 25, 10, 120)      # RGBA
        box_border_color = (141, 251, 45, 20)
        box_border_width = 3
        box_radius = 18

        # -----------------------------
        # CALCULATE BOX SIZE
        # -----------------------------
        line_count = len(self.scores)
        if line_count > 0:
            box_x = column_left_x - box_padding
            box_y = start_y - box_padding
            box_width = column_width + box_padding * 2
            box_height = line_count * spacing + box_padding * 2

            # Create transparent surface for box
            box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

            # Background
            pygame.draw.rect(
                box_surf,
                box_bg_color,
                box_surf.get_rect(),
                border_radius=box_radius
            )

            # Border
            if box_border_width > 0:
                pygame.draw.rect(
                    box_surf,
                    box_border_color,
                    box_surf.get_rect(),
                    box_border_width,
                    border_radius=box_radius
                )

            self.screen.blit(box_surf, (box_x, box_y))

        # -----------------------------
        # DRAW SCORES
        # -----------------------------
        for i, entry in enumerate(self.scores):
            name = entry.get("name", "???")
            score = entry.get("score", 0)
            text = f"{i+1}. {name} - {score}"

            y = start_y + i * spacing

            # Shadow
            shadow_surf = self.font.render(text, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(
                topleft=(
                    column_left_x + self.shadow_offset[0],
                    y + self.shadow_offset[1]
                )
            )
            self.screen.blit(shadow_surf, shadow_rect)

            # Main text
            label = self.font.render(text, True, self.score_color)
            rect = label.get_rect(topleft=(column_left_x, y))
            self.screen.blit(label, rect)

        self.return_btn.draw(self.screen)
        pygame.display.flip()




    # -----------------------------
    #   RUN LOOP
    # -----------------------------
    def run(self):
        """Reload scores at the start to always show latest data."""
        self.load_scores()  # <-- key change: reload every time
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.return_btn.handle_event(event):
                    return
            clock.tick(60)
