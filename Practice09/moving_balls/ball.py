import pygame

class Ball:
    def __init__(self, x, y, radius=25, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy, screen_width, screen_height):
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверка границ
        if (self.radius <= new_x <= screen_width - self.radius) and \
           (self.radius <= new_y <= screen_height - self.radius):
            self.x = new_x
            self.y = new_y

# dx, dy — смещение по осям X и Y (например, dx=5 сдвинет мяч вправо на 5 пикселей).

# Допустим:
# ширина окна (screen_width) = 800 пикселей
# радиус мяча (self.radius) = 25 пикселей

# Что проверяет условие:
# Левая граница:  
# self.radius <= new_x → центр мяча (new_x) не может быть меньше 25.
# Если центр будет, например, в точке 10, то часть мяча «вылезет» за левый край.

# Правая граница:  
# new_x <= screen_width - self.radius → центр мяча не может быть больше 800 - 25 = 775.
# Если центр будет, например, в точке 790, то часть мяча «вылезет» за правый край.