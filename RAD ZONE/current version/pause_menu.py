import pygame
from ui import BoxButton


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        w, h = self.screen.get_size()
        self.width, self.height = w, h

        start_y = 250
        spacing = int(h * 0.12)
        center_x = w // 2

        font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 48)

        # Knoppen laden
        base = "RAD ZONE/UI/Menu/"
        button_width = w // 4
        self.buttons = {
            "Resume": BoxButton("RESUME", (center_x, start_y), font=font),
            "Quit": BoxButton("QUIT", (center_x, start_y + spacing), font=font),
        }

    def draw(self, game_surface):
        # Grijs overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(game_surface, (0, 0))
        self.screen.blit(overlay, (0, 0))

        for btn in self.buttons.values():
            btn.draw(self.screen)
        pygame.display.flip()

    def run(self, game_surface):
        while True:
            self.draw(game_surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                for name, btn in self.buttons.items():
                    if btn.handle_event(event):
                        return name
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "Resume"
