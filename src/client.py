import pygame
import socket
import threading
import json

SERVER_IP = "10.60.104.178"  # 🔁 à modifier selon ton réseau local
PORT = 5000

# --- Initialisation réseau
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, PORT))

players = {}

def listen_server():
    global players
    buffer = ""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            buffer += data.decode()
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if message.strip():
                    players = json.loads(message)
        except Exception as e:
            print("Erreur de réception :", e)
            break

threading.Thread(target=listen_server, daemon=True).start()

# --- Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

speed = 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]: dx = -speed
    if keys[pygame.K_RIGHT]: dx = speed
    if keys[pygame.K_UP]: dy = -speed
    if keys[pygame.K_DOWN]: dy = speed

    if dx or dy:
        msg = {"action": "move", "dx": dx, "dy": dy}
        sock.send(json.dumps(msg).encode())

    # --- affichage
    screen.fill((30, 30, 30))
    for p in players.values():
        pygame.draw.rect(screen, p["color"], (p["x"], p["y"], 30, 30))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sock.close()
