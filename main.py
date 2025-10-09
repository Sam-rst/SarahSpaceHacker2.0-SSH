import sys, time

from src.core import sprites
from src.domain.game_timer import GameTimer
from src.ui.menus.menu_debut import MenuDebut
from src.ui.menus.menu_fin import MenuFin
from src.ui.menus.menu_game_over import MenuGameOver
from src.domain.pnj import *
from src.ui.menus.menu_mysql import LoginPage
from src.ui.menus.menu_terminal import Terminal
from src.ui.menus.menu_touches import MenuTouches
from src.ui.menus.menu_transition import Transition

pygame.init()

parchemin_surf = pygame.image.load("src/assets/touches/parchemin.png")
parchemin_surf = pygame.transform.scale(parchemin_surf, (200, 256))
parchemin_rect = parchemin_surf.get_rect(topright=(screen.get_width(), 0))

# Menus
login_page = LoginPage()
cmd = Terminal()
menuDebut = MenuDebut()
menuFin = MenuFin()
transition = Transition()
menuTouches = MenuTouches()

# Saves
sprites.player = menuDebut.run()
last_save_time = pygame.time.get_ticks()

# Dialogues
# emma = Emma("Emma", sprites.camera_group.carte.get_waypoint('SpawnEmmaSalon'), [sprites.camera_groups["Salon"], sprites.pnj_group], "Salon")
# caporal = Caporal("Caporal", sprites.camera_group.carte.get_waypoint('SpawnCaporal'), [sprites.camera_groups["FirstRoom"], sprites.pnj_group], "FirstRoom")
# Type camera
sprites.camera_group.set_type_camera("center")

# Game timer
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_timer = GameTimer(total_seconds=1*10, font=font)

# Game Over
game_over_menu = MenuGameOver(screen, font)


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
                        sprites.camera_group.messages.open_dialog() if sprites.camera_group.messages else None
                        sprites.aide_teleportation.close_dialog()
                else:
                    sprites.aide_teleportation.close_dialog()

            if event.key == pygame.K_SPACE:
                pass
                # messages = sprites.camera_group.messages
                # messages.execute()
                # if messages.letter_index == len(messages.texts[messages.text_index])-1:
                #     messages.next()
                #     messages.execute()
                # elif messages.reading:
                #    messages.letter_index = len(messages.texts[messages.text_index])
                
            # if sprites.player.rect.colliderect(sprites.camera_group.interaction.rect):
            #     sprites.aide_terminal.open_dialog()
            #     if event.key == pygame.K_a:
            #         if sprites.camera_group.interaction.name == "Terminal":
            #             cmd.run()
            #             if cmd.is_good:
            #                 sprites.camera_group = sprites.camera_groups["FirewallOuvert"]
            #                 sprites.camera_group.messages.open_dialog()
            #                 sprites.aide_terminal.close_dialog()
            #
            #         elif sprites.camera_group.interaction.name == "BDD":
            #             login_page.run()
            #
            #         elif sprites.camera_group.interaction.name == "Parchemin":
            #             menuFin.run()
            # else:
            #     sprites.aide_terminal.close_dialog()

    if sprites.camera_group.messages:
        if not sprites.camera_group.messages.reading:
            if pygame.sprite.spritecollide(sprites.player, sprites.pnj_group, False):
                sprites.camera_group.messages.open_dialog()
    
    # Background color depends of the map
    screen.fill('#000000')

    sprites.camera_group.update(dt)
    sprites.camera_group.custom_draw(sprites.player)

    #Render des messages
    sprites.camera_group.messages.render() if sprites.camera_group.messages else None
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
    
    screen.blit(parchemin_surf, (screen.get_width()-250, 0))

    # Mise à jour du timer
    game_timer.update()
    game_timer.draw(screen)

    if game_timer.is_game_over():
        game_over_menu.start()

    # Mise à jour et dessin du menu
    game_over_menu.update()
    game_over_menu.draw()

    # DEBUG : Permettre de faire apparaitre tous les sprites
    sprites.camera_group.debug()

    pygame.display.update()
    clock.tick(60)

