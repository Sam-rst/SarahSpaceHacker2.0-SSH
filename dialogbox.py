import pygame

class Dialogbox:

    def __init__(self):
        self.box = pygame.image.load('chemin vers l image')

    def render(self, screen):
        screen.blit(self.box, ())