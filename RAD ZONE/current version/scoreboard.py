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
    def __init__(self, screen, score_file="scores.json"):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.score_file = score_file

        # Load scores
        self.load_scores()

        # Load and scale background
        self.background = pygame.image.load(
            "RAD ZONE/UI/Menu/achtergrond_scoreboard.png"
        ).convert_alpha()  # preserve transparency
        orig_width, orig_height = self.background.get_size()
        self.background = pygame.transform.scale(
            self.background, (orig_width // 2, orig_height // 2)
        )
        # Apply rounded corners
        self.background = round_corners(self.background, radius=30)
        # Centered rect
        self.bg_rect = self.background.get_rect(center=(self.width // 2, self.height // 2))

        # Font
        pygame.font.init()
        self.font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 60)

        # Return button
        self.return_btn = BoxButton("RETURN", (self.width // 2, self.height - 100), font=self.font)

    # -----------------------------
    #   LOAD SCORES
    # -----------------------------
    def load_scores(self):
        if not os.path.exists(self.score_file):
            self.scores = []
            return

        with open(self.score_file, "r") as f:
            try:
                self.scores = json.load(f)
            except json.JSONDecodeError:
                self.scores = []

        # Sort descending and keep top 10
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]

    # -----------------------------
    #   DRAW
    # -----------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))  # clear screen
        self.screen.blit(self.background, self.bg_rect)

        # Draw scores
        start_y = 400
        spacing = 70
        for i, entry in enumerate(self.scores):
            name = entry.get("name", "Unknown")
            score = entry.get("score", 0)
            text = f"{i+1}. {name} - {score}"
            label = self.font.render(text, True, (255, 255, 255))
            rect = label.get_rect(center=(self.width // 2, start_y + i * spacing))
            self.screen.blit(label, rect)

        # Draw return button
        self.return_btn.draw(self.screen)

        pygame.display.flip()

    # -----------------------------
    #   RUN LOOP
    # -----------------------------
    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.return_btn.handle_event(event):
                    return
