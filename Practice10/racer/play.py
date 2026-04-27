import pygame 
import sys
import random,time
from pygame.locals import * # содержит константы клавиш (K_LEFT, K_RIGHT, QUIT и т.д.).

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED=5
SCORE=0
COINS_COLLECTED = 0   # новый счётчик монет

font=pygame.font.SysFont("Verdana", 60)
font_small=pygame.font.SysFont("Verdana", 20)
game_over=font.render("Game Over", True, BLACK)

background= pygame.image.load("images/AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #set_mode() один аргумент — размер окна в виде кортежа (ширина, высота).
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect() # Получаем прямоугольник вокруг картинки
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)# Случайная позиция сверху

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) # Двигаем вниз 
        # Это значит, что прямоугольник перемещается сам, без создания копии.
        if (self.rect.top > 600):# Если вышел за экран
            SCORE+=1
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)

    # def draw(self, surface):
    #     surface.blit(self.image, self.rect) # Отрисовка врага

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  #Начальная позиция внизу экрана 

    def move(self):
        pressed_keys = pygame.key.get_pressed()# Проверяем нажатые клавиши
        if self.rect.left > 0:  # Если не вышли за левую границу
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH: # Если не вышли за правую границу
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        # pygame.transform.scale() — это функция, которая изменяет размер изображения.
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, SPEED - 2)
        global COINS_COLLECTED
        if (self.rect.top > 600):# Если вышел за экран
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)
 
P1 = Player()
E1 = Enemy()
C1 = Coins()

enemies=pygame.sprite.Group() #это контейнер для спрайтов.
enemies.add(E1)#мы храним всех врагов 
coins=pygame.sprite.Group() # группа coins, чтобы хранить все монеты.
coins.add(C1)
all_sprites=pygame.sprite.Group() #все объекты игры (игрок и враг).
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED=pygame.USEREVENT+1 #создаём новый уникальный тип события. 
pygame.time.set_timer(INC_SPEED,1000)# каждые 1000 мс (1 секунда) будет генерироваться событие.
# pygame.time.set_timer(eventid, milliseconds, loops=0)


while True:
    for event in pygame.event.get():
        if event.type==INC_SPEED:
            SPEED+=0.5 #каждые 1 секунду скорость врагов увеличивается на 0.5.

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     # 1. Очистка экрана и фон
    DISPLAYSURF.blit(background,(0,0))
    scores=font_small.render(str(SCORE),True, BLACK)
    DISPLAYSURF.blit(scores,(10,10)) #В левом верхнем углу теперь отображается текущее количество очков.

    coins_text=font_small.render("Coins: "+ str(COINS_COLLECTED),True,BLACK)
    DISPLAYSURF.blit(coins_text,(50,10))
     # 2. Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image,entity.rect)
        entity.move() #заставляет объект выполнить своё движение.
    
    # 3. Проверка столкновений
    if pygame.sprite.spritecollideany(P1,enemies):
        pygame.mixer.Sound('sounds/crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED) #Экран закрашивается красным
        DISPLAYSURF.blit(game_over,(30,250)) #выводится надпись «Game Over».

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    if pygame.sprite.spritecollide(P1,coins,True):
        COINS_COLLECTED+=1
        new_coin=Coins() #Создаётся новая монета, чтобы игра продолжалась.
        coins.add(new_coin)
        all_sprites.add(new_coin)

    P1.update()# Обновляем игрока (движение)
    E1.move()# Двигаем врага

    # P1.draw(DISPLAYSURF)# Рисуем игрока
    # E1.draw(DISPLAYSURF)# Рисуем врага

    pygame.display.update()# Обновляем экран
    FramePerSec.tick(FPS)# Ограничиваем скорость до 60 FPS
