import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        
        self.music_folder = music_folder
        self.playlist = self.load_music()
        self.current_track = 0
        self.playing = False

    def load_music(self):
        files = []
        for file in os.listdir(self.music_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                files.append(os.path.join(self.music_folder, file))
        return files

    def play(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play()

    def previous(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.play()

    def get_current_track_name(self):
        if self.playlist:
            return os.path.basename(self.playlist[self.current_track])
        return "No track"

    def get_position(self):
        return pygame.mixer.music.get_pos() // 1000