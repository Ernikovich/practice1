import pygame
import sys
import random
import time

pygame.init()

# Загрузка и воспроизведение бэкграунд музыки
pygame.mixer.music.load("sounds/background.wav")
pygame.mixer.music.set_volume(0.5) # громкость 50%.
pygame.mixer.music.play(-1) # бесконечное воспроизведение.

# Частота кадров
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Создание окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Фон игры
background = pygame.image.load("images/AnimatedStreet.png")

# Глобальные переменные
SPEED = 5  
SCORE = 0  
COINS = 0  

# Увеличение скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Звук столкновения
crash_sound = pygame.mixer.Sound('sounds/crash.wav')

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # инициализация базового Sprite
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1  
            self.rect.top = 0 # враг появляется снова в самом верху экрана.
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#  монета
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 2, 3])  # Монеты разного веса (1, 2 или 5 очков)
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

    def move(self):
        global COINS, SPEED
        COINS += self.value  # Прибавляем очки в зависимости от монеты
        if COINS % 3 == 0:  # Если количество монет кратно 3 → скорость врагов увеличивается на 2.5
            SPEED += 2.5  
        self.value = random.choice([1, 2, 3])  # Генерируем новую случайную монету
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

#  игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)

# сценарий столкновения
def handle_crash():
    pygame.mixer.Sound.play(crash_sound)
    time.sleep(0.5)  #делает паузу на полсекунды, чтобы звук успел прозвучать.

    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over, (30, 250))
    pygame.display.update()
    pygame.time.delay(2000)  #задержка
    pygame.quit()
    sys.exit()

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

background_y = 0  

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == INC_SPEED:
            SPEED += 0.1  

    # Проверяем столкновение игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        handle_crash()

    # Двигаем фон для эффекта движения
    background_y = (background_y + SPEED) % background.get_height()
    DISPLAYSURF.blit(background, (0, background_y))
    DISPLAYSURF.blit(background, (0, background_y - background.get_height()))
    # % background.get_height() — остаток от деления. Это нужно, чтобы когда фон полностью «прокрутился», он начинался заново (циклический эффект бесконечной дороги).
    # Если рисовать только один фон, то при его движении вниз появлялась бы пустая область сверху.

    # Отображаем очки и монеты
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (10, 30))

    # Двигаем игрока и врага
    P1.move()
    E1.move()

    # Отображаем все спрайты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверяем столкновение игрока с монетами
    if pygame.sprite.spritecollideany(P1, coins):
        C1.move()  

    pygame.display.update()
    FramePerSec.tick(FPS)