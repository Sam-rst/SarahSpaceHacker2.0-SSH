import pygame, random, sys
from src.core.settings import screen
from src.core.sprites import player_sprite, camera_group, camera_groups
from src.data.save import SaveData
from src.domain.player import Player


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
        self.CYAN = (50, 180, 255)

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
        if self.class_joueur is None:
            largeur_bouton = 200
            bouton_start = pygame.Rect((self.WIDTH - largeur_bouton) / 2, 800, largeur_bouton, 50)

            # Créer des gouttes de texte "Matrix" au début
            # self.create_drops(50)  # Nombre initial de gouttes

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
                            print("#"*40)
                            print(camera_group.carte.map_name)
                            print("#"*40)
                            player = Player("Sarah", camera_group.carte.get_waypoint('Spawn'),
                                            [player_sprite] + list(camera_groups.values()))
                            player_position = {"x": player.pos.x, "y": player.pos.y}
                            self.save_data.save_player_position(player_position)
                            self.save_data.save_player_map(camera_group.carte.map_name)
                            self.save_data.save_player_life(player.get_HP())
                            return player

                screen.fill(self.BLACK)

                texte_bienvenue = self.font_grand.render("Bienvenue dans Sarah Lost Island : Les retours aux sources !", True, self.CYAN)
                screen.blit(texte_bienvenue, ((self.WIDTH - texte_bienvenue.get_width()) / 2, 150))

                # Dessiner les gouttes de texte "Matrix"
                for drop in self.drops:
                    text_surface = self.font.render(drop.character, True, self.CYAN)
                    screen.blit(text_surface, (drop.x, drop.y))
                    drop.fall()

                image_commandes = pygame.image.load("src/assets/touches/commandes.png")
                image_commandes = pygame.transform.scale(image_commandes, (1000, 600))
                screen.blit(image_commandes, (250, 120))

                pygame.draw.rect(screen, self.CYAN, bouton_start, border_radius=10)
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
                player = Player("Sarah", camera_group.carte.get_waypoint('Spawn'),
                                [player_sprite] + list(camera_groups.values()))

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
