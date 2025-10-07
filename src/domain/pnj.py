from src.domain.caracter import *


class Pnj(Caracter):
    type = 'Pnj'
    
    def __init__(self, name, pos, groups):
        super().__init__(name, pos, groups)
        self.transform_to_pnj()
        self.talked_to = False  # Booléen initialisé à False

    def talk_to(self):
        self.talked_to = True


    def transform_to_pnj(self):
        self.frames["Bottom Walk"] = caracter_bottom_walks
        self.frames["Left Walk"] = caracter_left_walks
        self.frames["Top Walk"] = caracter_top_walks
        self.frames["Right Walk"] = caracter_right_walks
        self.image = self.frames[self.animation_direction][self.animation_index]
        self.rect = self.image.get_rect(center = self.get_pos())
        self.set_speed(100)
        self.animation_speed = 0.2

    def change_direction(self):
        if randint(0,1):
            self.direction.x = randint(-1, 1)
            self.direction.y = randint(-1, 1)
            self.is_moving = True
        else:
            self.is_moving = False
            self.direction.x = 0
            self.direction.y = 0
        
        if self.direction.x == -1:
            self.animation_direction = 'Left Walk'
        elif self.direction.x == 1:
            self.animation_direction = 'Right Walk'
        
        if self.direction.y == -1:
            self.animation_direction = 'Top Walk'
        elif self.direction.y == 1:
            self.animation_direction = 'Bottom Walk'
    
    def is_alive(self):
        if self.get_HP() <= 0:
            self.kill()
            self.save_data.save_mob_dead(self.name)
            # self.piecemob = Item('Piece', self.get_pos(), [sprites.camera_group, sprites.items_sprites, sprites.items_drop])
            self.items.append(self.piecemob)
            
    def random_spawn(self):
        width, height = sprites.camera_group.carte.get_size_map()
        self.set_pos((randint(500, width-500), randint(500, height-500)))


    def display_life(self, screen, offset):
        life_ratio = self.get_HP() / self.get_max_HP()
        x = self.pos.x - 10 - offset.x
        y = self.pos.y - 10 - offset.y
        pygame.draw.rect(screen, '#ff0000', pygame.rect.Rect(x, y, 100, 10), 5)
        pygame.draw.rect(screen, '#00ff00', pygame.rect.Rect(x, y, 100 * life_ratio, 10), 5)
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        # Collisions and moving setup
        self.apply_collisions(dt)
        if (self.get_ticks() - self.last_move) > self.cooldown_move:
            self.change_direction()
            self.last_move = self.get_ticks()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.animation_state()
        self.rect = self.image.get_rect(topleft = self.get_pos())

class Emma(Pnj):
    type = 'Sarah'

    def __init__(self, name, pos, groups, map_name):
        super().__init__(name, pos, groups)
        self.transform_to_Emma()
        self.map_name = map_name

    def transform_to_Emma(self):
        """Transformer le pnj en Sarah"""
        self.frames['Bottom Walk'] = emma_bottom_walks
        self.frames['Left Walk'] = emma_left_walks
        self.frames['Top Walk'] = emma_top_walks
        self.frames['Right Walk'] = emma_right_walks
        self.image = self.frames[self.animation_direction][self.animation_index]
        self.set_range(0)
        self.set_max_HP(10000)
        self.set_HP(self.get_max_HP())
        self.set_attack_value(0)
        self.set_defense_value(100000)
        self.set_cooldown_attack(8000000)
        self.set_speed(0)
        # self.set_pos(sprites.camera_group.carte.get_waypoint('SpawnEmma'))
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        # Collisions and moving setup
        self.apply_collisions(dt)
        self.animation_state()
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.transform_scale()

class Caporal(Pnj):
    type = 'Sarah'

    def __init__(self, name, pos, groups, map_name):
        super().__init__(name, pos, groups)
        self.transform_to_Caporal()
        self.map_name = map_name

    def transform_to_Caporal(self):
        """Transformer le pnj en Caporal"""
        self.frames['Bottom Walk'] = caporal_bottom_walks
        self.frames['Left Walk'] = caporal_left_walks
        self.frames['Top Walk'] = caporal_top_walks
        self.frames['Right Walk'] = caporal_right_walks
        self.image = self.frames[self.animation_direction][self.animation_index]
        self.set_range(0)
        self.set_max_HP(10000)
        self.set_HP(self.get_max_HP())
        self.set_attack_value(0)
        self.set_defense_value(100000)
        self.set_cooldown_attack(8000000)
        self.set_speed(0)
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        # Collisions and moving setup
        self.apply_collisions(dt)
        self.animation_state()
        self.rect = self.image.get_rect(topleft = self.get_pos())
        self.transform_scale()