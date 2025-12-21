import pygame
from sys import exit
from ui import BoxButton


class CreditsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()

        # Achtergrond zwart
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))

        # Fonts
        self.title_font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 50)  # Tussentitels
        self.text_font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 40)   # Normale tekst

        # Credits tekst (type, line)
        self.credits = [
            ("The team behind Rad zone:", ["Keanu Aleart", "Manu De Smedt", "Esper Merckx", "Michiel Vanmossevelde", "Wouter Wingels"]),
            ("Verdeling taken voor projectweek:", "" ),
            ("Graphic Design:", ["Michiel", "Esper", "Keanu"]),
            ("Programming:", ["Wouter", "Keanu", "Manu", "Esper", "Michiel"]),
            ("Soundtrack:", ["Manu", "Michiel"]),
            ("Sound Design:", ["Manu"]),
            ("Voice Acting:", ["Esper", "Wouter", "Keanu", "Manu", "Michiel"]),
            ("Websites that helped us:", ""),
            ("Sound effects:", ["pixabay.com"]),
            ("Sprites:",  ["(Itch.io)", "Goncharov_Denis", "ArcadeIsland", "RanitayaStudio", "JackBurton84", "CraftPix.net"]),
            ("Gen AI", ["ChatGPT", "Gemini AI", "Microsoft copilot"]),
        ]




        # Scroll instellingen
        self.start_y = self.height
        self.scroll_speed = 1  # pixels per frame
        self.line_spacing_title = 60
        self.line_spacing_text = 40
        self.line_spacing_section = 100

        font = pygame.font.Font("RAD ZONE/UI/Menu/edit-undo.brk.ttf", 40)
        self.quit_btn = BoxButton(
            "RETURN",
            (self.width // 2, self.height -1000),
            size=(250, 60),
            font=font
        )

        # Soundtrack starten vanaf bepaald punt, loopend
        pygame.mixer.init()
        pygame.mixer.music.load("RAD ZONE/current version/Audio/RAD_ZONE_SOUNDTRACK.wav")
        pygame.mixer.music.play(loops=-1, start=30)  # start op 30 seconden, herhaling oneindig

    # def draw(self):
    #     self.screen.blit(self.background, (0, 0))
    #     y = self.start_y
    #     prev_type = None

    #     # Tekst tekenen
    #     for typ, line in self.credits:
    #         # Extra spatie tussen secties
    #         if typ == "title" and prev_type == "text":
    #             y += self.line_spacing_section

    #         # Renderen
    #         if typ == "title":
    #             surf = self.title_font.render(line, True, (255, 255, 255))
    #             y += self.line_spacing_title
    #         else:
    #             surf = self.text_font.render(line, True, (200, 200, 200))
    #             y += self.line_spacing_text

    #         rect = surf.get_rect(center=(self.width // 2, y))
    #         self.screen.blit(surf, rect)
    #         prev_type = typ

    #     # Scroll positie update
    #     self.start_y -= self.scroll_speed

    #     # Reset scroll wanneer alles voorbij is
    #     total_height = y + 100  # extra marge onderaan
    #     if total_height < 0:
    #         self.start_y = self.height

    #     # Quit-knop tekenen
    #     self.quit_btn.draw(self.screen)
    #     pygame.display.flip()


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        y = self.start_y

        role_x = 300                    # Left-aligned role column
        name_x = self.width // 2 * 1.3       # Start x-position for names
        role_name_spacing = 20         # Space between role and first name

        for role, names in self.credits:
            # Draw role
            role_surf = self.title_font.render(role, True, (255, 255, 255))
            role_rect = role_surf.get_rect(topleft=(role_x, y))
            self.screen.blit(role_surf, role_rect)

            # Draw first name on the same line as role
            if names:
                first_name_surf = self.text_font.render(names[0], True, (200, 200, 200))
                first_name_rect = first_name_surf.get_rect(topleft=(name_x, y))
                self.screen.blit(first_name_surf, first_name_rect)

                # Move y down for subsequent names
                y += self.line_spacing_text

                for name in names[1:]:
                    name_surf = self.text_font.render(name, True, (200, 200, 200))
                    name_rect = name_surf.get_rect(topleft=(name_x, y))
                    self.screen.blit(name_surf, name_rect)
                    y += self.line_spacing_text
            else:
                y += self.line_spacing_text  # no names, still add spacing

            # Extra spacing between roles
            y += self.line_spacing_section

        # Scroll
        self.start_y -= self.scroll_speed

        # Reset scroll if all text has gone
        total_height = y + 100
        if total_height < 0:
            self.start_y = self.height

        # Draw quit button
        self.quit_btn.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()
                if self.quit_btn.handle_event(event):
                    pygame.mixer.music.stop()
                    return
