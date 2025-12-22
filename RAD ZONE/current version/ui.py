import pygame

class UI:
    def __init__(self, health, stamina, outline):
        self._health_surf, self._health_rect = health
        self._stamina_surf, self._stamina_rect = stamina
        self._outline_surf = outline[0]
        self._font = pygame.font.SysFont(None, 48)  # Font for wave display

    def draw(self, screen, health, max_health, stamina, max_stamina, wave=1):
        # ---------- HEALTH (SHRINKS) ----------
        health_ratio = 0 if max_health <= 0 else max(0, min(health / max_health, 1))
        health_pos = self._health_rect.topleft

        if health_ratio > 0:
            width = int(self._health_surf.get_width() * health_ratio)
            health_part = self._health_surf.subsurface(
                (0, 0, width, self._health_surf.get_height())
            )
            screen.blit(health_part, health_pos)

        # Health outline on top
        screen.blit(self._outline_surf, health_pos)

        # ---------- STAMINA (SHRINKS) ----------
        stamina_ratio = 0 if max_stamina <= 0 else max(0, min(stamina / max_stamina, 1))
        stamina_pos = self._stamina_rect.topleft

        if stamina_ratio > 0:
            width = int(self._stamina_surf.get_width() * stamina_ratio)
            stamina_part = self._stamina_surf.subsurface(
                (0, 0, width, self._stamina_surf.get_height())
            )
            screen.blit(stamina_part, stamina_pos)

        screen.blit(self._outline_surf, stamina_pos)

        # ---------- WAVE DISPLAY ----------
        wave_text = self._font.render(f"Wave {wave}", True, (255, 255, 255))
        screen.blit(wave_text, (screen.get_width() // 2 - wave_text.get_width() // 2, 20))

class BoxButton:
    def __init__(
        self,
        text,
        center,
        size=(300, 70),
        font="Fonts/darkmode/Darkmode demo-Regular.ttf",
        idle_color=(12, 32, 17, 100),
        hover_color=(52, 168, 34, 150),
        pressed_color=(120, 120, 120, 200),
        text_color=(138, 250, 48),
        border_color=(74, 111, 5, 100),
        border_width=3,
        shadow_color=(0, 0, 0),          # default black shadow
        shadow_offset=(4, 4)             # default offset
    ):
        self.text = text
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center

        # Font handling
        if isinstance(font, str) and font:  # font path
            try:
                self.font = pygame.font.Font(font, 48)
            except:
                print(f"Failed to load font {font}, using default font")
                self.font = pygame.font.SysFont(None, 48)
        else:  # font object
            self.font = font or pygame.font.SysFont(None, 48)

        self.idle_color = idle_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width

        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset

        self.is_down = False

    def draw(self, screen):
        # Determine current button color
        mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.idle_color
        if self.is_down:
            color = self.pressed_color
        elif mouse_over:
            color = self.hover_color

        # Draw button background
        temp_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, color, temp_surf.get_rect(), border_radius=8)

        # Draw border if needed
        if self.border_width > 0:
            pygame.draw.rect(temp_surf, self.border_color, temp_surf.get_rect(), self.border_width, border_radius=8)

        # Blit background
        screen.blit(temp_surf, self.rect.topleft)

        # Draw text shadow first
        if self.shadow_color and self.shadow_offset != (0, 0):
            shadow_surf = self.font.render(self.text, True, self.shadow_color)
            shadow_rect = shadow_surf.get_rect(center=(self.rect.centerx + self.shadow_offset[0],
                                                       self.rect.centery + self.shadow_offset[1]))
            screen.blit(shadow_surf, shadow_rect)

        # Draw main text on top
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_down = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_down:
                self.is_down = False
                if self.rect.collidepoint(event.pos):
                    return True
        return False


