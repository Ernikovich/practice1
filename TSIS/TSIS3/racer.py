import pygame
import random
import os #  для работы с файлами и путям

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

LANE_CENTERS = [70, 160, 250, 330]   # X-координаты центров полос дороги

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets") # находит ПОЛНЫЙ путь к папке assets рядом с твоим файлом
# os.path.abspath(__file__)  это путь к текущему файлу   C:/Users/Asus/Desktop/TSIS3/racer.py
#   os.path.dirname(...) убирает имя файла и оставляет только папку
# os.path.join() нужен чтобы: правильно соединять пути не думать про / или \ добавляет папку assets


def asset(path): # делает удобный путь к файлу
    return os.path.join(ASSETS_DIR, path) # склеивает: папку assets и путь к файлу внутри неё

def _load_image(path, size=None):
    img = pygame.image.load(asset(path)).convert_alpha()
    # asset(path) → делает полный путь получаем полный путь к файлу
    # потом pygame.image.load(...) → открывает файл
    # convert_alpha() PNG с прозрачностью
    if size: # если размер задан — меняем его
        img = pygame.transform.scale(img, size)
    return img

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  100, 220),
    "green":  (50,  200, 80),
    "yellow": (240, 200, 30),
}

def tint_surface(surf, color): #перекрасить картинку
    tinted = surf.copy() # елаем копию картинки, чтобы не портить оригинал
    overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA) # создаёт новую пустую картинку (слой),  pygame.SRCALPHA у этой картинки будет прозрачность
    overlay.fill((*color, 90)) # сделай цветной слой, но слегка прозрачный
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD) # на накладывает цветной слой (overlay) на картинку (tinted),    BLEND_RGBA_ADD это режим смешивания цветов “сложи цвета overlay и оригинала”
    return tinted

# Background 
class Background:
    def __init__(self):
        self.image = _load_image("images/AnimatedStreet.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # растягиваем её на весь экран
        self.y = 0 # потому что фон сначала стоит в самом начале экрана

    def update(self, speed):
        self.y = (self.y + speed) % SCREEN_HEIGHT # фон “едет вниз”

    def draw(self, surf):
        surf.blit(self.image, (0, self.y)) # рисуем первую копию фона
        surf.blit(self.image, (0, self.y - SCREEN_HEIGHT)) # рисуем вторую копию сверху

# Player 
class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="red"):
        super().__init__()
        base = _load_image("images/Player.png", size=(40, 68))
        if car_color == "red":
            self.image = base # просто используем обычную картинку без изменений
        else:
            color = CAR_COLORS.get(car_color, CAR_COLORS["red"]) 
            self.image = tint_surface(base, color)
        self.rect  = self.image.get_rect(center=(LANE_CENTERS[1], 500)) # ставим машину на дорогу и фиксируем её позицию X = вторая полоса дороги Y = 500 (почти внизу экрана)

        self.shield_active = False
        self.nitro_active = False #ускорение
        self.nitro_mult= 1.0  #насколько ускорение сильное

        # щит вокруг машины (прозрачное голубое свечение)
        self._shield_surf = pygame.Surface((60, 88), pygame.SRCALPHA)  # создаём прямоугольник 60×88 прозрачный
        pygame.draw.ellipse(self._shield_surf, (80, 180, 255, 110), (0, 0, 60, 88)) # внешний овал голубой
        pygame.draw.ellipse(self._shield_surf, (140, 210, 255, 60),  (6, 6, 48, 76)) # внутренний овал

    def move(self, speed_multiplier=1.0):
        pressed = pygame.key.get_pressed() # какие клавиши сейчас нажаты?
        spd = max(1, int(6 * speed_multiplier * self.nitro_mult)) #speed_multiplier → сложность игры nitro_mult → ускорение
        if self.rect.left > 30 and pressed[pygame.K_LEFT]:
            self.rect.x -= spd
        if self.rect.right < SCREEN_WIDTH - 30 and pressed[pygame.K_RIGHT]: 
            self.rect.x += spd
        if self.rect.top > 0 and pressed[pygame.K_UP]:
            self.rect.y -= spd
        if self.rect.bottom < SCREEN_HEIGHT and pressed[pygame.K_DOWN]:
            self.rect.y += spd

    def draw(self, surface):
        if self.shield_active: #рисуем щит поверх машины
            surface.blit(self._shield_surf,
                         (self.rect.centerx - 30, self.rect.centery - 44))
        surface.blit(self.image, self.rect) # нарисуй саму машину в её позиции

# Enemy car 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = _load_image("images/Enemy.png", size=(40, 68))
        self.rect  = self.image.get_rect() # создаём коробку врага
        self.rect.centerx = random.choice(LANE_CENTERS) # враг появляется в случайной полосе
        self.rect.bottom   = -10 # враг появляется выше экрана
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill() #враг уехал за экран удаляем его

# Coin 
COIN_COLORS = {1: (255, 215, 0), 2: (192, 192, 192), 3: (184, 115, 51)}

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.value = random.choices([1, 2, 3], weights=[60, 30, 10])[0] # weights=[60, 30, 10] 1 → 60% (часто) 2 → 30% 3 → 10% (редко)
        base = _load_image("images/coin.png", size=(36, 36))
        self.image = tint_surface(base, COIN_COLORS[self.value]) #красим монету в цвет по стоимости
        f = pygame.font.SysFont("Arial", 12, bold=True)
        txt = f.render(str(self.value), True, (255, 255, 255)) # превращаем число в картинку текста
        self.image.blit(txt, txt.get_rect(center=(18, 18))) # накладываем цифру на монету
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = -10
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# Road Obstacle
class Obstacle(pygame.sprite.Sprite):
    TYPES = ["oil", "pothole", "bump"] # масло яма барьер

    def __init__(self, speed=5):
        super().__init__()
        self.kind = random.choice(self.TYPES)
        self.image = pygame.Surface((48, 30), pygame.SRCALPHA)

        if self.kind == "oil":
            pygame.draw.ellipse(self.image, (20, 20, 50, 210),  (2,  4, 44, 22)) # рисуется большая тёмная “лужа”
            pygame.draw.ellipse(self.image, (80, 50, 160, 130), (10, 8, 28, 14)) #добавляет светлое пятно сверху
            for i, c in enumerate([(255,0,100,60),(0,200,255,60),(100,255,0,60)]): #эффект масла
                pygame.draw.ellipse(self.image, c, (10 + i*6, 9, 10, 6))
        elif self.kind == "pothole":
            pygame.draw.ellipse(self.image, (40, 30, 20, 230), (4,  5, 40, 20)) # основная яма асфальт с дыркой
            pygame.draw.ellipse(self.image, (20, 15,  5, 200), (10, 9, 28, 12)) #внутренняя часть ямы глубина, туда проваливается колесо
        else:
            pygame.draw.rect(self.image, (120, 90, 20), (0, 9, 48, 12), border_radius=4) #тёмно-коричневый тонкий прямоугольник поперёк дороги углы закруглённым
            for i in range(3): # делаем 3 секции барьера
                pygame.draw.rect(self.image, (220, 50, 50), (i * 15 + 2, 9, 9, 12)) # красные блоки
                pygame.draw.rect(self.image, (240,240, 50), (i * 15 + 11, 9, 4, 12)) #жёлтые узкие полоски
                # (i * 15 + 2, 9, 9, 12) — это позиция маленького прямоугольника, который сдвигается вправо для создания ряда полос на барьере

        self.rect = self.image.get_rect() # прямоугольник объекта
        self.rect.centerx = random.choice(LANE_CENTERS) #объект появляется в случайной полосе дороги
        self.rect.bottom   = -10
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# Nitro strip  падающий бонус на дороге
class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = pygame.Surface((80, 18), pygame.SRCALPHA)
        for i in range(8): # создаём 8 сегментов
            c = 255 if i % 2 == 0 else 80  # эффект “энергии / движения” чередуем цвета
            pygame.draw.rect(self.image, (c, 220, c, 210), (i * 10, 0, 10, 18)) #рисуем полоски
        f = pygame.font.SysFont("Arial", 9, bold=True)
        lbl = f.render("NITRO", True, (0, 0, 0)) # надпись NITRO
        self.image.blit(lbl, lbl.get_rect(center=(40, 9))) #пишем его по центру
        self.rect = self.image.get_rect() # создаём хитбокс
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = -10
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# Power-Up 
PU_ICONS  = {"nitro": (255, 200, 0), "shield": (80, 160, 255), "repair": (80, 220, 80)}
PU_LABELS = {"nitro": "N","shield": "S", "repair": "R"}
PU_NAMES  = {"nitro": "NITRO","shield": "SHIELD","repair": "REPAIR"}

class PowerUp(pygame.sprite.Sprite):  #универсальный контейнер для разных бонусов
    LIFETIME = 8000 #время жизни объекта в миллисекундах

    def __init__(self, kind, speed=5):
        super().__init__() # инициализировать базовый Sprite
        self.kind = kind # тип бонуса
        self.spawned_at = pygame.time.get_ticks() # сохраняем момент создания
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA) # квадрат 40×40 с прозрачностью
        color = PU_ICONS[kind]
        pygame.draw.rect(self.image, color, (0, 0, 40, 40), border_radius=10) # рисуется закруглённый квадрат
        pygame.draw.rect(self.image, (255, 255, 255, 180),(0, 0, 40, 40), 2, border_radius=10) # добавляет белую рамку вокруг кнопки
        f_big = pygame.font.SysFont("Arial", 20, bold=True)
        f_sml = pygame.font.SysFont("Arial",  8, bold=True)
        lbl = f_big.render(PU_LABELS[kind], True, (255, 255, 255))
        self.image.blit(lbl, lbl.get_rect(center=(20, 18)))
        sml = f_sml.render(PU_NAMES[kind],  True, (0, 0, 0))
        self.image.blit(sml, sml.get_rect(center=(20, 33)))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = -10
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()
        if pygame.time.get_ticks() - self.spawned_at > self.LIFETIME: # удаление по времени 
            self.kill()
            # текущее время игры -когда появился