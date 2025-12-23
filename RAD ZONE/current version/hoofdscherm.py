import pygame
import sys
from ui import BoxButton
from pathlib import Path
from sound_manager import SoundManager

# -----------------------------
#        INITIALIZATION
# -----------------------------
pygame.init()

# Base directory (folder this file is in)
BASE_DIR = Path(__file__).resolve().parent

# -----------------------------
#        FONT SETUP
# -----------------------------
FONT_PATH = BASE_DIR / "Fonts" / "Sixtyfour-Regular-VariableFont_BLED,SCAN.ttf"

if FONT_PATH.exists():
    font = pygame.font.Font(str(FONT_PATH), 36)
else:
    print("Font file not found! Using default system font.")
    font = pygame.font.SysFont(None, 48)

# -----------------------------
#       HELPER FUNCTION
# -----------------------------
def round_corners(image, radius):
    """Return a copy of the image with rounded corners of given radius."""
    size = image.get_size()
    rounded_surf = pygame.Surface(size, pygame.SRCALPHA)

    rect = pygame.Rect(0, 0, *size)
    pygame.draw.rect(
        rounded_surf,
        (255, 255, 255, 255),
        rect,
        border_radius=radius
    )

    rounded_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded_surf

# -----------------------------
#            MENU
# -----------------------------
class Menu:
    def __init__(self, screen, items, sound_manager):
        self.screen = screen
        self.items = items
        self.sound = sound_manager
        self.width, self.height = self.screen.get_size()

        # -----------------------------
        #   LOAD BACKGROUND
        # -----------------------------
        background_path = BASE_DIR / "Graphics" / "achtergrond menu.png"
        self.background = pygame.image.load(str(background_path)).convert_alpha()

        orig_width, orig_height = self.background.get_size()
        self.background = pygame.transform.scale(
            self.background,
            (orig_width // 2, orig_height // 2)
        )

        self.background = round_corners(self.background, radius=30)
        self.bg_rect = self.background.get_rect(
            center=(self.width // 2, self.height // 2)
        )

        # -----------------------------
        #   CREATE BUTTONS
        # -----------------------------
        center_x = self.width // 2
        start_y = 550
        spacing = int(self.height * 0.04)

        menu_font = pygame.font.Font(str(FONT_PATH), 24) if FONT_PATH.exists() else pygame.font.SysFont(None, 48)

        self.buttons = {
            "Play": BoxButton("PLAY", (center_x, start_y + spacing * 0), size=(95, 35), font=menu_font),
            "Scoreboard": BoxButton("SCOREBOARD", (center_x, start_y + spacing * 1), size=(240, 35), font=menu_font),
            "Settings": BoxButton("SETTINGS", (center_x, start_y + spacing * 2), size=(190, 35), font=menu_font),
            "Credits": BoxButton("CREDITS", (center_x, start_y + spacing * 3), size=(170, 35), font=menu_font),
            "Quit": BoxButton("EXIT", (center_x, start_y + spacing * 4), size=(105, 35), font=menu_font),
        }

    # -----------------------------
    #           DRAW MENU
    # -----------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.bg_rect)

        for btn in self.buttons.values():
            btn.draw(self.screen)

        pygame.display.flip()

    # -----------------------------
    #           RUN LOOP
    # -----------------------------
    def run(self):
        menu_music = BASE_DIR / "Audio" / "intro_loop_3.wav"

        # Play menu music ONCE via SoundManager
        if not pygame.mixer.music.get_busy():
            self.sound.play_music(menu_music, loop=True, start=0.0,)

        

        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sound.stop_music()
                    pygame.quit()
                    sys.exit()

                for name, btn in self.buttons.items():
                    if btn.handle_event(event):
                        if name == "Play":
                            self.sound.stop_music()
                            return "Play"
                        elif name == "Settings":
                            return "Settings"
                        elif name == "Scoreboard":
                            return "Scoreboard"
                        elif name == "Credits":
                            return "Credits"
                        elif name == "Quit":
                            self.sound.stop_music()
                            pygame.quit()
                            sys.exit()
