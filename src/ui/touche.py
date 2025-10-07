import pygame
import src.core.sprites

class Touche(pygame.sprite.Sprite):
    type = "Touche"
    
    def __init__(self, nom_touche : str, group):
        super().__init__(group)
        self.name = nom_touche
        self.image = pygame.image.load(f"src/assets/touches/{nom_touche}.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.midbottom)
    
    def set_pos(self, new_pos):
        self.pos.x = new_pos[0]
        self.pos.y = new_pos[1]