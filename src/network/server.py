import argparse
import json
import socket
import threading
import time
from itertools import count
from random import randint

WORLD_W = 800
WORLD_H = 600
PLAYER_SPEED = 5
TICKRATE = 20  # Hz, diffusion d'état

lock = threading.Lock()
players = {}          # player_id -> {"x": int, "y": int, "color": [r,g,b]}
clients = {}          # player_id -> socket
_id_counter = count(1)
stop_event = threading.Event()


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def send_json_line(conn: socket.socket, obj: dict):
    data = (json.dumps(obj, separators=(",", ":")) + "\n").encode("utf-8")
    conn.sendall(data)


def snapshot_state():
    with lock:
        return {
            "type": "state",
            "players": [
                {"id": pid, "x": p["x"], "y": p["y"], "color": p["color"]}
                for pid, p in players.items()
            ],
        }


def broadcast_state():
    msg = snapshot_state()
    dead = []
    with lock:
        for pid, conn in list(clients.items()):
            try:
                send_json_line(conn, msg)
            except OSError:
                dead.append(pid)
    if dead:
        for pid in dead:
            remove_player(pid)


def broadcast_loop():
    interval = 1.0 / TICKRATE
    while not stop_event.is_set():
        broadcast_state()
        time.sleep(interval)


def remove_player(player_id: int):
    with lock:
        conn = clients.pop(player_id, None)
        players.pop(player_id, None)
    if conn:
        try:
            conn.close()
        except OSError:
            pass
    # Après suppression, envoyer un état à jour
    try:
        broadcast_state()
    except Exception:
        pass


def handle_client(conn: socket.socket, addr):
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    player_id = next(_id_counter)
    # Créer le joueur avec une couleur et une position de départ
    player = {
        "x": randint(50, WORLD_W - 50),
        "y": randint(50, WORLD_H - 50),
        "color": [randint(50, 255), randint(50, 255), randint(50, 255)],
    }

    with lock:
        players[player_id] = player
        clients[player_id] = conn

    # Message de bienvenue (id et dimensions du monde)
    try:
        send_json_line(conn, {"type": "welcome", "id": player_id, "world": {"w": WORLD_W, "h": WORLD_H}})
    except OSError:
        remove_player(player_id)
        return

    print(f"[+] Joueur {player_id} connecté depuis {addr}")

    # Lire les messages ligne par ligne
    try:
        f = conn.makefile("r", encoding="utf-8", newline="\n")
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            if msg.get("type") == "input":
                dx = int(msg.get("dx", 0))
                dy = int(msg.get("dy", 0))
                if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
                    continue
                with lock:
                    p = players.get(player_id)
                    if not p:
                        break
                    p["x"] = clamp(p["x"] + dx * PLAYER_SPEED, 0, WORLD_W)
                    p["y"] = clamp(p["y"] + dy * PLAYER_SPEED, 0, WORLD_H)
            # Vous pouvez étendre ici: tirs, collisions, scores, etc.

    except (ConnectionResetError, OSError):
        pass
    finally:
        print(f"[-] Joueur {player_id} déconnecté")
        remove_player(player_id)


def run_server(host: str, port: int):
    t_broadcast = threading.Thread(target=broadcast_loop, name="broadcast", daemon=True)
    t_broadcast.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"[SERVER] En écoute sur {host}:{port}")
        try:
            while not stop_event.is_set():
                s.settimeout(1.0)
                try:
                    conn, addr = s.accept()
                except socket.timeout:
                    continue
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\n[SERVER] Arrêt demandé...")
        finally:
            stop_event.set()
            # Fermer toutes les connexions
            with lock:
                conns = list(clients.values())
            for c in conns:
                try:
                    c.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    c.close()
                except OSError:
                    pass
            print("[SERVER] Terminé.")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serveur coop (LAN)")
    parser.add_argument("--host", default="0.0.0.0", help="Adresse d'écoute (0.0.0.0 pour LAN)")
    parser.add_argument("--port", type=int, default=5000, help="Port d'écoute")
    args = parser.parse_args()
    run_server(get_local_ip(), args.port)