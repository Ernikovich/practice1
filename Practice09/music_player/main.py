import pygame
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Плейлист
playlist = ["music/gameshakers.mp3", "music/gravity_falls.mp3"]
player = MusicPlayer(playlist)

# Заливка цветом
screen.fill((200, 220, 255))  # нежно-голубой фон

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                player.play()
            elif event.key == pygame.K_s:  # Stop
                player.stop()
            elif event.key == pygame.K_n:  # Next
                player.next_track()
            elif event.key == pygame.K_b:  # Previous
                player.prev_track()
            elif event.key == pygame.K_q:  # Quit
                running = False

    # UI
    screen.fill((255, 255, 255))
    track_text = font.render(f"Track: {player.get_current_track()}", True, (0, 0, 0))
    pos_text = font.render(f"Position: {player.get_position()}s", True, (0, 0, 0))

    screen.blit(track_text, (20, 40))
    screen.blit(pos_text, (20, 80))

    # Прогресс‑бар
    progress = player.get_position() % 60  # пока просто 60 секунд для примера
    bar_width = int((progress / 60) * 500)  # ширина полоски
    pygame.draw.rect(screen, (0, 0, 255), (20, 120, bar_width, 20))  # синяя полоска
    pygame.draw.rect(screen, (0, 0, 0), (20, 120, 500, 20), 2)       # рамка

    pygame.display.flip()
    clock.tick(30)

pygame.quit()




