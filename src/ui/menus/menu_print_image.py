import pygame
import sys


class MenuPrintImage:
    def __init__(self, image_name):
        """
        Initialise le menu avec une image.

        Args:
            image_name (str): Chemin vers l'image à afficher
        """
        pygame.init()

        # Charger l'image
        try:
            self.image = pygame.image.load(image_name)
            self.image_rect = self.image.get_rect()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            sys.exit()

        # Créer la fenêtre avec la taille de l'image
        self.screen = pygame.display.set_mode((self.image_rect.width, self.image_rect.height))
        pygame.display.set_caption("Menu Image")

        # Horloge pour gérer les FPS
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        """Gère les événements du menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        """Affiche l'image à l'écran."""
        self.screen.blit(self.image, (0, 0))
        pygame.display.flip()

    def run(self):
        """Boucle principale du menu."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        # pygame.quit()


# Exemple d'utilisation
if __name__ == "__main__":
    # Remplacer 'votre_image.png' par le chemin de votre image
    menu = MenuPrintImage("../../../src/assets/interactions/ticket_caisse_bar.png")
    menu.run()