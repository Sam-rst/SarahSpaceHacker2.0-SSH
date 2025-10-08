import pygame

from src.network.client import GameClient
from src.ui.menus.menu_server_connection import MenuServerConnection

# --- Paramètres ---
SERVER_IP = "10.60.104.178"   # à remplacer par l'IP du serveur si besoin
SERVER_PORT = 50006
BUFFER_SIZE = 4096

# --- Paramètres du monde ---
WORLD_W, WORLD_H = 800, 600
PLAYER_RADIUS = 10

# --- Boucle de jeu Pygame ---
def run_game(host, port):
    pygame.init()
    screen = pygame.display.set_mode((WORLD_W, WORLD_H))
    pygame.display.set_caption("Client Coop LAN")
    clock = pygame.time.Clock()

    client = GameClient(host, port)
    client.connect()

    # --- Boucle principale ---
    while client.running:
        dt = clock.tick(60) / 1000.0
        dx = dy = 0

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1

        # Envoi des entrées
        if dx != 0 or dy != 0:
            client.send_input(dx, dy)

        # --- Affichage ---
        screen.fill((20, 20, 30))
        with client.lock:
            for pid, p in client.players.items():
                color = tuple(p["color"])
                pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"])), PLAYER_RADIUS)
                if pid == client.player_id:
                    pygame.draw.circle(screen, (255, 255, 255), (int(p["x"]), int(p["y"])), PLAYER_RADIUS, 2)

        pygame.display.flip()

    client.close()
    pygame.quit()

if __name__ == "__main__":
    print("[CLIENT] Démarrage...")
    authenticated = False
    while not authenticated:
        host, port = MenuServerConnection().run_connect_menu()
        if host and port:
            authenticated = True

    run_game(host, port)