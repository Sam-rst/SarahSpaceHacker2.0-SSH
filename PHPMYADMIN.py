import asyncio
import pygame
import sys
import time

class LoginPage:
    def __init__(self):
        pygame.init()

        # Récupérer la taille de l'écran de l'ordinateur
        self.largeur, self.hauteur = pygame.display.Info().current_w, pygame.display.Info().current_h

        # Mettre la fenêtre en plein écran
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur), pygame.FULLSCREEN)

        pygame.display.set_caption("Page de Connexion")

        # Inverser les couleurs : arrière-plan blanc, texte noir
        self.blanc = (255, 255, 255)
        self.noir = (0, 0, 0)  # Arrière-plan noir, texte blanc

        self.rouge = (255, 0, 0)
        self.bleu = (0, 0, 255)

        self.police = pygame.font.Font(None, 36)

        self.nom_utilisateur = ""
        self.mot_de_passe = ""
        self.curseur_actif = None
        self.curseur_temps = 0
        self.message_erreur = ""
        self.message_connexion_reussie = ""
        self.connexion_reussie = False

        self.bouton_connexion = pygame.Rect(self.largeur // 2 - 100, self.hauteur - 150, 200, 50)
        self.clic_sur_bouton = False

        # Charger une image (remplacez 'logo.png' par le chemin de votre propre image)
        self.logo = pygame.image.load('assets/logo.png')

        # Temps où le message "Connexion réussie!" a été affiché
        self.temps_connexion_reussie = 0

        # Durée en millisecondes pendant laquelle le message "Connexion réussie!" sera affiché (5 secondes)
        self.duree_connexion_reussie = 5000

    async def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.est_clic_dans_champ(event.pos, self.largeur // 2 - 150, 520, 300, 40):
                        self.curseur_actif = "nom_utilisateur"
                        self.message_erreur = ""
                    elif self.est_clic_dans_champ(event.pos, self.largeur // 2 - 150, 620, 300, 40):
                        self.curseur_actif = "mot_de_passe"
                        self.message_erreur = ""
                    elif self.bouton_connexion.collidepoint(event.pos):
                        if self.verifier_connexion():
                            self.message_connexion_reussie = "Connexion réussie!"
                            self.connexion_reussie = True
                            self.temps_connexion_reussie = pygame.time.get_ticks()  # Enregistrer le temps
                            pygame.time.wait(1000)  # Attendre 1 seconde
                            running = False
                        else:
                            self.message_erreur = "Échec de la connexion. Veuillez réessayer."
                            self.nom_utilisateur = ""
                            self.mot_de_passe = ""
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.time.wait(100)
                    elif event.key == pygame.K_RETURN or (event.key == pygame.K_KP_ENTER and self.curseur_actif == "mot_de_passe"):
                        if self.verifier_connexion():
                            self.message_connexion_reussie = "Diriges toi vers la salle n°3, tente de rentrer dans un des serveurs."
                            self.connexion_reussie = True
                            self.temps_connexion_reussie = pygame.time.get_ticks()  # Enregistrer le temps
                            pygame.time.wait(1000)  # Attendre 1 seconde
                        else:
                            self.message_erreur = "Échec de la connexion. Veuillez réessayer."
                            self.nom_utilisateur = ""
                            self.mot_de_passe = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if self.curseur_actif == "nom_utilisateur":
                            if self.nom_utilisateur:
                                self.nom_utilisateur = self.nom_utilisateur[:-1]
                        elif self.curseur_actif == "mot_de_passe":
                            if self.mot_de_passe:
                                self.mot_de_passe = self.mot_de_passe[:-1]
                    else:
                        if self.curseur_actif == "nom_utilisateur":
                            self.nom_utilisateur += event.unicode
                        elif self.curseur_actif == "mot_de_passe":
                            self.mot_de_passe += event.unicode

            self.fenetre.fill(self.blanc)  # Arrière-plan blanc

            # Afficher le titre "Page de Connexion" en noir
            self.afficher_texte("Page de Connexion", (self.largeur // 2, 50), self.noir)

            # Afficher l'image sous le titre
            image_rect = self.logo.get_rect()
            image_rect.midtop = (self.largeur // 2, 100)  # Position de l'image
            self.fenetre.blit(self.logo, image_rect)

            # Texte "Nom d'utilisateur" et "Mot de passe" en noir
            self.afficher_texte("Nom d'utilisateur:", (self.largeur // 2 - 250 - 10, 520), self.noir)
            self.afficher_texte("Mot de passe:", (self.largeur // 2 - 250 - 10, 620), self.noir)

            nom_utilisateur_surface = self.police.render(self.nom_utilisateur, True, self.noir)

            # Masquer le mot de passe en le remplaçant par des étoiles (*) en noir
            mot_de_passe_masque = "*" * len(self.mot_de_passe)
            mot_de_passe_surface = self.police.render(mot_de_passe_masque, True, self.noir)

            if self.curseur_actif == "nom_utilisateur" and pygame.time.get_ticks() % 1000 > 500:
                nom_utilisateur_surface = self.police.render(self.nom_utilisateur + "|", True, self.noir)
            elif self.curseur_actif == "mot_de_passe" and pygame.time.get_ticks() % 1000 > 500:
                mot_de_passe_surface = self.police.render(mot_de_passe_masque + "|", True, self.noir)

            # Ajustez les coordonnées y pour placer les zones de texte légèrement plus bas
            self.fenetre.blit(nom_utilisateur_surface, (self.largeur // 2 - 150, 520))
            self.fenetre.blit(mot_de_passe_surface, (self.largeur // 2 - 150, 620))

            # Ajustez les coordonnées y des zones de texte pour les placer légèrement plus bas
            pygame.draw.rect(self.fenetre, self.noir, (self.largeur // 2 - 150, 510, 300, 40), 2)
            pygame.draw.rect(self.fenetre, self.noir, (self.largeur // 2 - 150, 610, 300, 40), 2)

            # Afficher le bouton de connexion avec la possibilité de le cliquer en noir
            pygame.draw.rect(self.fenetre, self.noir, self.bouton_connexion, 2)
            self.afficher_texte("Connexion", (self.bouton_connexion.centerx, self.bouton_connexion.centery), self.noir)

            # Afficher le message d'erreur en rouge
            self.afficher_texte(self.message_erreur, (self.largeur // 2, self.hauteur - 60), self.rouge)

            # Afficher le message de connexion réussie en bleu s'il est activé et si le temps n'a pas dépassé la durée
            if self.connexion_reussie:
                temps_actuel = pygame.time.get_ticks()
                # Vérifier si la durée d'affichage est dépassée, et si oui, réinitialiser la connexion
                if temps_actuel - self.temps_connexion_reussie >= self.duree_connexion_reussie:
                    self.connexion_reussie = False
                    self.message_connexion_reussie = ""
                else:
                    self.afficher_texte(self.message_connexion_reussie, (self.largeur // 2, self.hauteur - 60), self.bleu)

            pygame.display.flip()
            await asyncio.sleep(0)

    def afficher_texte(self, texte, position, couleur):
        texte_surface = self.police.render(texte, True, couleur)
        texte_rect = texte_surface.get_rect(center=position)
        self.fenetre.blit(texte_surface, texte_rect)

    def verifier_connexion(self):
        # Vérifier si le nom d'utilisateur est "root" et le mot de passe est "root"
        return self.nom_utilisateur == "root" and self.mot_de_passe == "root"

    def est_clic_dans_champ(self, position, x, y, largeur, hauteur):
        return x <= position[0] <= x + largeur and y <= position[1] <= y + hauteur

if __name__ == "__main__":
    page_connexion = LoginPage()
    page_connexion.run()