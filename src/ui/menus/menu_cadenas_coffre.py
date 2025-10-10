import pygame
import random
import math

pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (100, 150, 255)

# Configuration
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cadenas à 4 Chiffres")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)


class Dial:
    def __init__(self, x, y, radius=60):
        self.x = x
        self.y = y
        self.radius = radius
        self.current_value = 0
        self.dragging = False
        self.last_angle = 0

    def draw(self, screen):
        # Cercle extérieur (cadran)
        pygame.draw.circle(screen, DARK_GRAY, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius - 5)

        # Afficher les chiffres autour du cadran
        for i in range(10):
            angle = -math.pi / 2 + (i * 2 * math.pi / 10)
            text_x = self.x + int((self.radius - 25) * math.cos(angle))
            text_y = self.y + int((self.radius - 25) * math.sin(angle))
            text = small_font.render(str(i), True, WHITE)
            text_rect = text.get_rect(center=(text_x, text_y))
            screen.blit(text, text_rect)

        # Indicateur (flèche pointant vers le chiffre actuel)
        indicator_angle = -math.pi / 2 + (self.current_value * 2 * math.pi / 10)
        end_x = self.x + int((self.radius - 35) * math.cos(indicator_angle))
        end_y = self.y + int((self.radius - 35) * math.sin(indicator_angle))
        pygame.draw.line(screen, RED, (self.x, self.y), (end_x, end_y), 4)
        pygame.draw.circle(screen, RED, (self.x, self.y), 8)

        # Chiffre central
        value_text = font.render(str(self.current_value), True, GOLD)
        value_rect = value_text.get_rect(center=(self.x, self.y + self.radius + 35))
        screen.blit(value_text, value_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                dist = math.sqrt((event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2)
                if dist <= self.radius:
                    self.dragging = True
                    dx = event.pos[0] - self.x
                    dy = event.pos[1] - self.y
                    self.last_angle = math.atan2(dy, dx)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.x
                dy = event.pos[1] - self.y
                current_angle = math.atan2(dy, dx)

                angle_diff = current_angle - self.last_angle

                # Gérer le passage de -π à π
                if angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                elif angle_diff < -math.pi:
                    angle_diff += 2 * math.pi

                # Convertir en rotation de chiffres
                if abs(angle_diff) > 0.15:  # Seuil de sensibilité
                    if angle_diff > 0:
                        self.current_value = (self.current_value + 1) % 10
                    else:
                        self.current_value = (self.current_value - 1) % 10
                    self.last_angle = current_angle


class CadenasGame:
    def __init__(self):
        # Code secret aléatoire
        self.secret_code = [1, 9, 6, 3]
        print(f"Code secret: {self.secret_code}")  # Pour tricher pendant les tests ;)

        # Créer 4 cadrans
        spacing = 150
        start_x = WIDTH // 2 - (spacing * 3) // 2
        self.dials = [Dial(start_x + i * spacing, HEIGHT // 2) for i in range(4)]

        self.unlocked = False
        self.message = ""
        self.message_color = WHITE

    def check_code(self):
        current_code = [dial.current_value for dial in self.dials]
        print(current_code)
        if current_code == self.secret_code:
            self.unlocked = True
            self.message = "DÉVERROUILLÉ !"
            self.message_color = GREEN
        else:
            self.message = "Code incorrect"
            self.message_color = RED

    def reset(self):
        self.secret_code = [1, 9, 6, 3]
        print(f"Nouveau code secret: {self.secret_code}")
        for dial in self.dials:
            dial.current_value = 0
        self.unlocked = False
        self.message = ""

    def draw(self, screen):
        screen.fill((30, 30, 50))

        # Titre
        title = font.render("Cadenas à 4 Chiffres", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        # Instructions
        instr = small_font.render("Faites glisser les cadrans pour tourner", True, WHITE)
        screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 80))

        # Dessiner les cadrans
        for dial in self.dials:
            dial.draw(screen)

        # Bouton vérifier
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 120, 200, 50)
        color = GREEN if not self.unlocked else GRAY
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
        verify_text = small_font.render("VÉRIFIER", True, WHITE)
        screen.blit(verify_text, (button_rect.centerx - verify_text.get_width() // 2,
                                  button_rect.centery - verify_text.get_height() // 2))

        # Message
        if self.message:
            msg_text = font.render(self.message, True, self.message_color)
            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT - 200))

        # Bouton reset si déverrouillé
        if self.unlocked:
            reset_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)
            pygame.draw.rect(screen, BLUE, reset_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, reset_rect, 2, border_radius=8)
            reset_text = small_font.render("QUITTER", True, WHITE)
            screen.blit(reset_text, (reset_rect.centerx - reset_text.get_width() // 2,
                                     reset_rect.centery - reset_text.get_height() // 2))

        return button_rect if not self.unlocked else None, pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200,
                                                                       40) if self.unlocked else None


    # Boucle principale
    def run(self):
        game = CadenasGame()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Gérer les événements des cadrans
                for dial in game.dials:
                    dial.handle_event(event)

                # Gérer les clics sur les boutons
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button_rect, reset_rect = game.draw(screen)

                    if button_rect and button_rect.collidepoint(event.pos) and not game.unlocked:
                        game.check_code()

                    if reset_rect and reset_rect.collidepoint(event.pos) and game.unlocked:
                        running = False

            game.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        # pygame.quit()


if __name__ == "__main__":
    game = CadenasGame()
    game.run()