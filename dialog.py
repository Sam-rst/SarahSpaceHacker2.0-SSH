import pygame
from settings import *

class DialogBox:
    
    X_POSITION = 200
    Y_POSITION = screen.get_height() - 200
    
    def __init__(self, nom_perso, texts):
        self.nom_perso = nom_perso
        self.box = pygame.image.load('graphics/dialog/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (1200, 150))
        self.pnj = pygame.image.load(f'graphics/caracters/{self.nom_perso}/right/sprite_1.png')
        self.pnj = pygame.transform.scale(self.pnj, (100, 150))
        self.texts = texts
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('graphics/font/Cyberpunk2.ttf', 30)
        self.reading = False
        self.was_speak = False
        
    def open_dialog(self):
        self.reading = True
        self.text_index = 0
    
    def execute(self):
        self.next_text()
        
    def render(self):
        if self.reading:
            self.letter_index += 1
            
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            screen.blit(self.pnj, (self.X_POSITION-100, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text, (self.X_POSITION + 100, self.Y_POSITION + 20))
        
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        
        if self.text_index >= len(self.texts):
            self.reading = False

class Aide:
    
    X_POSITION = screen.get_width()//2 - 200
    Y_POSITION = screen.get_height()//2 -100
    
    def __init__(self, texts):
        self.texts = texts
        self.text_index = 0
        self.font = pygame.font.Font('graphics/font/Cyberpunk2.ttf', 20)
        self.reading = False
        self.was_speak = False
        
    def open_dialog(self):
        self.reading = True
        self.text_index = 0
    
    def close_dialog(self):
        self.reading = False
        self.text_index = 0
    
    def execute(self):
        self.next_text()
        
    def render(self):
        if self.reading:
            text = self.font.render(self.texts[self.text_index], False, (211, 211, 211), (255, 255, 255))
            screen.blit(text, (self.X_POSITION, self.Y_POSITION))
        
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        
        if self.text_index >= len(self.texts):
            self.reading = False
            
# class Aide:
    
#     X_POSITION = 200
#     Y_POSITION = screen.get_height() - 200
    
#     def __init__(self, text, button, player_pos) -> None:
#         self.font = pygame.font.Font('graphics/font/Cyberpunk2.ttf', 60)
#         self.text = text
#         self.text_surf = self.font.render(self.text, False, (255, 0, 255))
#         self.button = button
#         self.player_pos = player_pos
#         self.reading = False
    
#     def render(self):
#         if self.reading:
#             screen.blit(self.text_surf, (self.X_POSITION, self.Y_POSITION-200))
            
#         # screen.blit(self.button.ima)