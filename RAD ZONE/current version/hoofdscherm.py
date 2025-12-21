import pygame
import sys
from ui import BoxButton
import os

# initialize pygame first

pygame.init()  # ensure pygame is initialized

# Build font path relative to this script
# font_path = os.path.join(os.path.dirname(__file__), "Fonts", "undertow", "UNDERTOW.ttf")
font_path = os.path.join(os.path.dirname(__file__), "Fonts", "darkmode", "darkmode demo-Regular.ttf")

if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 48)
else:
    print("Font file not found! Using default system font.")
    font = pygame.font.SysFont(None, 48)

# -----------------------------
#       HELPER FUNCTION
# -----------------------------
def round_corners(image, radius):
    """Return a copy of the image with rounded corners of given radius."""
    size = image.get_size()
    # Create a temporary surface with alpha
    rounded_surf = pygame.Surface(size, pygame.SRCALPHA)
    
    # Draw a filled rounded rectangle
    rect = pygame.Rect(0, 0, *size)
    pygame.draw.rect(rounded_surf, (255, 255, 255, 255), rect, border_radius=radius)
    
    # Copy the image onto the rounded rectangle using BLEND_RGBA_MULT
    rounded_surf.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return rounded_surf

# -----------------------------
#            MENU
# -----------------------------
class Menu:
    def __init__(self, screen, items):
        self.screen = screen
        self.items = items  # ["Play", "Scoreboard", "Credits", "Exit Game"]
        self.width, self.height = self.screen.get_size()

        # -----------------------------
        #   LOAD BACKGROUND
        # -----------------------------
        self.background = pygame.image.load(
            "RAD ZONE/UI/Menu/achtergrond menu.png"
        ).convert_alpha()

        # Scale to half size
        orig_width, orig_height = self.background.get_size()
        self.background = pygame.transform.scale(
            self.background, (orig_width // 2, orig_height // 2)
        )

        # Apply rounded corners
        self.background = round_corners(self.background, radius=30)

        # Get rect centered
        self.bg_rect = self.background.get_rect(center=(self.width // 2, self.height // 2))

        # -----------------------------
        #   LOAD & START MUSIC
        # -----------------------------
        pygame.mixer.init()
        pygame.mixer.music.load("RAD ZONE/current version/MP3/intro_loop.mp3")
        pygame.mixer.music.set_volume(0.7)
        start_second = 5
        pygame.mixer.music.play(-1, start=start_second)

        # -----------------------------
        #   CREATE BUTTONS
        # -----------------------------
        center_x = self.width // 2
        start_y = 580
        spacing = int(self.height * 0.06)

        font = pygame.font.Font(font_path, 48)

        self.buttons = {
            "Play": BoxButton("PLAY", (center_x, start_y + spacing * 0), size=(80, 60), font=font),
            "Scoreboard": BoxButton("SCOREBOARD", (center_x, start_y + spacing * 1), size=(180, 60),font=font),
            "Credits": BoxButton("CREDITS", (center_x, start_y + spacing * 2), size=(130, 60),font=font),
            "Quit": BoxButton("EXIT GAME", (center_x, start_y + spacing * 3), size=(150, 60),font=font),
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
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

                # Check button clicks
                for name, btn in self.buttons.items():
                    if btn.handle_event(event):
                        if name == "Play":
                            pygame.mixer.music.stop()  # Stop music
                        return name
