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
