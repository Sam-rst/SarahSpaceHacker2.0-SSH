from src.domain.caracter import *
from src.core.sprites import *

class Player(Caracter):
    type = 'Player'
    
    def __init__(self, name, pos, groups):
        super().__init__(name, pos, groups)
        self.transform_to_player()
    
    def transform_to_player(self):
        self.frames["Bottom Walk"] = sarah_bottom_walks
        self.frames["Left Walk"] = sarah_left_walks
        self.frames["Top Walk"] = sarah_top_walks
        self.frames["Right Walk"] = sarah_right_walks
        self.image = self.frames[self.animation_direction][self.animation_index]

    
    def is_alive(self):
        if self.HP == 0:
            self.kill()
            return False
        return True
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_q] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            if keys[pygame.K_z] or keys[pygame.K_UP]:
                self.direction.y = -1
                self.animation_direction = 'Top Walk'
                self.is_moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.animation_direction = 'Bottom Walk'
                self.is_moving = True
            else:
                self.direction.y = 0
                
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.animation_direction = 'Right Walk'
                self.is_moving = True
            elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.animation_direction = 'Left Walk'
                self.is_moving = True
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.is_moving = False
            self.animation_index = 0
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.feet.midbottom = self.rect.midbottom
        self.input()
        self.apply_collisions(dt)
        self.animation_state()
        self.transform_scale()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()