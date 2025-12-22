import pygame
from ui import BoxButton
from audio_menu import Audio_Menu
from controls_menu import ControlsMenu
from sys import exit


class PauseMenu:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        w, h = self.screen.get_size()
        self.width, self.height = w, h

        start_y = 300
        spacing = int(h * 0.05)
        center_x = w // 2

        font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 48)

        # Buttons
        self.buttons = {
            "Resume": BoxButton("RESUME", (center_x, start_y), size=(180, 45), font=font),
            "Audio Settings": BoxButton("AUDIO SETTINGS", (center_x, start_y + spacing * 1), size=(370, 45), font=font),
            "Controls": BoxButton("CONTROLS", (center_x, start_y + spacing * 2), size=(230, 45), font=font),
            "Quit": BoxButton("QUIT", (center_x, start_y + spacing * 3), size=(130, 45), font=font),
        }

    def draw(self, game_surface):
        """Draw the paused overlay and buttons."""
        # Draw frozen game snapshot
        self.screen.blit(game_surface, (0, 0))

        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Draw buttons
        for btn in self.buttons.values():
            btn.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        """Handle a single event. Returns the action string if a button is clicked."""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        for name, btn in self.buttons.items():
            if btn.handle_event(event):
                return name
        return None

    def run_blocking(self, game_surface):
        """
        Run the pause menu in a blocking loop, fully freezing the game.
        Returns the chosen action: "Resume" or "Quit".
        """
        clock = pygame.time.Clock()
        while True:
            self.draw(game_surface)

            for event in pygame.event.get():
                action = self.handle_event(event)
                if action == "Resume":
                    return "Resume"
                elif action == "Quit":
                    return "Quit"
                elif action == "Audio Settings":
                    Audio_Menu(self.screen, self.sound_manager).run()
                elif action == "Controls":
                    ControlsMenu(self.screen, self.sound_manager).run()

            clock.tick(60)
