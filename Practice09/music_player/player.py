import pygame

class MusicPlayer:
    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.index = 0
        self.is_playing = False
        self.saved_pos = 0  # сохраняем позицию при стопе

    def play(self):
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play(start=self.saved_pos)  # продолжаем с сохранённой позиции
        self.is_playing = True

    def stop(self):
        pos = pygame.mixer.music.get_pos() // 1000
        if pos >= 0:
            self.saved_pos += pos  # сохраняем позицию
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.saved_pos = 0  # сбрасываем позицию для нового трека
        self.play()

    def prev_track(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.saved_pos = 0  # сбрасываем позицию для нового трека
        self.play()

    def get_current_track(self):
        return self.playlist[self.index]

    def get_position(self):
        if self.is_playing:
            pos = pygame.mixer.music.get_pos() // 1000
            if pos >= 0:
                return self.saved_pos + pos
        return self.saved_pos
