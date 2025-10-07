import socket
import threading
import json

# --- Détermination automatique de l'adresse IP locale ---
def get_local_ip():
    try:
        # Crée une connexion "factice" pour déterminer l'IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # pas besoin que ça réponde
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"  # fallback

HOST = "0.0.0.0"
PORT = 5000
SERVER_IP = get_local_ip()

clients = {}
players = {}
lock = threading.Lock()

def broadcast(state):
    data = (json.dumps(state) + "\n").encode()
    for conn in clients.values():
        try:
            conn.sendall(data)
        except:
            pass


def handle_client(conn, addr, player_id):
    print(f"[+] Nouveau joueur {player_id} depuis {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = json.loads(data.decode())

            with lock:
                player = players[player_id]
                if msg["action"] == "move":
                    dx, dy = msg["dx"], msg["dy"]
                    player["x"] += dx
                    player["y"] += dy
                    players[player_id] = player

                broadcast(players)

        except ConnectionResetError:
            break
        except Exception as e:
            print("Erreur :", e)
            break

    print(f"[-] Joueur {player_id} déconnecté")
    with lock:
        del clients[player_id]
        del players[player_id]
        broadcast(players)
    conn.close()

# --- Initialisation du serveur ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("===================================")
print("🎮 Serveur multijoueur Pygame démarré !")
print(f"📡 Adresse IP locale : {SERVER_IP}")
print(f"🔌 Port d'écoute     : {PORT}")
print("💡 Les clients doivent utiliser cette IP dans client.py")
print("===================================\n")

player_counter = 0

while True:
    conn, addr = s.accept()
    player_id = f"player_{player_counter}"
    clients[player_id] = conn
    players[player_id] = {
        "x": 100 + 50 * player_counter,
        "y": 100,
        "color": [255, 0, 0] if player_counter == 0 else [0, 0, 255]
    }
    player_counter += 1
    threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()
    broadcast(players)
