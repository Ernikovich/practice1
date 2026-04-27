import pygame
from ball import Ball

# Настройки экрана
WIDTH, HEIGHT = 600, 400
BG_COLOR = (255, 255, 255)

def main():
    pygame.init() # запускает все модули Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")

    clock = pygame.time.Clock()
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed() #возвращает список всех клавиш (True/False)
        if keys[pygame.K_UP]:
            ball.move(0, -20, WIDTH, HEIGHT)
        if keys[pygame.K_DOWN]:
            ball.move(0, 20, WIDTH, HEIGHT)
        if keys[pygame.K_LEFT]:
            ball.move(-20, 0, WIDTH, HEIGHT)
        if keys[pygame.K_RIGHT]:
            ball.move(20, 0, WIDTH, HEIGHT)

        ball.draw(screen) #рисуем мяч на экране.
        pygame.display.flip() #обновляем экран (показываем изменения).
        clock.tick(50)  # FPS

    pygame.quit()#Когда цикл завершён, закрываем Pygame и окно.

if __name__ == "__main__":
    main()
# нужна для того, чтобы твоя программа запускалась только тогда, когда файл запускается напрямую, а не когда он импортируется в другой модуль.
