import pygame 
import time
import math
pygame.init()

#пайда болатын экран ұзындықтары
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

#пайда болған экранның жоғар жағындағы атау
pygame.display.set_caption("Mickey clock")

#суреттерді пайда болған экранға енгіземіз
leftarm = pygame.image.load("images/leftarm.png")
rightarm = pygame.image.load("images/rightarm.png")
mainclock = pygame.transform.scale(pygame.image.load("images/clock.png"), (800, 600)) #масштабирования изображения

done = False

while not done: 
    for event in pygame.event.get():# Получаем все события, которые происходят в окне
        if event.type == pygame.QUIT:
            done = True
    #localtime арқылы минут пен секундты анықтап аламыз
    current_time = time.localtime()
    minute = current_time.tm_min
    second = current_time.tm_sec
    
    #минут пен секундтың бұрышын алып аламыз
    #қазіргі минут * 360 градус / 60 минут + қазіргі секундты қосамыз    
    minute_angle = minute * 6    + (second / 60) * 6   
    second_angle = second * 6  
    
    #экран бетіне пайда фонмен болуы
    screen.blit(mainclock, (0,0))
    
    rotated_rightarm = pygame.transform.rotate(pygame.transform.scale(rightarm, (800, 600)), -minute_angle)#Масштабирует картинку стрелки,Поворачивает уже масштабированную картинку на угол
    rightarmrect = rotated_rightarm.get_rect(center=(800 // 2, 600 // 2 + 12))
    screen.blit(rotated_rightarm, rightarmrect)
    
    rotated_leftarm = pygame.transform.rotate(pygame.transform.scale(leftarm, (40.95, 682.5)), -second_angle)
    leftarmrect = rotated_leftarm.get_rect(center=(800 // 2, 600 // 2 + 10))
    screen.blit(rotated_leftarm, leftarmrect)
    
    pygame.display.flip() #окноны жаңартады
    clock.tick(60) #fps
    
pygame.quit()

# pygame.transform.scale(surface, (new_width, new_height))
# surface — это объект изображения (например, загруженный через pygame.image.load()).
# (new_width, new_height) — новые размеры картинки в пикселях.

# for event in pygame.event.get():  
# Получаем все события, которые происходят в окне (например, нажатие клавиш, движение мыши, закрытие окна).

# модуле time функция time.localtime() возвращает объект типа struct_time — это структура, где каждая часть времени хранится в отдельном поле.
# У этой структуры есть атрибуты (поля), например:
# tm_hour — часы (0–23)
# tm_min — минуты (0–59)
# tm_sec — секунды (0–59)

# screen.blit(...) — это метод, который рисует (копирует) изображение или поверхность (Surface) на экран.
# (0,0) — это координаты, куда картинка будет нарисована.
# В Pygame система координат начинается в левом верхнем углу окна:
# x = 0 — край слева,
# y = 0 — край сверху

# pygame.transform.rotate(surface, angle)
# surface — это картинка или поверхность, которую ты хочешь повернуть (например, загруженная через pygame.image.load()).
# angle — угол поворота в градусах.

# rotated_rightarm.get_rect(...)  
# Метод get_rect() возвращает прямоугольник (объект Rect), который описывает границы картинки rotated_rightarm.
# С помощью него можно удобно управлять положением изображения на экране.

# center=(800 // 2, 600 // 2 + 12)  
# Здесь задаётся точка, вокруг которой картинка будет расположена.

# 800 // 2 = 400 → середина окна по горизонтали.

# 600 // 2 = 300 → середина окна по вертикали.

# + 12 немного смещает центр вниз, чтобы стрелка выглядела правильно относительно циферблата.

# Зачем нужен Rect:
# Управление положением: можно задать center, topleft, bottomright и другие точки, чтобы разместить картинку именно там, где нужно.
# После вращения: картинка меняет размеры, и без Rect её было бы сложно правильно поставить в центр.

# screen.blit(rotated_rightarm, rightarmrect) говорит:
# «Возьми повернутую минутную стрелку и нарисуй её на экране в том месте, которое указано в rightarmrect (центр часов)».


# Обновляет всё окно целиком.
# pygame.display.flip()
# То есть все изменения, которые ты нарисовал с помощью screen.blit(...), становятся видимыми для пользователя.
# clock.tick(60)
# Ограничивает скорость выполнения цикла до 60 кадров в секунду (FPS).


#  fake_seconds += 1   # каждый кадр +1
#     second = fake_seconds % 60
#     minute = (fake_seconds // 60) % 60


# now = pygame.time.get_ticks()
#    if now - last_update >= 2000:   # задержка 2 секунды
#         second += 1
#         if second >= 60:
#             second = 0
#             minute += 1
#         last_update = now