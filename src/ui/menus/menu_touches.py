import pygame, random, sys
from src.core.settings import screen


class MenuTouches:
    def __init__(self):

        # Configuration de la fenêtre
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        # Couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        # Création de la liste des caractères "1" et "0"
        self.characters = ["0", "1"]

        # Création de la liste pour stocker les gouttes de texte
        self.drops = []

        # Polices de caractères
        self.font_grand = pygame.font.Font('src/assets/font/Gixel.ttf', 50)
        self.font = pygame.font.Font('src/assets/font/Gixel.ttf', 30)

    def create_drops(self, num_drops):
        for _ in range(num_drops):
            self.drops.append(self.Drop(self.WIDTH, self.HEIGHT, self.characters))  # Passer WIDTH, HEIGHT et characters

    class Drop:
        def __init__(self, WIDTH, HEIGHT, characters):
            self.WIDTH = WIDTH  # Récupérer WIDTH depuis Menu
            self.HEIGHT = HEIGHT  # Récupérer HEIGHT depuis Menu
            self.characters = characters  # Récupérer characters depuis Menu
            self.x = random.randint(0, self.WIDTH)
            self.y = random.randint(-100, 0)
            self.speed = random.randint(2, 5)
            self.character = random.choice(self.characters)

        def fall(self):
            self.y += self.speed
            if self.y > self.HEIGHT:
                self.y = random.randint(-100, 0)

    def run(self):
        largeur_bouton = 200
        bouton_continuer = pygame.Rect((self.WIDTH - largeur_bouton) / 2, 800, largeur_bouton, 50)

        # Créer des gouttes de texte "Matrix" au début
        self.create_drops(50)  # Nombre initial de gouttes
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_continuer.collidepoint(pygame.mouse.get_pos()):
                        running = False

            screen.fill(self.BLACK)

            texte_bienvenue = self.font_grand.render("Comment jouer ?", True, self.GREEN)
            screen.blit(texte_bienvenue, ((self.WIDTH - texte_bienvenue.get_width()) / 2, 150))

            # Dessiner les gouttes de texte "Matrix"
            for drop in self.drops:
                text_surface = self.font.render(drop.character, True, self.GREEN)
                screen.blit(text_surface, (drop.x, drop.y))
                drop.fall()

            image_commandes = pygame.image.load("src/assets/touches/commandes.png")
            image_commandes = pygame.transform.scale(image_commandes, (1000, 600))
            screen.blit(image_commandes, (250, 120))

            pygame.draw.rect(screen, self.GREEN, bouton_continuer, border_radius=10)
            pygame.draw.rect(screen, self.BLACK, bouton_continuer, 3, border_radius=10)

            texte_start = self.font.render("Continuer", True, self.BLACK)

            # Utilisez cette ligne pour centrer le texte dans le bouton
            texte_rect = texte_start.get_rect()
            texte_rect.center = bouton_continuer.center
            screen.blit(texte_start, texte_rect)

            pygame.display.flip()
            pygame.time.delay(7)
