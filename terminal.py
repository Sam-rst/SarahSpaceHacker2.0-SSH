import asyncio
import pygame
import sys
import time

class CMD:
    def __init__(self):
        pygame.init()

        self.largeur, self.hauteur = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Console Kali Linux Simulator")

        self.blanc = (255, 255, 255)
        self.noir = (0, 0, 0)

        self.police = pygame.font.Font(None, 36)
        self.texte = ""
        self.historique = []

        self.curseur_visible = True
        self.curseur_timer = time.time()

        self.menu_ouvert = False
        
        self.is_good = False

    def ouvrir_menu(self):
        self.menu_ouvert = True

    def fermer_menu(self):
        self.menu_ouvert = False

    def afficher_progression_nmap(self):
        nmap_resultats = [
            "Scanning...",
            "Port 80: Open",
            "Port 22: Open",
            "Port 443: Open",
            "Scan complet. 3 ports ouverts.",
            "Pour quitter : [ECHAP]"
        ]

        for resultat in nmap_resultats:
            self.historique.append(resultat)
            time.sleep(0.5)  # Pause d'une seconde pour simuler le chargement
            self.fenetre.fill(self.noir)
            self.afficher_console()
            pygame.display.flip()

    def afficher_console(self):
        y = 10
        for ligne in self.historique:
            texte_surface = self.police.render(ligne, True, self.blanc)
            self.fenetre.blit(texte_surface, (10, y))
            y += 40

        ligne_actuelle = "root@kali > " + self.texte
        texte_surface = self.police.render(ligne_actuelle, True, self.blanc)
        self.fenetre.blit(texte_surface, (10, self.hauteur - 50))

        if time.time() - self.curseur_timer > 0.5:
            self.curseur_visible = not self.curseur_visible
            self.curseur_timer = time.time()

        if self.curseur_visible:
            curseur_x = 130 + self.police.size(ligne_actuelle[:len(self.texte) + 2])[0]
            pygame.draw.line(self.fenetre, self.blanc, (curseur_x, self.hauteur - 50), (curseur_x, self.hauteur - 10), 2)

    async def run(self):
        running = True
        self.ouvrir_menu()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.time.wait(100)
                    elif self.menu_ouvert:
                        if event.key == pygame.K_RETURN:
                            self.historique.append(self.texte)
                            print(self.texte)  # Afficher le texte dans la console
                            if self.texte.lower() == "nmap":
                                self.afficher_progression_nmap()
                                self.is_good = True
                            else:
                                self.historique.append("Commande inconnue")
                            self.texte = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.texte = self.texte[:-1]
                        else:
                            self.texte += event.unicode

            self.fenetre.fill(self.noir)

            if self.menu_ouvert:
                self.afficher_console()
            else:
                # Fermez le menu
                self.historique = []
                self.texte = ""

            pygame.display.flip()
            await asyncio.sleep(0)

if __name__ == "__main__":
    menu = CMD()
    menu.run()
