import pygame
from src.core.camera import CameraGroup
from src.data.save import SaveData
from src.ui.dialog.dialog import DialogBox, Aide
from src.ui.touche import Touche



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
aide_interaction = Aide(["Appuie sur le bouton [F] pour ouvrir le menu"])
liste_aides_message = [aide_interaction, aide_teleportation]

city_before_enigm_collisions = pygame.sprite.Group()
city_after_enigm_collisions = pygame.sprite.Group()
bar_collisions = pygame.sprite.Group()
bar_hallway_toilets_collisions = pygame.sprite.Group()
bar_toilets_collisions = pygame.sprite.Group()
bar_cave_before_opened_chest_collisions = pygame.sprite.Group()
bar_cave_after_opened_chest_collisions = pygame.sprite.Group()
transition_city_port_collisions = pygame.sprite.Group()
port_collisions = pygame.sprite.Group()
labyrinthe_collisions = pygame.sprite.Group()

camera_groups = {
    "Bar": CameraGroup(name_map='Bar', list_teleporters=[('EntranceBarHallwayToilets', 'BarHallwayToilets', 'EntranceBarHallwayToilets'), ('EntranceBarCave', 'BarCaveBeforeOpenedChest', 'EntranceBarCave'), ('ExitBar', 'CityBeforeEnigm', 'ExitBar')], layers_obstacles=(['Collisions'], bar_collisions), name_interaction="PrintAlcools"),
    "BarHallwayToilets": CameraGroup(name_map='BarHallwayToilets', list_teleporters=[('ExitBarHallwayToilets', 'Bar', 'ExitBarHallwayToilets'), ('EntranceBarToilets', 'BarToilets', 'EntranceBarToilets')], layers_obstacles=(['Collisions'], bar_hallway_toilets_collisions), name_interaction="SomonGame"),
    "BarToilets": CameraGroup(name_map='BarToilets', list_teleporters=[('ExitBarToilets', 'BarHallwayToilets', 'ExitBarToilets')], layers_obstacles=(['Collisions'], bar_toilets_collisions), name_interaction="TicketDeCaisse"),
    "BarCaveBeforeOpenedChest": CameraGroup(name_map='BarCaveBeforeOpenedChest', list_teleporters=[('ExitBarCave', 'Bar', 'ExitBarCave')], layers_obstacles=(['Collisions'], bar_cave_before_opened_chest_collisions), name_interaction="CadenasGame"),
    "BarCaveAfterOpenedChest": CameraGroup(name_map='BarCaveAfterOpenedChest', list_teleporters=[('ExitBarCave', 'Bar', 'ExitBarCave')], layers_obstacles=(['Collisions'], bar_cave_after_opened_chest_collisions), name_interaction="AucuneInteraction"),
    "CityBeforeEnigm": CameraGroup(name_map='CityBeforeEnigm', list_teleporters=[('EntranceBar', 'Bar', 'EntranceBar'), ('ExitCity', 'TransitionCityPort', 'ExitCity'), ('TrapLabyrinthe', 'Labyrinthe', 'TrapLabyrinthe')], layers_obstacles=(['Collisions'], city_before_enigm_collisions), name_interaction="AucuneInteraction"),
    "CityAfterEnigm": CameraGroup(name_map='CityAfterEnigm', list_teleporters=[('EntranceBar', 'Bar', 'EntranceBar'), ('ExitCity', 'TransitionCityPort', 'ExitCity')], layers_obstacles=(['Collisions'], city_after_enigm_collisions), name_interaction="AucuneInteraction"),
    "Labyrinthe": CameraGroup(name_map='Labyrinthe', list_teleporters=[('ExitLabyrinthe', 'CityAfterEnigm', 'ExitLabyrinthe')], layers_obstacles=(['Collisions'], labyrinthe_collisions), name_interaction="OpenPanneauMeteo"),
    "TransitionCityPort": CameraGroup(name_map='TransitionCityPort', list_teleporters=[('EntrancePort', 'Port', 'EntrancePort'), ('EntranceCity', 'CityBeforeEnigm', 'EntranceCity')], layers_obstacles=(['Collisions'], transition_city_port_collisions), name_interaction="AucuneInteraction"),
    "Port": CameraGroup(name_map='Port', list_teleporters=[('ExitPort', 'TransitionCityPort', 'ExitPort')], layers_obstacles=(['Collisions'], port_collisions), name_interaction="FinishGame"),
}

save_data = SaveData('src/data/save.json')
map_name = save_data.load_player_map()
mob_dead = save_data.load_mob_dead()

if map_name is None:
    camera_group = camera_groups["BarToilets"]
else:
    camera_group = camera_groups[map_name]