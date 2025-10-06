import pygame
import os
import random

class MusicPlayer:
    def __init__(self, volume=0.5):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.mixer.music.set_volume(volume)
        self.playlist = []
        self.current_track_index = 0
        self.shuffle_playlist()
        self.load_current_track()
        self.play_current_track()

    def shuffle_playlist(self):
        self.playlist = [
            "graphics/songs/dbz.mp3",
            "graphics/songs/pokemon.mp3"
            ]
        random.shuffle(self.playlist)

    def load_current_track(self):
        pygame.mixer.music.load(self.playlist[self.current_track_index])

    def play_current_track(self):
        pygame.mixer.music.play()

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.load_current_track()
        pygame.mixer.music.play()  # Commencez à jouer la piste suivante

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_track()
        return True

    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
