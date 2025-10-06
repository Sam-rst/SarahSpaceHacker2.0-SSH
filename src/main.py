import pygame, sys, time
from settings import *
import sprites
from player import *
from ennemy import *
from menu import MenuDebut, MenuFin, Transition, MenuTouches
from pnj import *
from PHPMYADMIN import LoginPage
from terminal import CMD
from dialog import Aide

pygame.init()

clock = pygame.time.Clock()

parchemin_surf = pygame.image.load("assets/touches/parchemin.png")
parchemin_surf = pygame.transform.scale(parchemin_surf, (200, 256))
parchemin_rect = parchemin_surf.get_rect(topleft = (0, 0))

# Menus
login_page = LoginPage()
cmd = CMD()
menuDebut = MenuDebut()
menuFin = MenuFin()
transition = Transition()
menuTouches = MenuTouches()

# Saves
sprites.player = menuDebut.run()
last_save_time = pygame.time.get_ticks()

# Dialogues
emma = Emma("Emma", sprites.camera_group.carte.get_waypoint('SpawnEmmaSalon'), [sprites.camera_groups["Salon"], sprites.pnj_group], "Salon")
caporal = Caporal("Caporal", sprites.camera_group.carte.get_waypoint('SpawnCaporal'), [sprites.camera_groups["FirstRoom"], sprites.pnj_group], "FirstRoom")
# Type camera
sprites.camera_group.set_type_camera("center")

last_time = time.time()
while True:
    dt = time.time() - last_time
    last_time = time.time()

    if sprites.player.is_teleporting:
        sprites.player.is_teleporting = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
            sprites.save_data.save_player_position(player_position)
            sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
            sprites.save_data.save_player_life(sprites.player.get_HP())
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if parchemin_rect.collidepoint(pygame.mouse.get_pos()):
                menuTouches.run()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                menuTouches.run()

            if event.key == pygame.K_ESCAPE:
                player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
                sprites.save_data.save_player_position(player_position)
                sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
                sprites.save_data.save_player_life(sprites.player.get_HP())
                pygame.quit()
                sys.exit()

            for tp in sprites.camera_group.teleporters:
                if sprites.player.rect.colliderect(tp.rect):
                    sprites.aide_teleportation.open_dialog()
                    if event.key == pygame.K_e:
                        transition.run()
                        name_dest = tp.name_destination
                        sprites.camera_group = sprites.camera_groups[name_dest]
                        sprites.player.set_pos(sprites.camera_groups[name_dest].carte.get_waypoint(tp.name_tp_back))
                        sprites.player.is_teleporting = True
                        sprites.camera_group.messages.open_dialog()
                        sprites.aide_teleportation.close_dialog()
                else:
                    sprites.aide_teleportation.close_dialog()

            if event.key == pygame.K_SPACE:
                messages = sprites.camera_group.messages
                messages.execute()
                # if messages.letter_index == len(messages.texts[messages.text_index])-1:
                #     messages.next()
                #     messages.execute()
                # elif messages.reading:
                #    messages.letter_index = len(messages.texts[messages.text_index])
                
            if sprites.player.rect.colliderect(sprites.camera_group.interaction.rect):
                sprites.aide_terminal.open_dialog()
                if event.key == pygame.K_a:
                    if sprites.camera_group.interaction.name == "Terminal":
                        cmd.run()
                        if cmd.is_good:
                            sprites.camera_group = sprites.camera_groups["FirewallOuvert"]
                            sprites.camera_group.messages.open_dialog()
                            sprites.aide_terminal.close_dialog()
                            
                    elif sprites.camera_group.interaction.name == "BDD":
                        login_page.run()
                    
                    elif sprites.camera_group.interaction.name == "Parchemin":
                        menuFin.run()
            else:
                sprites.aide_terminal.close_dialog()

    if not sprites.camera_group.messages.reading:
        if pygame.sprite.spritecollide(sprites.player, sprites.pnj_group, False):
            sprites.camera_group.messages.open_dialog()
    
    # Background color depends of the map
    screen.fill('#000000')

    sprites.camera_group.update(dt)
    sprites.camera_group.custom_draw(sprites.player)

    #Render des messages
    sprites.camera_group.messages.render()
    for aide_message in sprites.liste_aides_message:
        aide_message.render()
        
    # Sauvegarde la position du joueur toutes les 5 secondes
    current_time = pygame.time.get_ticks()
    if current_time - last_save_time > 5000:
        player_position = {"x": sprites.player.pos.x, "y": sprites.player.pos.y}
        sprites.save_data.save_player_position(player_position)
        sprites.save_data.save_player_map(sprites.camera_group.carte.map_name)
        sprites.save_data.save_player_life(sprites.player.get_HP())
        last_save_time = current_time
    
    screen.blit(parchemin_surf, (0, 0))

    # DEBUG : Permettre de faire apparaitre tous les sprites
    # sprites.camera_group.debug()

    pygame.display.update()
    clock.tick(60)

