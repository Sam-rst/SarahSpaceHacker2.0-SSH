import pygame, sys

# -------------------
# Classe GameTimer
# -------------------
import pygame

class GameTimer:
    def __init__(self, total_seconds=5*60, font=None):
        """
        total_seconds : durée du timer en secondes (default 5 min)
        font : pygame font object
        """
        self.time_left = total_seconds
        self.font = font or pygame.font.SysFont("monospace", 48)
        self.game_over = False
        self.last_tick = pygame.time.get_ticks()
        self.blink_timer = 0
        self.begins = False

    def update(self):
        """Met à jour le timer toutes les secondes"""
        if self.game_over or not self.begins:
            return
        now = pygame.time.get_ticks()
        if now - self.last_tick >= 1000:  # 1 seconde
            self.time_left -= 1
            self.last_tick = now
            if self.time_left <= 0:
                self.game_over = True

    def draw(self, surface):
        """Affiche le timer en haut à gauche"""
        if self.game_over or not self.begins:
            return
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Couleur visible : blanc, rouge si <30 sec avec clignotement
        color = (255, 255, 255)
        if self.time_left <= 30:
            self.blink_timer += 1
            if self.blink_timer % 30 < 15:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)

        text_surface = self.font.render(timer_text, True, color)
        text_rect = text_surface.get_rect(topleft=(10, 10))
        surface.blit(text_surface, text_rect)

    def is_game_over(self):
        return self.game_over


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Timer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 48)

    # Crée un timer de 5 minutes
    game_timer = GameTimer(total_seconds=1*30, font=font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mettre à jour le timer
        game_timer.update()

        # Effacer l’écran
        screen.fill((0, 0, 0))

        # Dessiner le timer
        game_timer.draw(screen)

        # Afficher un message GAME OVER si besoin
        if game_timer.is_game_over():
            game_over_surface = font.render("GAME OVER", True, (255, 0, 0))
            rect = game_over_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(game_over_surface, rect)

        pygame.display.flip()
        clock.tick(60)