import pygame

class MusicPlayer:
    def __init__(self, playlist):
        pygame.mixer.init() #нициализация аудио‑модуля Pygame
        self.playlist = playlist
        self.index = 0 #текущий трек
        self.is_playing = False # флаг, играет ли музыка.
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

# self.index = (self.index + 1) % len(self.playlist)
# Увеличиваем индекс текущего трека на 1.
# % len(self.playlist) гарантирует, что если мы дошли до конца списка, то вернёмся к началу (циклический переход).
# Например:
# Было index = 0, станет 1
# Было index = 1, а длина плейлиста = 2 → (1+1) % 2 = 0, значит снова первый трек.

# pos = pygame.mixer.music.get_pos() // 1000
# Получаем текущую позицию трека в миллисекундах.
# Делим на 1000, чтобы перевести в секунды.
# Например, если прошло 12.345 мс → будет 12 секунд.

# if pos >= 0:
# Pygame возвращает -1, если трек не играет.
# Поэтому проверяем, что позиция корректная.

# return self.saved_pos + pos
# Возвращаем сумму:
# self.saved_pos — сколько секунд уже было накоплено до этого (например, после остановки).
# pos — сколько секунд прошло с момента последнего запуска.