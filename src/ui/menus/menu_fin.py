import pygame, sys, random

from src.core import sprites
from src.core.sprites import *
from src.core.settings import screen


class MenuFin:

    def __init__(self):
        self.fireworks = []
        self.running = True
        self.menu_open = True

    def run(self):

        # Configuration de la fenêtre
        WIDTH, HEIGHT = screen.get_size()
        # screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # pygame.display.set_caption("Menu de victoire")

        # Couleurs
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)

        # Polices de caractères
        font = pygame.font.Font(None, 36)

        # Texte "YOU WIN"
        text_you_win = font.render("YOU WIN", True, WHITE)
        text_rect = text_you_win.get_rect(center=(WIDTH // 2, HEIGHT // 3))

        # Bouton "Continuer"
        bouton_width = 200
        bouton_height = 50
        continue_button = pygame.Rect(WIDTH // 2 - bouton_width // 2, 2 * HEIGHT // 3, bouton_width, bouton_height)
        continue_text = font.render("Continuer", True, BLACK)
        continue_text_rect = continue_text.get_rect(center=continue_button.center)

        # Espacement vertical entre les boutons
        button_spacing = 20

        # Bouton "Quitter"
        quit_button = pygame.Rect(WIDTH // 2 - bouton_width // 2, continue_button.bottom + button_spacing, bouton_width, bouton_height)
        quit_text = font.render("Quitter", True, BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        # Classe pour les feux d'artifice
        class Firework:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.radius = random.randint(2, 6)
                self.speed = random.randint(1, 5)

            def update(self):
                self.y -= self.speed

        fireworks = []

        running = True
        menu_open = True
        transition_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(transition_timer, 8000)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == transition_timer:
                    running = False
                if menu_open:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if continue_button.collidepoint(event.pos):
                            menu_open = False
                            sprites.camera_group = camera_groups["Salon"]
                        elif quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            screen.fill(BLACK if menu_open else BLACK)

            if menu_open:
                fireworks.append(Firework(random.randint(0, WIDTH), HEIGHT))

            for firework in fireworks:
                pygame.draw.circle(screen, firework.color, (firework.x, firework.y), firework.radius)
                firework.update()
                if firework.y < 0:
                    fireworks.remove(firework)

            if menu_open:
                # Dessin des boutons avec coins arrondis
                pygame.draw.rect(screen, WHITE, continue_button, border_radius=10)
                pygame.draw.rect(screen, WHITE, quit_button, border_radius=10)

                screen.blit(text_you_win, text_rect)
                screen.blit(continue_text, continue_text_rect)
                screen.blit(quit_text, quit_text_rect)

            pygame.time.delay(7)
            pygame.display.flip()