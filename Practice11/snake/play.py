import pygame,sys,random,time

#  Инициализация 
pygame.init()
WIDTH,HEIGHT=600,400
CELL_SIZE=20
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
clock=pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED   = (255,0,0)
WHITE = (255,255,255)

# Шрифт 
font=pygame.font.SysFont("Verdana",20)

# Начальные параметры 
snake=[(100,100)]# только голова
direction=(CELL_SIZE,0)# движение вправо
score=0
level=1
speed=10
last_level_score = 0

food=(200,200) # первая еда
food_size = CELL_SIZE
food_spawn_time = time.time()  # время появления еды
food_lifetime = 5              # еда исчезает через 5 секунд

while True:
     # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_UP and direction !=(0,CELL_SIZE):
                direction = (0, -CELL_SIZE)
            if event.key==pygame.K_DOWN and direction != (0,-CELL_SIZE):
                direction = (0, CELL_SIZE)
            if event.key==pygame.K_LEFT and direction != (CELL_SIZE,0):
                direction= (-CELL_SIZE,0)
            if event.key==pygame.K_RIGHT and direction != (-CELL_SIZE,0):
                direction = (CELL_SIZE,0)

# Движение змейки: добавляем новую голову
    new_head=(snake[0][0]+direction[0],snake[0][1]+direction[1])
    new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
    snake.insert(0, new_head) #змейка «сдвинулась» вперёд
    # новая голова добавилась в начало,
    # старая голова стала вторым сегментом
    # телепортируем голову на противоположную сторону

    # Проверка столкновения с собой
    if new_head in snake[1:]:
        print("Game Over")
        sys.exit()

    # Проверка еды (используем прямоугольники для столкновения)
    head_rect=pygame.Rect(new_head[0],new_head[1], CELL_SIZE, CELL_SIZE)
    food_rect = pygame.Rect(food[0], food[1], food_size, food_size)

# Проверка еды
    if head_rect.colliderect(food_rect):
        score+=1
        food=(random.randrange(0,WIDTH,CELL_SIZE),
              random.randrange(0,HEIGHT,CELL_SIZE))
        food_size=random.choice([10,20,30,40])# случайный размер еды
        food_spawn_time=time.time()# обновляем время появления
    else:
        snake.pop() # удаляем хвост, если еда не съедена

    # Проверка таймера еды: если прошло больше food_lifetime секунд, еда исчезает
    if time.time()-food_spawn_time>food_lifetime:
        food=(random.randrange(0,WIDTH,CELL_SIZE),
              random.randrange(0,HEIGHT,CELL_SIZE))
        food_size=random.choice([10,20,30,40])# случайный размер еды
        food_spawn_time=time.time()# обновляем время появления

    # Проверка перехода на новый уровень
    if score > 0 and score % 5 == 0 and score != last_level_score:
        level += 1
        last_level_score = score # запоминаем, что на этом счёте уровень уже был повышен.

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen,GREEN,(*segment,CELL_SIZE,CELL_SIZE))
        # segment = (x, y) → координаты сегмента.
        # pygame.draw.rect(surface, color, rect, width=0, border_radius=0)
        # rect
        # Координаты и размеры прямоугольника.
        # Можно передать:
        # кортеж (x, y, width, height),
        # или объект pygame.Rect(x, y, width, height).
    pygame.draw.rect(screen,RED,(*food,food_size,food_size))
    # food — координаты яблока (x, y).

    score_text=font.render(f"Score: {score}", True, (255,255,255))
    level_text=font.render(f"Level: {level}",True,(255,255,255))
    screen.blit(score_text, (10,10))
    screen.blit(level_text, (10,30))

    pygame.display.flip()
    clock.tick(speed)


 