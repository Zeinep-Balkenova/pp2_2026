import pygame
import random

class Player:
    def __init__(self):
        self._songs = [
            r'C:\\git_practice\\Practice9\\player\\music\\Tame Impala - Let It Happen.mp3',
            r'C:\\git_practice\\Practice9\\player\\music\\Tame Impala - The Less I Know The Better.mp3',
            r'C:\\git_practice\\Practice9\\player\\music\\Иван Дорн - Северное Сияние.mp3',
            r'C:\\git_practice\\Practice9\\player\\music\\Bad Bunny - BAILE INoLVIDABLE.mp3'
        ]
        self.shuffled_queue = list(self._songs)
        random.shuffle(self.shuffled_queue)
        
        self.current_track_index = 0
        self.current_song_name = 'No song playing'
        self.paused = False

    def play_current(self):
        song = self.shuffled_queue[self.current_track_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        some = song.replace(r'C:\\git_practice\\Practice9\\player\\music\\', '')
        self.current_song_name = some.replace('.mp3', '')

        self.paused = False

    def next_song(self):
        if self.current_track_index < len(self.shuffled_queue) - 1:
            self.current_track_index += 1
        else:
            self.current_track_index = 0
            random.shuffle(self.shuffled_queue)
        self.play_current()

    def prev_song(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
        else:
            self.current_track_index = len(self.shuffled_queue) - 1
        self.play_current()

    def pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True
