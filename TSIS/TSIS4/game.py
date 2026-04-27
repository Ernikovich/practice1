import pygame, random, time
from config import *

def random_cell(exclude=None): #генерирует случайную клетку на поле
    exclude = exclude or set() #если ничего не передали делаем пустой список запретов
    while True:
        pos = (random.randint(0, WIDTH//CELL_SIZE-1)*CELL_SIZE,
               random.randint(0, HEIGHT//CELL_SIZE-1)*CELL_SIZE)
        if pos not in exclude: #если позиция НЕ занята
            return pos

class Food:
    TYPES = {
        'normal': (RED,     CELL_SIZE,    1),
        'big':    (ORANGE,  CELL_SIZE+10, 3),
        'tiny':   (YELLOW,  CELL_SIZE-8,  2),
        'poison': (DARK_RED,CELL_SIZE,    0),
    }
    def __init__(self, forbidden):
        self.forbidden = forbidden #сохраняет запрещённые клетки
        self.spawn() # вызывает spawn()

    def spawn(self):
        self.kind = random.choices(list(self.TYPES), weights=[0.5,0.2,0.2,0.1])[0] # выбирает тип еды случайно:
        self.color, self.size
        self.points = self.TYPES[self.kind]
        self.pos = random_cell(self.forbidden) #выбираем случайную свободную клетку
        self.spawn_time = time.time() # запоминаем время появления

    def is_expired(self): #прошло ли слишком много времени
        return time.time() - self.spawn_time > FOOD_LIFETIME

    def get_rect(self): #центрирует еду внутри клетки
        o = (CELL_SIZE - self.size) // 2
        return pygame.Rect(self.pos[0]+o, self.pos[1]+o, self.size, self.size) # создаёт прямоугольник для коллизий

    def draw(self, surface): 
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=4)
        if self.kind == 'poison':
            pygame.draw.rect(surface, (200,0,50), r, 2, border_radius=4) #добавляет красную рамку


class PowerUp:
    TYPES  = {'speed': CYAN, 'slow': BLUE, 'shield': PURPLE}
    LABELS = {'speed': 'SPD', 'slow': 'SLO', 'shield': 'SHD'}

    def __init__(self, forbidden):
        self.kind = random.choice(list(self.TYPES))
        self.color = self.TYPES[self.kind] # берёт цвет этого бонуса
        self.pos = random_cell(forbidden) # ставит в свободную клетку
        self.spawn_ticks = pygame.time.get_ticks()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_ticks > POWERUP_LIFETIME

    def get_rect(self):
        return pygame.Rect(*self.pos, CELL_SIZE, CELL_SIZE) #делает квадрат для коллизий

    def draw(self, surface, font):
        r = self.get_rect()
        pygame.draw.rect(surface, self.color, r, border_radius=5)  #рисует сам бонус
        pygame.draw.rect(surface, WHITE, r, 1, border_radius=5) #белая рамка
        surface.blit(font.render(self.LABELS[self.kind], True, BLACK), (r.x+1, r.y+3)) #пишет текст внутри


class Game:
    def __init__(self, screen, settings, player_id, personal_best):
        self.screen, self.settings = screen, settings
        self.best = personal_best
        self.font   = pygame.font.SysFont("Verdana", 18)
        self.font_sm = pygame.font.SysFont("Verdana", 14)
        self.clock  = pygame.time.Clock()
        self.reset()

    def reset(self):# перезапуск игры
        self.snake = [(200,200),(180,200),(160,200)] # 3 сегмента змейки
        self.direction = self.next_dir = (CELL_SIZE, 0) # стартовое движение вправо
        self.score = 0
        self.level = 1
        self.speed = BASE_SPEED
        self.last_lvl_score = 0 #чтобы понимать когда повышать уровень
        self.obstacles = set() # набор блоков
        self.shield_active = False
        self.powerup = None
        self.powerup_timer = pygame.time.get_ticks() #последний раз появился powerup
        self.active_effect = None #активный эффект
        self.effect_end = 0 #когда он закончится
        self._spawn_food() # создаёт первую еду
 
    def _forbidden(self): # запрещённые клетки
        occ = set(self.snake) | self.obstacles # все занятые клетки все клетки змейки все блоки
        if hasattr(self, 'food') and self.food: # чтобы новая еда не появилась поверх старой
            occ.add(self.food.pos)
        return occ

    def _spawn_food(self):
        self.food = Food(self._forbidden()) # создаём еду в свободном месте
    def _spawn_powerup(self):
        fb = self._forbidden() #берём запрещённые клетки
        if self.powerup: #если уже есть бонус
            fb.add(self.powerup.pos) #чтобы не было 2 бонуса в одной клетке
        self.powerup = PowerUp(fb) #создаём новый powerup в свободной клетке

    def handle_event(self, event): #управление
        if event.type != pygame.KEYDOWN:
            return
        dirs = {
            pygame.K_UP:((0,-CELL_SIZE),(0, CELL_SIZE)),
            pygame.K_DOWN:((0, CELL_SIZE),(0,-CELL_SIZE)),
            pygame.K_LEFT:((-CELL_SIZE,0),( CELL_SIZE,0)),
            pygame.K_RIGHT:(( CELL_SIZE,0),(-CELL_SIZE,0)),
        }
        if event.key in dirs:
            nd, opp = dirs[event.key]
            if self.direction != opp: #нельзя мгновенно развернуться на 180
                self.next_dir = nd

    def update(self):
        self.direction = self.next_dir #направление
        # берём голову змейки и двигаем её
        hx = self.snake[0][0] + self.direction[0]
        hy = self.snake[0][1] + self.direction[1]

        if not (0 <= hx < WIDTH and 0 <= hy < HEIGHT): #выход за границы
            if self.shield_active:
                hx %= WIDTH
                hy %= HEIGHT
                self.shield_active = False # телепорт через край и щит исчезает
            else:
                return 'gameover'

        new_head = (hx, hy) #координаты следующей клетки
        for check in (self.snake[1:], self.obstacles): #проверка столкновений
            if new_head in check: #новая позиция головы совпала с чем-то
                if self.shield_active: #если есть щит
                    self.shield_active = False
                    return 'playing'
                return 'gameover'

        self.snake.insert(0, new_head) #new_head становится первым элементом списка
        hr = pygame.Rect(*new_head, CELL_SIZE, CELL_SIZE) #создаём hitbox

        if self.food and hr.colliderect(self.food.get_rect()):
            if self.food.kind == 'poison':
                for _ in range(3):
                    if len(self.snake) > 1: self.snake.pop()
                if len(self.snake) <= 1: return 'gameover'
            else:
                self.score += self.food.points
            self._spawn_food()
        else:
            self.snake.pop()

        if self.food and self.food.is_expired():
            self._spawn_food()

        now = pygame.time.get_ticks()
        if self.powerup:
            if self.powerup.is_expired():
                self.powerup = None
            elif hr.colliderect(self.powerup.get_rect()):
                self._apply_powerup(self.powerup.kind, now)
                self.powerup = None
        elif now - self.powerup_timer > 10000:
            self._spawn_powerup(); self.powerup_timer = now

        if self.active_effect and now > self.effect_end: #еЕсли бонус активен И его время вышло
            self._clear_effect()

        if self.score >= self.last_lvl_score + SCORE_PER_LEVEL and self.score > 0:
            self.level += 1
            self.speed = BASE_SPEED + (self.level-1)*SPEED_INCREMENT
            self.last_lvl_score = self.score #обновляем “контрольную точку”
            if self.level >= OBSTACLE_START_LEVEL: #добавление препятствий
                self._add_obstacles()

        return 'playing'

    def _apply_powerup(self, kind, now):
        self._clear_effect()
        self.active_effect = kind; self.effect_end = now + POWERUP_DURATION
        if kind == 'speed':    self.speed = min(self.speed+4, 20)
        elif kind == 'slow':   self.speed = max(self.speed-4, 3)
        elif kind == 'shield': self.shield_active = True

    def _clear_effect(self):
        if self.active_effect in ('speed','slow'):
            self.speed = BASE_SPEED + (self.level-1)*SPEED_INCREMENT
        self.active_effect = None; self.shield_active = False

    def _add_obstacles(self):
        hx, hy = self.snake[0]
        buffer = {(hx+dx*CELL_SIZE, hy+dy*CELL_SIZE) for dx in range(-3,4) for dy in range(-3,4)}
        forbidden = set(self.snake) | {self.food.pos} | buffer
        added = 0
        for _ in range(500):
            if added >= OBSTACLE_COUNT: break
            pos = random_cell(forbidden | self.obstacles)
            self.obstacles.add(pos); forbidden.add(pos); added += 1

    def draw(self):
        self.screen.fill(BG_COLOR)
        if self.settings.get('grid_overlay'):
            for x in range(0,WIDTH,CELL_SIZE):
                pygame.draw.line(self.screen,(30,30,45),(x,0),(x,HEIGHT))
            for y in range(0,HEIGHT,CELL_SIZE):
                pygame.draw.line(self.screen,(30,30,45),(0,y),(WIDTH,y))

        for obs in self.obstacles:
            pygame.draw.rect(self.screen, GRAY,(*obs,CELL_SIZE,CELL_SIZE))
            pygame.draw.rect(self.screen, LIGHT_GRAY, (*obs,CELL_SIZE,CELL_SIZE), 1)

        sc = tuple(self.settings.get('snake_color',[0,200,80]))
        for i, seg in enumerate(self.snake):
            c = tuple(min(255,x+60) for x in sc) if i==0 else sc
            pygame.draw.rect(self.screen, c, (*seg,CELL_SIZE-1,CELL_SIZE-1), border_radius=3)

        if self.shield_active:
            pygame.draw.rect(self.screen, PURPLE, (*self.snake[0],CELL_SIZE,CELL_SIZE), 2, border_radius=3)
        if self.food:
            self.food.draw(self.screen)
        if self.powerup:
            self.powerup.draw(self.screen, self.font_sm)

        for i, t in enumerate([f"Score:{self.score}", f"Level:{self.level}", f"Best:{self.best}"]):
            self.screen.blit(self.font.render(t,True,WHITE),(10,10+i*22))

        if self.active_effect:
            now = pygame.time.get_ticks()
            rem = max(0,(self.effect_end-now)//1000)
            lbl,col = {'speed':('SPEED',CYAN),'slow':('SLOW',BLUE),'shield':('SHIELD',PURPLE)}[self.active_effect]
            s = self.font.render(f"{lbl} {rem}s",True,col)
            self.screen.blit(s,(WIDTH-s.get_width()-10,10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                self.handle_event(event)
            state = self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.speed)
            if state == 'gameover': 
                return self.score, self.level