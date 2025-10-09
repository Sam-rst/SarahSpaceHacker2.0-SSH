import pygame, sys

class MenuGameOver:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = font or pygame.font.SysFont("monospace", 64)
        self.alpha = 0  # pour fade-in
        self.fade_speed = 5
        self.active = False

        # Surface pour overlay sombre
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(self.alpha)

    def start(self):
        """Active le menu"""
        self.active = True
        self.alpha = 0

    def update(self):
        """Animation fade-in"""
        if not self.active:
            return
        if self.alpha < 180:
            self.alpha += self.fade_speed
        self.overlay.set_alpha(self.alpha)

    def draw(self):
        if not self.active:
            return
        # Dessiner l'overlay sombre
        self.screen.blit(self.overlay, (0, 0))

        # Dessiner le texte Game Over
        text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, text_rect)

        # Optionnel : texte "Appuyez sur R pour rejouer"
        small_font = pygame.font.SysFont("monospace", 32)
        sub_text = small_font.render("Press R to Retry or ESC to Quit", True, (255, 255, 255))
        sub_rect = sub_text.get_rect(center=(self.width//2, self.height//2 + 80))
        self.screen.blit(sub_text, sub_rect)
