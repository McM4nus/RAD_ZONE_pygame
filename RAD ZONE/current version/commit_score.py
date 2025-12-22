import pygame
import json
import os
import sys
from ui import BoxButton

# -----------------------------
#       HELPER FUNCTION
# -----------------------------
def round_corners(image, radius):
    size = image.get_size()
    rounded_surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, *size)
    pygame.draw.rect(rounded_surf, (255, 255, 255, 255), rect, border_radius=radius)
    rounded_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded_surf

# -----------------------------
#   COMMIT SCORE SCREEN
# -----------------------------
class CommitScoreScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.clock = pygame.time.Clock()
        self.width, self.height = screen.get_size()

        # Letters and numbers
        self.characters = [chr(i) for i in range(65, 91)]  # A-Z
        self.characters += [str(i) for i in range(10)]     # 0-9
        self.characters.append("OK")                        # Confirm button

        # Layout
        self.cols = 10
        self.rows = (len(self.characters) + self.cols - 1) // self.cols
        self.cell_width = self.width // self.cols
        self.cell_height = 60

        # Cursor
        self.cursor_x = 0
        self.cursor_y = 0

        # Player name being entered
        self.name = []

        # Font
        font_path = os.path.join("RAD ZONE", "UI", "Menu", "edit-undo.brk.ttf")
        self.font = pygame.font.Font(font_path, 60)

        # Score file (consistent absolute path)
        self.score_file = os.path.join(os.path.dirname(__file__), "scores.json")
        os.makedirs(os.path.dirname(self.score_file), exist_ok=True)

    # -----------------------------
    #   DRAW SCREEN
    # -----------------------------
    def draw(self):
        self.screen.fill((20, 20, 20))

        title = self.font.render("Enter your initials (MAX 3)", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 50)))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
        self.screen.blit(score_text, score_text.get_rect(center=(self.width // 2, 100)))

        name_text = self.font.render("".join(self.name), True, (0, 255, 0))
        self.screen.blit(name_text, name_text.get_rect(center=(self.width // 2, 150)))

        for idx, char in enumerate(self.characters):
            col = idx % self.cols
            row = idx // self.cols
            x = col * self.cell_width + self.cell_width // 2
            y = 200 + row * self.cell_height
            color = (255, 255, 255)
            if col == self.cursor_x and row == self.cursor_y:
                color = (255, 0, 0)
            char_surf = self.font.render(char, True, color)
            self.screen.blit(char_surf, char_surf.get_rect(center=(x, y)))

        pygame.display.flip()

    # -----------------------------
    #   CLAMP CURSOR
    # -----------------------------
    def _clamp_cursor(self):
        idx = self.cursor_y * self.cols + self.cursor_x
        if idx >= len(self.characters):
            last_idx = len(self.characters) - 1
            self.cursor_y = last_idx // self.cols
            self.cursor_x = last_idx % self.cols

    # -----------------------------
    #   SAVE SCORE
    # -----------------------------
    def save_score(self, name, score):
        try:
            with open(self.score_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append({"name": name, "score": score})
        data.sort(key=lambda x: x["score"], reverse=True)
        data = data[:10]

        with open(self.score_file, "w") as f:
            json.dump(data, f, indent=4)

    # -----------------------------
    #   RUN LOOP FOR ENTERING NAME
    # -----------------------------
    def run(self):
        while True:
            self.clock.tick(60)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cursor_x = (self.cursor_x - 1) % self.cols
                        self._clamp_cursor()
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_x = (self.cursor_x + 1) % self.cols
                        self._clamp_cursor()
                    elif event.key == pygame.K_UP:
                        self.cursor_y = (self.cursor_y - 1) % self.rows
                        self._clamp_cursor()
                    elif event.key == pygame.K_DOWN:
                        self.cursor_y = (self.cursor_y + 1) % self.rows
                        self._clamp_cursor()

                    elif event.key == pygame.K_RETURN:
                        idx = self.cursor_y * self.cols + self.cursor_x
                        if idx >= len(self.characters):
                            continue
                        char = self.characters[idx]

                        if char == "OK":
                            player_name = "".join(self.name)
                            self.save_score(player_name, self.score)
                            # After saving, show scoreboard
                            Scoreboard(self.screen, self.score_file).reload_and_run()
                            return player_name
                        else:
                            if len(self.name) < 3:
                                self.name.append(char)

                    elif event.key == pygame.K_BACKSPACE:
                        if self.name:
                            self.name.pop()


# -----------------------------
#       SCOREBOARD CLASS
# -----------------------------
class Scoreboard:
    def __init__(self, screen, score_file=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.score_file = score_file or os.path.join(os.path.dirname(__file__), "scores.json")
        self.load_scores()

        # Background
        bg_path = os.path.join("RAD ZONE", "UI", "Menu", "achtergrond_scoreboard.png")
        self.background = pygame.image.load(bg_path).convert_alpha()
        orig_width, orig_height = self.background.get_size()
        self.background = pygame.transform.scale(self.background, (orig_width // 2, orig_height // 2))
        self.background = round_corners(self.background, 30)
        self.bg_rect = self.background.get_rect(center=(self.width // 2, self.height // 2))

        font_path = os.path.join("RAD ZONE", "current version", "Fonts", "Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf")
        self.font = pygame.font.Font(font_path, 24)

        self.return_btn = BoxButton("RETURN", (self.width // 2, self.height - 100), font=self.font)

    def load_scores(self):
        if not os.path.exists(self.score_file):
            self.scores = []
            return
        try:
            with open(self.score_file, "r") as f:
                self.scores = json.load(f)
        except json.JSONDecodeError:
            self.scores = []

        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.bg_rect)

        start_y = 400
        spacing = 30
        for i, entry in enumerate(self.scores):
            name = entry.get("name", "???")
            score = entry.get("score", 0)
            text = f"{i+1}. {name} - {score}"
            label = self.font.render(text, True, (255, 255, 255))
            rect = label.get_rect(center=(self.width // 2, start_y + i * spacing))
            self.screen.blit(label, rect)

        self.return_btn.draw(self.screen)
        pygame.display.flip()

    def run(self):
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

    # Reload scores and run (for after committing a score)
    def reload_and_run(self):
        self.load_scores()
        self.run()
