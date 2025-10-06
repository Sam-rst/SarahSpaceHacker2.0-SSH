import pygame, sys, random
from dice import Dice
from save import SaveData
from player import *
from camera import *
from sprites import *

screen = pygame.display.get_surface()

class MenuDebut:
    def __init__(self):
        self.save_data = SaveData('save.json')
        self.class_joueur = self.save_data.load_player_class()
        self.player_data = self.save_data.load_player_data()
        self.player_HP = self.save_data.load_player_life()
        self.map_name = self.save_data.load_player_map()

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
        self.font_grand = pygame.font.Font('graphics/font/Gixel.ttf', 50)
        self.font = pygame.font.Font('graphics/font/Gixel.ttf', 30)

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
        if self.class_joueur is None:
            largeur_bouton = 200
            bouton_start = pygame.Rect((self.WIDTH - largeur_bouton) / 2, 800, largeur_bouton, 50)

            # Créer des gouttes de texte "Matrix" au début
            self.create_drops(50)  # Nombre initial de gouttes

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_start.collidepoint(pygame.mouse.get_pos()):
                            player = Player("Sarah", camera_group.carte.get_waypoint('Spawn'), [player_sprite] + list(camera_groups.values()))
                            player_position = {"x": player.pos.x, "y": player.pos.y}
                            self.save_data.save_player_position(player_position)
                            self.save_data.save_player_map(camera_group.carte.map_name) 
                            self.save_data.save_player_life(player.get_HP())
                            return player

                screen.fill(self.BLACK)
                
                texte_bienvenue = self.font_grand.render("Bienvenue dans Sarah Space Hacker", True, self.GREEN)
                screen.blit(texte_bienvenue, ((self.WIDTH - texte_bienvenue.get_width()) / 2, 150))

                # Dessiner les gouttes de texte "Matrix"
                for drop in self.drops:
                    text_surface = self.font.render(drop.character, True, self.GREEN)
                    screen.blit(text_surface, (drop.x, drop.y))
                    drop.fall()
                    
                image_commandes = pygame.image.load("graphics/touches/commandes.png")
                image_commandes = pygame.transform.scale(image_commandes, (1000, 600))
                screen.blit(image_commandes, (250, 120))
                

                pygame.draw.rect(screen, self.GREEN, bouton_start, border_radius=10)
                pygame.draw.rect(screen, self.BLACK, bouton_start, 3, border_radius=10)

                texte_start = self.font.render("Commencer", True, self.BLACK)

                # Utilisez cette ligne pour centrer le texte dans le bouton
                texte_rect = texte_start.get_rect()
                texte_rect.center = bouton_start.center
                screen.blit(texte_start, texte_rect)


                pygame.display.flip()
                pygame.time.delay(7)

        else:
            if self.class_joueur['Class'] == 'Player':
                player = Player("Sarah", camera_group.carte.get_waypoint('Spawn'), [player_sprite] + list(camera_groups.values()))
            
            name = self.class_joueur['Name']
            player.set_name(name)
            player.set_HP(self.player_HP)
            max_HP = self.class_joueur['Max HP']
            player.set_max_HP(max_HP)
            attack_value = self.class_joueur['Attack value']
            player.set_attack_value(attack_value)
            defend_value = self.class_joueur['Defend value']
            player.set_defense_value(defend_value)
            attack_range = self.class_joueur['Attack range']
            player.set_range(attack_range)
            player_pos = self.player_data.get('player_position')
            player.set_pos((player_pos['x'], player_pos['y']))

            return player

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
        self.font_grand = pygame.font.Font('graphics/font/Gixel.ttf', 50)
        self.font = pygame.font.Font('graphics/font/Gixel.ttf', 30)

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
                
            image_commandes = pygame.image.load("graphics/touches/commandes.png")
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