import pygame
import socket
import json
import threading
import time

# --- Paramètres ---
SERVER_IP = "10.60.104.178"   # à remplacer par l'IP du serveur si besoin
SERVER_PORT = 50006
BUFFER_SIZE = 4096

# --- Paramètres du monde ---
WORLD_W, WORLD_H = 800, 600
PLAYER_RADIUS = 10


# --- Classe principale du client ---
class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.player_id = None
        self.players = {}
        self.lock = threading.Lock()

    def connect(self):
        """Connexion au serveur"""
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=5)
            self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print(f"[CLIENT] Connecté à {self.host}:{self.port}")
            self.running = True
            # Démarrer le thread de réception
            threading.Thread(target=self.listen_server, daemon=True).start()
        except Exception as e:
            print(f"[CLIENT] Erreur de connexion : {e}")
            self.running = False

    def listen_server(self):
        """Écoute en continu les messages JSON du serveur"""
        try:
            f = self.sock.makefile("r", encoding="utf-8", newline="\n")
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Traitement des messages
                if msg["type"] == "welcome":
                    self.player_id = msg["id"]
                    print(f"[CLIENT] Bienvenue ! ID = {self.player_id}")
                elif msg["type"] == "state":
                    with self.lock:
                        self.players = {p["id"]: p for p in msg["players"]}
        except Exception as e:
            print(f"[CLIENT] Erreur réception : {e}")
        finally:
            print("[CLIENT] Déconnexion du serveur.")
            self.running = False

    def send_input(self, dx, dy):
        """Envoie les entrées de déplacement"""
        if not self.running:
            return
        msg = {"type": "input", "dx": dx, "dy": dy}
        try:
            data = (json.dumps(msg) + "\n").encode("utf-8")
            self.sock.sendall(data)
        except OSError:
            self.running = False

    def close(self):
        """Fermeture propre"""
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        if self.sock:
            self.sock.close()


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
    run_game(SERVER_IP, SERVER_PORT)
