import pygame
from camera import CameraGroup
from save import SaveData
from dialog import DialogBox, Aide
from touche import Touche



all_sprites = pygame.sprite.Group()

projectile_sprites = pygame.sprite.Group()

ennemi_projectiles = pygame.sprite.Group()

items_drop = pygame.sprite.Group()

ennemi_group = pygame.sprite.Group()
pnj_group = pygame.sprite.Group()
player_sprite = pygame.sprite.GroupSingle()
player = None
items_drop = pygame.sprite.Group()
items_sprites = pygame.sprite.Group()

#Messages
dialogues_caporal_intro = DialogBox('caporal', ["Bonjour soldat !", "Aujourd'hui ta mission est de récupérer la...","...formule d'une arme chimique confidentielle.", "Elle est tombée dans les mains d'un groupe militant terroriste.","Pour te déplacer, utilise les touches  [Z]  pour avancer...","... [S] pour reculer, [Q] pour aller à gauche,  [D] pour aller a droite.","Pour intéragir avec les différents objets, appuie sur [A]. ","Pour quitter les différentes intéractions, appuie sur [ECHAP].", "Puis pour passer à la salle suivante.", "Apuie sur  [E]  pour te téléporter."])
dialogues_Emma_salon = DialogBox('emma', ["Bonjour Sarah, je m'appelle Emma.", "Je te guiderais tout au long de ton expédition.","Déplace-toi vers mon ordinateur puis connecte-toi .", "Appuie sur [E] pour te téléporter."])
dialogues_Emma_teleporter = DialogBox('emma', ["Incroyable ! Il semblerait que tu sois passé sans accroc.", "A partir de maintenant tu vas devoir passer dans toutes les salles en passant...", "...par le firewall, la salle serveur ainsi que la base de données !", "Ton objectif est donc de récupérer la formule chimique sous forme de parchemin, ", "il sera à la dernière salle devant une grande cuve tu ne pourras pas le louper !","Ne sois pas effrayée de cet environnement je resterais avec toi...","...tout le long de cette aventure ","Maintenant que les explications sont faites je te laisse passer...","...par cette porte à droite qui te guidera vers le firewall."])
dialogues_Emma_firewall_ferme = DialogBox('emma', ["Tu peux constater autour de toi différents portails.","Ces portails représentent des ports fermés.","Ton but est de trouver à partir d’un des ordinateurs du fond de la pièce...","...le port nécessaire pour accéder à la salle serveur.","Connecte donc toi à cet ordinateur et entre dans le terminal la commande “nmap”","Cette commande te permettra de savoir quelle port est ouvert.","Rends-toi en face d'un des ports que tu devras chercher et passe le portail."])
dialogues_Emma_firewall_ouvert = DialogBox('emma', ["Bravo, il semblerait que un port soit ouvert !","Déplace toi vers le port."])
dialogues_Emma_server = DialogBox('emma', ["Te voici à la moitié de ton périple !","Tu t’en sors déjà très bien.","Voici les salles serveurs, en anglais data center.","Ces salles sont généralement climatisées pour garder les composants...","... informatiques à bonnes températures permettant ainsi leurs bons entretiens. ","Ces salles permettent le fonctionnement optimal des systèmes informatiques", "Connecte-toi à l'ordinateur plus haut...", "... et rentre les identifiants suivants dans la base sql.","Les identifiants par défauts sont root pour l'identifiant et pour le mot de passe."])
dialogues_Emma_BDD = DialogBox('emma', ["Quelle structure impressionnante !", "Tu as devant toi une data, elle renferme ce qui nous intéresse.", "Les données sont stockées dans différentes capacités de stockage...","...telles que des disques durs, des serveurs, des clés usb, des clouds etc…", "Ces données sont stockées sous forme d’octet.","Pour te donner une image, le cerveau humain permet d'emmagasiner...","...l’équivalent de 1200 pétaoctet.","1 pétaoctet c’est 1000 fois la capacité d’un disque dur moderne.","Le cerveau humain est impressionnant n’est ce pas ?","Le but de ton périple se situe à l'intérieur de cette structure, passe le portail."])
dialogues_Emma_final = DialogBox('emma', ["Bravo à toi Sarah, tu as fini la démo de notre jeu !", "A présent, récupère le parchemin qui se trouve dans le coffre.", "A très bientôt !"])

#Touches
touches = pygame.sprite.Group()
touche_i = Touche("touche_i", touches)
touche_a = Touche("touche_a", touches)
touche_d = Touche("touche_d", touches)
touche_e = Touche("touche_e", touches)
touche_q = Touche("touche_q", touches)
touche_s = Touche("touche_s", touches)
touche_fleche_bas = Touche("touche_fleche_bas", touches)
touche_fleche_droite = Touche("touche_fleche_droite", touches)
touche_fleche_gauche = Touche("touche_fleche_gauche", touches)
touche_fleche_haut = Touche("touche_fleche_haut", touches)
touche_escape = Touche("touche_escape", touches)

aide_teleportation = Aide(["Appuie sur le bouton [E] pour te téléporter"])
aide_terminal = Aide(["Appuie sur le bouton [A] pour ouvrir le terminal"])
liste_aides_message = [aide_terminal, aide_teleportation]

first_room_collisions = pygame.sprite.Group()
salon_collisions = pygame.sprite.Group()
teleporter_collisions = pygame.sprite.Group()
firewall_collisions = pygame.sprite.Group()
server_collisions = pygame.sprite.Group()
bdd_collisions = pygame.sprite.Group()
final_collisions = pygame.sprite.Group()

camera_groups = {
    "FirstRoom": CameraGroup(name_map='FirstRoom', list_teleporters=[('EntranceSalon', 'Salon', 'EntranceSalon')], layers_obstacles=(['Collisions'], first_room_collisions), messages=dialogues_caporal_intro, name_interaction="AucuneInteraction"),
    "Salon": CameraGroup(name_map='Salon', list_teleporters=[('EntranceTeleporter', 'Teleporter', 'EntranceTeleporter'), ('ExitSalon', 'FirstRoom', 'ExitSalon')], layers_obstacles=(['Collisions'], salon_collisions), messages=dialogues_Emma_salon, name_interaction="AucuneInteraction"),
    "Teleporter": CameraGroup(name_map='Teleporter', list_teleporters=[('ExitTeleporter', 'Salon', 'ExitTeleporter'), ('EntranceFirewall', 'FirewallFerme', 'EntranceFirewall')], layers_obstacles=(['Collisions'], teleporter_collisions), messages=dialogues_Emma_teleporter, name_interaction="AucuneInteraction"),
    "FirewallFerme": CameraGroup(name_map='FirewallFerme', list_teleporters=[('ExitFirewall', 'Teleporter', 'ExitFirewall')], layers_obstacles=(['Collisions'], firewall_collisions), messages=dialogues_Emma_firewall_ferme, name_interaction="Terminal"),
    "FirewallOuvert": CameraGroup(name_map='FirewallOuvert', list_teleporters=[('ExitFirewall', 'Teleporter', 'ExitFirewall'), ('EntranceServer', 'Server', 'EntranceServer')], layers_obstacles=(['Collisions'], firewall_collisions), messages=dialogues_Emma_firewall_ouvert, name_interaction="AucuneInteraction"),
    "Server": CameraGroup(name_map='Server', list_teleporters=[('ExitServer', 'FirewallOuvert', 'ExitServer'), ('EntranceBDD', 'BDD', 'EntranceBDD')], layers_obstacles=(['Collisions'], server_collisions), messages=dialogues_Emma_server, name_interaction="BDD"),
    "BDD": CameraGroup(name_map='BDD', list_teleporters=[('ExitBDD', 'Server', 'ExitBDD'), ('EntranceFinal', 'FinalRoom', 'EntranceFinal')], layers_obstacles=(['Collisions'], bdd_collisions), messages=dialogues_Emma_BDD, name_interaction="Dezoom"),
    "FinalRoom": CameraGroup(name_map='FinalRoom', list_teleporters=[('EntranceFinal', 'FinalRoom', 'EntranceFinal'), ('ExitFinal', 'BDD', 'ExitFinal')], layers_obstacles=(['Collisions'], final_collisions), messages=dialogues_Emma_final, name_interaction="Parchemin"),
}
# Water Fall ;)

save_data = SaveData('save.json')
map_name = save_data.load_player_map()
mob_dead = save_data.load_mob_dead()

if map_name is None:
    camera_group = camera_groups["FirstRoom"]
else:
    camera_group = camera_groups[map_name]