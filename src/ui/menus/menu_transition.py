import pygame
from src.core.settings import screen


class Transition:

    def __init__(self):
        self.test = 'test'

    def run(self):
        # Configuration de la fenêtre
        WIDTH, HEIGHT = screen.get_size()

        # Couleur
        BLACK = (0, 0, 0)

        # Rayon de l'effet de téléportation
        teleport_radius = 0
        max_teleport_radius = max(WIDTH, HEIGHT)

        running = True

        transition_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(transition_timer, 1000)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == transition_timer:
                    running = False

            screen.fill(BLACK)

            # Effet de téléportation circulaire
            if teleport_radius < max_teleport_radius:
                pygame.draw.circle(screen, (121, 248, 248), (WIDTH // 2, HEIGHT // 2), teleport_radius, width=3)
                teleport_radius += 5  # Vitesse de l'effet de téléportation
            else:
                teleport_radius = 0  # Réinitialiser le rayon pour répéter l'effet

            pygame.display.flip()
            pygame.time.delay(6)

        running = False