from enum import Enum
import pygame
import math
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu Somon - Combinaison Secrète")
clock = pygame.time.Clock()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 200, 0)


class ColorsSectorsEnum(Enum):
    """Enumération des couleurs des secteurs (normal, illuminé)"""
    ORANGE = ((200, 150, 0), (255, 200, 0))
    JAUNE = ((200, 200, 0), (255, 255, 100))
    ROUGE = ((150, 0, 0), (255, 50, 50))
    MARRON = ((100, 80, 60), (150, 120, 90))
    VIOLET = ((150, 100, 200), (200, 150, 255))
    CYAN = ((0, 100, 150), (50, 180, 255))
    BLEU = ((0, 0, 150), (50, 50, 255))
    VERT = ((100, 150, 100), (150, 255, 150))


class GameState(Enum):
    """États possibles du jeu"""
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ABANDONNED = "ABANDONNED"


class Sector:
    """Représente un secteur du jeu Somon"""

    def __init__(self, sector_id: int, color: ColorsSectorsEnum, angle_per_sector: float):
        self.id: int = sector_id
        self.color: ColorsSectorsEnum = color
        self.angle_per_sector: float = angle_per_sector
        self.start_angle: float = self._calculate_start_angle(sector_id, angle_per_sector)
        self.end_angle: float = self._calculate_end_angle(self.start_angle, angle_per_sector)

    def _calculate_start_angle(self, i: int, angle_per_sector: float) -> float:
        """Calcule l'angle de départ du secteur"""
        return i * angle_per_sector - 90  # -90 pour commencer en haut

    def _calculate_end_angle(self, start_angle: float, angle_per_sector: float) -> float:
        """Calcule l'angle de fin du secteur"""
        return start_angle + angle_per_sector

    def get_normal_color(self) -> tuple:
        """Retourne la couleur normale du secteur"""
        return self.color.value[0]

    def get_lit_color(self) -> tuple:
        """Retourne la couleur illuminée du secteur"""
        return self.color.value[1]

    def __eq__(self, other):
        """Permet de comparer deux secteurs"""
        if isinstance(other, Sector):
            return self.id == other.id
        return False

    def __repr__(self):
        """Représentation textuelle du secteur"""
        return f"Sector({self.color.name})"


BUTTON_BOTTOM = pygame.Rect(WIDTH // 2 - 70, 660, 140, 35)

class SomonGame:
    """Classe principale du jeu Somon"""

    def __init__(self):
        self.center: tuple[int, int] = (WIDTH // 2, 320)
        self.outer_radius: int = 200
        self.inner_radius: int = 60
        self.sectors: list[Sector] = []
        self.secret_combination: list[Sector] = []
        self.player_sequence: list[Sector] = []
        self.game_state: GameState = GameState.WAITING
        self.lit_sector: Sector | None = None
        self.lit_time: int = 0
        self.attempts: int = 0

        self._create_sectors()
        self.new_game()

    def _create_sectors(self) -> None:
        """Crée les 8 secteurs du Somon"""
        num_sectors = 8
        angle_per_sector = 360 / num_sectors

        colors = list(ColorsSectorsEnum)
        for i in range(num_sectors):
            self.sectors.append(Sector(i, colors[i], angle_per_sector))

    def draw_sector(self, sector: Sector, is_lit: bool = False) -> None:
        """Dessine un secteur"""
        start_angle = math.radians(sector.start_angle)
        end_angle = math.radians(sector.end_angle)

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
        color = sector.get_lit_color() if is_lit else sector.get_normal_color()
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)  # Bordure

    def get_clicked_sector(self, pos: tuple[int, int]) -> Sector | None:
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
            start = (sector.start_angle + 90) % 360
            end = (sector.end_angle + 90) % 360

            if start > end:  # Secteur qui traverse 0°
                if angle >= start or angle <= end:
                    return sector
            else:
                if start <= angle <= end:
                    return sector

        return None

    def new_game(self) -> None:
        """Démarre une nouvelle partie avec une combinaison secrète"""
        # Définir une combinaison fixe ou aléatoire
        # Combinaison fixe :
        self.secret_combination = [
            self.sectors[7],  # VERT
            self.sectors[2],  # ROUGE
            self.sectors[5],  # CYAN
            self.sectors[0]  # ORANGE
        ]

        # Ou combinaison aléatoire :
        # self.secret_combination = [random.choice(self.sectors) for _ in range(4)]

        self.player_sequence = []
        self.game_state = GameState.PLAYING
        self.attempts = 0
        print(f"[DEBUG] Combinaison secrète: {[s.color.name for s in self.secret_combination]}")

    def light_sector(self, sector: Sector, duration: int = 200) -> None:
        """Illumine un secteur"""
        self.lit_sector = sector
        self.lit_time = pygame.time.get_ticks()

    def player_click(self, sector: Sector) -> None:
        """Gère le clic du joueur"""
        if self.game_state != GameState.PLAYING:
            return

        self.light_sector(sector)
        self.player_sequence.append(sector)

        # Vérifier si la combinaison est complète
        if len(self.player_sequence) == len(self.secret_combination):
            self.attempts += 1

            # Vérifier si c'est la bonne combinaison
            if self.player_sequence == self.secret_combination:
                self.game_state = GameState.SUCCESS
            else:
                # Mauvaise combinaison, on réinitialise
                self.game_state = GameState.FAILED
                pygame.time.set_timer(pygame.USEREVENT, 800)  # Attendre avant de reset

    def reset_player_sequence(self) -> None:
        """Réinitialise la séquence du joueur"""
        self.player_sequence = []
        if self.game_state == GameState.FAILED:
            self.game_state = GameState.PLAYING

    def update(self) -> None:
        """Met à jour le jeu"""
        current_time = pygame.time.get_ticks()

        # Éteindre le secteur illuminé
        if self.lit_sector is not None and current_time - self.lit_time > 200:
            self.lit_sector = None

    def draw(self) -> None:
        """Dessine le jeu"""
        screen.fill(DARK_GRAY)

        # Dessiner tous les secteurs
        for sector in self.sectors:
            is_lit = self.lit_sector is not None and sector.id == self.lit_sector.id
            self.draw_sector(sector, is_lit)

        # Cercle central avec texte "SOMON"
        pygame.draw.circle(screen, BLACK, self.center, self.inner_radius)
        pygame.draw.circle(screen, WHITE, self.center, self.inner_radius, 3)

        font = pygame.font.Font(None, 32)
        text = font.render("SOMON", True, WHITE)
        text_rect = text.get_rect(center=self.center)
        screen.blit(text, text_rect)

        # Afficher les instructions
        font_small = pygame.font.Font(None, 26)

        msg = ""
        if self.game_state == GameState.WAITING:
            msg = "Cliquez sur JOUER pour commencer"
        elif self.game_state == GameState.PLAYING:
            msg = f"Trouvez la combinaison secrète ({len(self.secret_combination)} couleurs)"
        elif self.game_state == GameState.SUCCESS:
            msg = "🎉 BIEN JOUÉ ! 🎉"
        elif self.game_state == GameState.FAILED:
            msg = "Dommage... Réessayez !"

        text = font_small.render(msg, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 560))

        if self.game_state == GameState.SUCCESS:
            attempts_msg = f"Réussi en {self.attempts} tentative(s) !"
            text2 = font_small.render(attempts_msg, True, GREEN)
            screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 590))

        # Afficher la séquence du joueur
        sequence_y = 625
        font_tiny = pygame.font.Font(None, 22)
        seq_text = font_tiny.render("Votre séquence:", True, WHITE)
        screen.blit(seq_text, (20, sequence_y))

        # Dessiner les petits cercles pour la séquence
        circle_x = 150
        for i in range(len(self.secret_combination)):
            if i < len(self.player_sequence):
                color = self.player_sequence[i].get_normal_color()
            else:
                color = (60, 60, 60)  # Gris pour les cases vides

            pygame.draw.circle(screen, color, (circle_x + i * 35, sequence_y + 10), 12)
            pygame.draw.circle(screen, WHITE, (circle_x + i * 35, sequence_y + 10), 12, 2)

        # Bouton JOUER / REJOUER


        if self.game_state == GameState.SUCCESS:
            button_color = (0, 150, 0)
            button_text = "CONTINUER"
        else:
            button_color = (0, 0, 150)
            button_text = "RETOUR"

        pygame.draw.rect(screen, button_color, BUTTON_BOTTOM, border_radius=5)
        pygame.draw.rect(screen, WHITE, BUTTON_BOTTOM, 2, border_radius=5)
        btn_text = font_small.render(button_text, True, WHITE)
        screen.blit(btn_text, (WIDTH // 2 - btn_text.get_width() // 2, 665))


# Jeu principal
    def run(self):
        game = SomonGame()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        # Vérifier bouton RETOUR/CONTINUER
                        if BUTTON_BOTTOM.collidepoint(event.pos):
                            if game.game_state in [GameState.WAITING]:
                                game.new_game()
                            elif game.game_state in [GameState.SUCCESS]:
                                running = False
                            elif game.game_state == GameState.PLAYING:
                                game.reset_player_sequence()
                            else:
                                running = False

                        # Vérifier clic sur secteur
                        else:
                            sector = game.get_clicked_sector(event.pos)
                            if sector is not None:
                                game.player_click(sector)

                elif event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Désactiver le timer
                    game.reset_player_sequence()

            game.update()
            game.draw()
            pygame.display.flip()
            clock.tick(60)

        # pygame.quit()


if __name__ == "__main__":
    game = SomonGame()
    game.run()