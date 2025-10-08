import pygame
import socket
import threading
from typing import Optional, Tuple

# Paramètres par défaut
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 50007
CONNECT_TIMEOUT = 3.0  # secondes

class InputField:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, allowed: str = "ip"):
        self.rect = rect
        self.text = text
        self.font = font
        self.focused = False
        self.allowed = allowed  # "ip" -> [0-9.] / "port" -> [0-9]
        self.caret_visible = True
        self._caret_timer = 0.0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)
        if not self.focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # La validation sera gérée à l'extérieur
                pass
            else:
                ch = event.unicode
                if self.allowed == "ip":
                    if ch.isdigit() or ch == ".":
                        self.text += ch
                elif self.allowed == "port":
                    if ch.isdigit():
                        self.text += ch

    def update(self, dt: float):
        self._caret_timer += dt
        if self._caret_timer >= 0.5:
            self._caret_timer = 0.0
            self.caret_visible = not self.caret_visible

    def draw(self, surf: pygame.Surface):
        # Fond
        pygame.draw.rect(surf, (34, 34, 42), self.rect, border_radius=6)
        pygame.draw.rect(surf, (90, 90, 110) if self.focused else (60, 60, 80), self.rect, width=2, border_radius=6)
        # Texte
        txt = self.font.render(self.text, True, (230, 230, 240))
        surf.blit(txt, (self.rect.x + 10, self.rect.y + (self.rect.height - txt.get_height()) // 2))
        # Caret
        if self.focused and self.caret_visible:
            caret_x = self.rect.x + 10 + txt.get_width() + 1
            caret_y = self.rect.y + 8
            pygame.draw.line(surf, (230, 230, 240), (caret_x, caret_y), (caret_x, self.rect.bottom - 8), 2)


class Button:
    def __init__(self, rect: pygame.Rect, label: str, font: pygame.font.Font, on_click):
        self.rect = rect
        self.label = label
        self.font = font
        self.on_click = on_click
        self._hover = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surf: pygame.Surface):
        base = (70, 110, 220) if self._hover else (60, 90, 190)
        pygame.draw.rect(surf, base, self.rect, border_radius=8)
        pygame.draw.rect(surf, (35, 50, 110), self.rect, width=2, border_radius=8)
        txt = self.font.render(self.label, True, (245, 245, 255))
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))


class ServerConnector:
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._busy = False
        self._ok = False
        self._error: Optional[str] = None
        self._endpoint: Optional[Tuple[str, int]] = None

    def try_connect(self, ip: str, port: int):
        if self._busy:
            return
        self._busy = True
        self._ok = False
        self._error = None

        def _run():
            try:
                # Test simple de connexion TCP, fermeture immédiate.
                with socket.create_connection((ip, port), timeout=CONNECT_TIMEOUT) as s:
                    # Optionnel: désactiver Nagle
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                with self._lock:
                    self._ok = True
                    self._endpoint = (ip, port)
            except Exception as e:
                with self._lock:
                    self._ok = False
                    self._error = str(e)
            finally:
                self._busy = False

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def is_busy(self) -> bool:
        return self._busy

    def result(self) -> Tuple[bool, Optional[str], Optional[Tuple[str, int]]]:
        with self._lock:
            return self._ok, self._error, self._endpoint


class MenuServerConnection:
    @staticmethod
    def run_connect_menu(on_success=None, default_ip: str = DEFAULT_IP, default_port: int = DEFAULT_PORT):
        pygame.init()
        pygame.display.set_caption("Connexion au serveur (LAN)")
        screen = pygame.display.set_mode((720, 420))
        clock = pygame.time.Clock()

        font_title = pygame.font.SysFont(None, 36)
        font = pygame.font.SysFont(None, 26)
        font_small = pygame.font.SysFont(None, 22)

        # Champs de saisie
        ip_field = InputField(pygame.Rect(220, 140, 280, 40), default_ip, font, allowed="ip")
        port_field = InputField(pygame.Rect(220, 200, 120, 40), str(default_port), font, allowed="port")

        connector = ServerConnector()
        status_text = ""
        status_color = (200, 200, 210)

        def on_click_connect():
            nonlocal status_text, status_color
            ip = ip_field.text.strip() or DEFAULT_IP
            try:
                port = int(port_field.text) if port_field.text.strip() else DEFAULT_PORT
            except ValueError:
                status_text = "Port invalide."
                status_color = (255, 120, 120)
                return

            status_text = f"Tentative de connexion à {ip}:{port}..."
            status_color = (200, 200, 210)
            connector.try_connect(ip, port)

        btn_connect = Button(pygame.Rect(520, 140, 160, 40), "Se connecter", font, on_click_connect)

        running = True
        connected_endpoint: Optional[Tuple[str, int]] = None

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                ip_field.handle_event(event)
                port_field.handle_event(event)
                btn_connect.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    on_click_connect()

            ip_field.update(dt)
            port_field.update(dt)

            # Mettre à jour l'état de connexion
            if connector.is_busy():
                status_text = "Connexion en cours..."
                status_color = (200, 200, 210)
            else:
                ok, err, endpoint = connector.result()
                if ok and endpoint and not connected_endpoint:
                    status_text = f"Connecté à {endpoint[0]}:{endpoint[1]}"
                    status_color = (140, 230, 140)
                    connected_endpoint = endpoint
                    # Si un callback est fourni, on le déclenche (ex: démarrer le client du jeu)
                    running = False
                elif err:
                    status_text = f"Échec: {err}"
                    status_color = (255, 120, 120)
                else:
                    status_text = f"Il y a eu un problème lors de la connexion au serveur"
                    status_color = (255, 120, 120)

            # Rendu
            screen.fill((18, 20, 28))
            title = font_title.render("Connexion à un serveur local", True, (240, 240, 255))
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

            lbl_ip = font_small.render("Adresse IP du serveur", True, (200, 200, 210))
            screen.blit(lbl_ip, (ip_field.rect.x, ip_field.rect.y - 24))
            ip_field.draw(screen)

            lbl_port = font_small.render("Port", True, (200, 200, 210))
            screen.blit(lbl_port, (port_field.rect.x, port_field.rect.y - 24))
            port_field.draw(screen)

            btn_connect.draw(screen)

            if status_text:
                st = font.render(status_text, True, status_color)
                screen.blit(st, (220, 260))

            hint = font_small.render("Astuce: entrez l'IP (ex: 192.168.1.42) puis cliquez Se connecter.", True, (160, 160, 180))
            screen.blit(hint, (220, 300))

            pygame.display.flip()

        pygame.quit()
        return connected_endpoint  # (ip, port) si connecté, sinon None