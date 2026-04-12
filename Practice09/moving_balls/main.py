import pygame
from ball import Ball

# Настройки экрана
WIDTH, HEIGHT = 600, 400
BG_COLOR = (255, 255, 255)

def main():
    pygame.init()
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ball.move(0, -20, WIDTH, HEIGHT)
        if keys[pygame.K_DOWN]:
            ball.move(0, 20, WIDTH, HEIGHT)
        if keys[pygame.K_LEFT]:
            ball.move(-20, 0, WIDTH, HEIGHT)
        if keys[pygame.K_RIGHT]:
            ball.move(20, 0, WIDTH, HEIGHT)

        ball.draw(screen)
        pygame.display.flip()
        clock.tick(30)  # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
