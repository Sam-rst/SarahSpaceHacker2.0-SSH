import pygame
import math
import random
import time

# Initialisation
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu Simon")
clock = pygame.time.Clock()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)

# Couleurs des secteurs (normal, illuminé)
COLORS = [
    ((200, 150, 0), (255, 200, 0)),  # Orange foncé/clair
    ((200, 200, 0), (255, 255, 100)),  # Jaune
    ((150, 0, 0), (255, 50, 50)),  # Rouge
    ((100, 80, 60), (150, 120, 90)),  # Marron
    ((150, 100, 200), (200, 150, 255)),  # Violet
    ((0, 100, 150), (50, 180, 255)),  # Cyan
    ((0, 0, 150), (50, 50, 255)),  # Bleu
    ((100, 150, 100), (150, 255, 150)),  # Vert pâle
]


# Sons (fréquences différentes pour chaque secteur)
def play_tone(sector):
    """Joue un son pour le secteur"""
    frequencies = [262, 294, 330, 349, 392, 440, 494, 523]  # Do à Do
    # Note: pygame.mixer.Sound peut être utilisé pour de vrais sons
    pass  # Simplifié pour cet exemple


class SimonGame:
    def __init__(self):
        self.center = (WIDTH // 2, 320)
        self.outer_radius = 200
        self.inner_radius = 60
        self.sectors = []
        self.sequence = []
        self.player_sequence = []
        self.current_step = 0
        self.game_state = "WAITING"  # WAITING, SHOWING, PLAYING, GAMEOVER
        self.score = 0
        self.lit_sector = None
        self.lit_time = 0

        self.create_sectors()
        self.new_game()

    def create_sectors(self):
        """Crée les 8 secteurs du Simon"""
        num_sectors = 8
        angle_per_sector = 360 / num_sectors

        for i in range(num_sectors):
            start_angle = i * angle_per_sector - 90  # -90 pour commencer en haut
            end_angle = start_angle + angle_per_sector
            self.sectors.append({
                'id': i,
                'start_angle': start_angle,
                'end_angle': end_angle,
                'colors': COLORS[i]
            })

    def draw_sector(self, sector, is_lit=False):
        """Dessine un secteur"""
        start_angle = math.radians(sector['start_angle'])
        end_angle = math.radians(sector['end_angle'])

        # Créer les points du polygone
        points = [self.center]

        # Points sur l'arc extérieur
        num_points = 20
        for j in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * j / num_points
            x = self.center[0] + self.outer_radius * math.cos(angle)
            y = self.center[1] + self.outer_radius * math.sin(angle)
            points.append((x, y))

        # Points sur l'arc intérieur (en sens inverse)
        for j in range(num_points, -1, -1):
            angle = start_angle + (end_angle - start_angle) * j / num_points
            x = self.center[0] + self.inner_radius * math.cos(angle)
            y = self.center[1] + self.inner_radius * math.sin(angle)
            points.append((x, y))

        # Dessiner le secteur
        color = sector['colors'][1] if is_lit else sector['colors'][0]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)  # Bordure

    def get_clicked_sector(self, pos):
        """Retourne le secteur cliqué ou None"""
        dx = pos[0] - self.center[0]
        dy = pos[1] - self.center[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Vérifier si dans la zone cliquable
        if distance > self.outer_radius or distance < self.inner_radius:
            return None

        # Calculer l'angle
        angle = math.degrees(math.atan2(dy, dx)) + 90  # +90 pour aligner avec nos secteurs
        angle = (angle + 360) % 360

        # Trouver le secteur
        for sector in self.sectors:
            start = (sector['start_angle'] + 90) % 360
            end = (sector['end_angle'] + 90) % 360

            if start > end:  # Secteur qui traverse 0°
                if angle >= start or angle <= end:
                    return sector['id']
            else:
                if start <= angle <= end:
                    return sector['id']

        return None

    def new_game(self):
        """Démarre une nouvelle partie"""
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.game_state = "WAITING"
        self.add_to_sequence()

    def add_to_sequence(self):
        """Ajoute un élément à la séquence"""
        self.sequence.append(random.randint(0, 7))
        self.score = len(self.sequence) - 1

    def show_sequence(self):
        """Montre la séquence au joueur"""
        self.game_state = "SHOWING"
        self.current_step = 0

    def light_sector(self, sector_id, duration=500):
        """Illumine un secteur"""
        self.lit_sector = sector_id
        self.lit_time = pygame.time.get_ticks()
        play_tone(sector_id)

    def player_click(self, sector_id):
        """Gère le clic du joueur"""
        if self.game_state != "PLAYING":
            return

        self.light_sector(sector_id, 200)
        self.player_sequence.append(sector_id)

        # Vérifier si c'est correct
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            self.game_state = "GAMEOVER"
            return

        # Si séquence complète
        if len(self.player_sequence) == len(self.sequence):
            self.player_sequence = []
            self.add_to_sequence()
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Attendre 1s avant de rejouer

    def update(self):
        """Met à jour le jeu"""
        current_time = pygame.time.get_ticks()

        # Éteindre le secteur illuminé
        if self.lit_sector is not None and current_time - self.lit_time > 300:
            self.lit_sector = None

        # Montrer la séquence
        if self.game_state == "SHOWING":
            if self.lit_sector is None:
                if self.current_step < len(self.sequence):
                    self.light_sector(self.sequence[self.current_step])
                    self.current_step += 1
                    pygame.time.set_timer(pygame.USEREVENT, 600)
                else:
                    self.game_state = "PLAYING"
                    self.player_sequence = []

    def draw(self):
        """Dessine le jeu"""
        screen.fill(DARK_GRAY)

        # Dessiner tous les secteurs
        for sector in self.sectors:
            is_lit = sector['id'] == self.lit_sector
            self.draw_sector(sector, is_lit)

        # Cercle central avec texte "SIMON"
        pygame.draw.circle(screen, BLACK, self.center, self.inner_radius)
        pygame.draw.circle(screen, WHITE, self.center, self.inner_radius, 3)

        font = pygame.font.Font(None, 32)
        text = font.render("SIMON", True, WHITE)
        text_rect = text.get_rect(center=self.center)
        screen.blit(text, text_rect)

        # Afficher les instructions et le score
        font_small = pygame.font.Font(None, 28)

        msg = ""
        if self.game_state == "WAITING":
            msg = "Cliquez sur START pour commencer"
        elif self.game_state == "SHOWING":
            msg = "Mémorisez la séquence..."
        elif self.game_state == "PLAYING":
            msg = "À votre tour !"
        elif self.game_state == "GAMEOVER":
            msg = "GAME OVER ! Cliquez sur START"

        text = font_small.render(msg, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 580))

        # Score
        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 620))

        # Bouton START
        button_rect = pygame.Rect(WIDTH // 2 - 60, 650, 120, 40)
        pygame.draw.rect(screen, (0, 150, 0), button_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=5)
        start_text = font_small.render("START", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 658))


# Jeu principal
game = SimonGame()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                # Vérifier bouton START
                button_rect = pygame.Rect(WIDTH // 2 - 60, 650, 120, 40)
                if button_rect.collidepoint(event.pos):
                    if game.game_state in ["WAITING", "GAMEOVER"]:
                        game.new_game()
                        game.show_sequence()

                # Vérifier clic sur secteur
                else:
                    sector_id = game.get_clicked_sector(event.pos)
                    if sector_id is not None:
                        game.player_click(sector_id)

        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Désactiver le timer

        elif event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            game.show_sequence()

    game.update()
    game.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()