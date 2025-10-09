import os
from src.core.settings import *
from src.domain.images import *
from src.core import sprites


class Caracter(pygame.sprite.Sprite):
    type = "Caracter"

    def __init__(self, name, pos, groups):
        super().__init__(groups)
        self.save_data = sprites.save_data
        # Aspects of the caracter
        self.name = name
        self.max_HP = 1
        self.HP = self.max_HP
        self.attack_value = 1
        self.defense_value = 1
        self.range = 10 * scale
        self.cooldown_attack = 200
        self.last_shot = 0

        # Image and animations
        self.frames = {
            "Bottom Walk": caracter_bottom_walks,
            "Left Walk": caracter_left_walks,
            "Top Walk": caracter_top_walks,
            "Right Walk": caracter_right_walks
        }
        self.animation_index = 0
        self.animation_direction = "Bottom Walk"
        self.image = self.frames[self.animation_direction][self.animation_index]
        # 🔧 FIX : Utiliser une taille cohérente
        self.image = pygame.transform.scale(self.image, (64 * (scale-1), 64 * (scale-1)))
        self.animation_speed = 0.1
        self.is_moving = False
        self.is_attack = False

        # Rectangle
        self.rect = self.image.get_rect(midbottom=pos)
        self.old_rect = self.rect.copy()

        # 🔧 FIX : Pieds positionnés correctement dès le départ
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.25)
        self.feet.midbottom = self.rect.midbottom
        self.old_feet = self.feet.copy()

        # Screen
        self.screen = pygame.display.get_surface()

        # Moving
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.cooldown_move = 1500
        self.last_move = 0

        self.is_teleporting = False
        self.is_animating = False

    # ... (tous vos getters/setters restent identiques)

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def set_max_HP(self, new_value):
        self.max_HP = new_value

    def get_max_HP(self):
        return self.max_HP

    def set_HP(self, new_value):
        self.HP = new_value

    def get_HP(self):
        return self.HP

    def set_range(self, new_value):
        self.range = new_value

    def get_range(self):
        return self.range

    def set_animation_direction(self, new_value):
        self.animation_direction = new_value

    def set_cooldown_attack(self, new_value):
        self.cooldown_attack = new_value

    def get_cooldown_attack(self):
        return self.cooldown_attack

    def set_attack_value(self, new_value):
        self.attack_value = new_value

    def get_attack_value(self):
        return self.attack_value

    def set_defense_value(self, new_value):
        self.defense_value = new_value

    def get_defense_value(self):
        return self.defense_value

    def get_type(self):
        return type(self).type

    def set_pos(self, new_pos):
        self.pos.x = new_pos[0]
        self.pos.y = new_pos[1]

    def get_pos(self):
        return self.pos

    def set_speed(self, new_value):
        self.speed = new_value

    def get_speed(self):
        return self.speed

    def set_cooldown_move(self, new_value):
        self.cooldown_move = new_value

    def get_ticks(self):
        return pygame.time.get_ticks()

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def transform_scale(self):
        # 🔧 FIX : Retourner l'image redimensionnée !
        return pygame.transform.scale(self.image, (64 * (scale-1), 64 * (scale-1)))

    def __str__(self):
        return f"Le {self.get_type()} {self.get_name()} possède : vie = {self.get_HP()}/{self.get_max_HP()}, attaque = {self.get_attack_value()}, defense = {self.get_defense_value()}, cooldown = {self.get_cooldown_attack()}, attack range = {self.get_range()}, position = {self.get_pos()}"

    def regenerate(self):
        self.HP = self.max_HP

    def level_up(self):
        self.set_attack_value(self.attack_value + 5)
        self.set_defense_value(self.defense_value + 2)
        self.set_max_HP(self.max_HP + 5)
        self.regenerate()

    def decrease_health(self, amount):
        self.set_HP(self.get_HP() - amount)
        if self.get_HP() < 0:
            self.set_HP(0)

    def load_character_animations(self, base_path, character_name, action_name):
        directions = ["bottom", "left", "top", "right"]
        frames = {}

        for direction in directions:
            direction_path = os.path.join(base_path, character_name, "actions", action_name, direction)

            if not os.path.exists(direction_path):
                print(f"⚠️ Dossier manquant : {direction_path}")
                continue

            images = sorted(
                [f for f in os.listdir(direction_path) if f.endswith(".png")],
                key=lambda f: int(''.join(filter(str.isdigit, f)) or 0)
            )

            frame_list = [
                pygame.image.load(os.path.join(direction_path, img)).convert_alpha()
                for img in images
            ]

            frames[f"{direction.capitalize()} {action_name.capitalize()}"] = frame_list
            print(f"✅ {character_name}_{direction}_{action_name} : {len(frame_list)} frames chargées")

        return frames

    def collision(self, direction):
        if self.is_teleporting:
            return

        # 🔧 FIX : Vérifier les collisions avec les pieds, pas le rect
        for sprite in sprites.camera_group.collision_group:
            if self.feet.colliderect(sprite.rect):
                if direction == 'horizontal':
                    # Collision on the right
                    if self.feet.right >= sprite.rect.left and self.old_feet.right <= sprite.old_rect.left:
                        self.feet.right = sprite.rect.left
                        self.rect.midbottom = self.feet.midbottom
                        self.pos.x = self.rect.centerx
                        self.pos.y = self.rect.bottom

                    # Collision on the left
                    if self.feet.left <= sprite.rect.right and self.old_feet.left >= sprite.old_rect.right:
                        self.feet.left = sprite.rect.right
                        self.rect.midbottom = self.feet.midbottom
                        self.pos.x = self.rect.centerx
                        self.pos.y = self.rect.bottom

                if direction == 'vertical':
                    # Collisions on the top
                    if self.feet.top <= sprite.rect.bottom and self.old_feet.top >= sprite.old_rect.bottom:
                        self.feet.top = sprite.rect.bottom
                        self.rect.midbottom = self.feet.midbottom
                        self.pos.x = self.rect.centerx
                        self.pos.y = self.rect.bottom

                    # Collisions on the bottom
                    if self.feet.bottom >= sprite.rect.top and self.old_feet.bottom <= sprite.old_rect.top:
                        self.feet.bottom = sprite.rect.top
                        self.rect.midbottom = self.feet.midbottom
                        self.pos.x = self.rect.centerx
                        self.pos.y = self.rect.bottom

    def map_collision(self, direction):
        map_width = sprites.camera_group.carte.get_size_map_width()
        map_height = sprites.camera_group.carte.get_size_map_height()
        tile_height = sprites.camera_group.carte.get_tileheight()

        if direction == 'horizontal':
            # 🔧 FIX : Vérifier avec les pieds
            if self.feet.left < 0:
                self.feet.left = 0
                self.rect.midbottom = self.feet.midbottom
                self.pos.x = self.rect.centerx
                self.pos.y = self.rect.bottom

            if self.feet.right > map_width:
                self.feet.right = map_width
                self.rect.midbottom = self.feet.midbottom
                self.pos.x = self.rect.centerx
                self.pos.y = self.rect.bottom

        if direction == 'vertical':
            # 🔧 FIX : Vérifier avec les pieds
            if self.feet.top < 0:
                self.feet.top = 0
                self.rect.midbottom = self.feet.midbottom
                self.pos.x = self.rect.centerx
                self.pos.y = self.rect.bottom

            if self.feet.bottom > map_height - tile_height:
                self.feet.bottom = map_height - tile_height
                self.rect.midbottom = self.feet.midbottom
                self.pos.x = self.rect.centerx
                self.pos.y = self.rect.bottom

    def apply_collisions(self, dt):
        # 🔧 FIX : Sauvegarder les anciennes positions AVANT le déplacement
        self.old_rect = self.rect.copy()
        self.old_feet = self.feet.copy()

        # Déplacement horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.bottom = round(self.pos.y)
        self.feet.midbottom = self.rect.midbottom
        self.collision('horizontal')
        # self.map_collision('horizontal')

        # Déplacement vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.bottom = round(self.pos.y)
        self.feet.midbottom = self.rect.midbottom
        self.collision('vertical')
        # self.map_collision('vertical')

    def animation_state(self):
        if self.is_attack:
            if not self.is_animating:
                self.is_animating = True
                self.animation_index = 0

            if self.animation_index < len(self.frames[self.animation_direction]):
                self.image = self.frames[self.animation_direction][int(self.animation_index)]
                self.image = self.transform_scale()  # 🔧 Maintenant ça retourne bien l'image
                self.animation_index += self.animation_speed
            else:
                self.animation_index = 0
                self.is_attack = False
                self.is_animating = False

        elif self.is_moving:
            if not self.is_animating:
                self.is_animating = True
                self.animation_index = 0

            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.frames[self.animation_direction]):
                self.animation_index = 0

            self.image = self.frames[self.animation_direction][int(self.animation_index)]
            self.image = self.transform_scale()

        else:
            self.is_animating = False
            self.animation_index = 0

    def update(self):
        # Les pieds sont déjà mis à jour dans apply_collisions
        pass

    def debug(self):
        pygame.draw.rect(self.screen, '#ff0000', self.rect, 5)
        pygame.draw.rect(self.screen, '#00ff00', self.feet, 3)
        pygame.draw.circle(self.screen, '#fd5a61', self.rect.midbottom, 5)