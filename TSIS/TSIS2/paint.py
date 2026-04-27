import pygame
import datetime
import tools

#  НАСТРОЙКИ 
W, H = 1200, 800
TB = 60 #Toolbar
FPS = 90

BRUSH = {'small': 2, 'medium': 5, 'large': 10}
PALETTE = ['black','white','red','green','blue','yellow','orange','purple','cyan','brown']

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Paint')
clock = pygame.time.Clock()

canvas = pygame.Surface((W, H-TB)) #область для рисования, которая НЕ включает тулбар
canvas.fill("white")

mode = "pen"
color = "blue"
size = "small"
radius = BRUSH[size] #radius = 2

draw = False #нажата ли мышь
prev = None
last = (0, 0)
line_buf = None

# line_buf = скриншот холста 📸
# ты каждый раз:
# откатываешься к скриншоту
# рисуешь новую линию

text_on = False #включён ли режим текста
text_pos = None #где печатать
text = "" #сам текст

font = pygame.font.SysFont(None, 28) 
font_big = pygame.font.SysFont(None, 36)
# SysFont(name, size)

# ПАЛИТРА В ТУЛБАРЕ 
# Квадратики цветов: рисуем справа, начиная с отступа
COLOR_SIZE = 36 #размер квадрата цвета = 36 px
COLOR_PAD = 4 # расстояние между ними = 4 px
palette_rects = {} 
# цвет → его положение на экране  'red': Rect(800, 12, 36, 36),

def build_palette(): #квадратики цветов в тулбаре
    palette_rects.clear()  #очищаем словарь (на случай, если пересоздаём)
    x = W - (COLOR_SIZE + COLOR_PAD) * len(PALETTE) #значит палитра начинается с x = 800
    for c in PALETTE:
        palette_rects[c] = pygame.Rect(x, (TB - COLOR_SIZE) // 2, COLOR_SIZE, COLOR_SIZE) # создаём прямоугольник (кнопку цвета)
        x += COLOR_SIZE + COLOR_PAD #двигаем позицию для следующего цвета
# TB - COLOR_SIZE) // 2 центр по вертикали в тулбаре

build_palette()

# Клавиши 1-9,0 → цвета (первые 10 из палитры)
KEY_COLORS = {
    pygame.K_1: 'black',
    pygame.K_2: 'white',
    pygame.K_3: 'red',
    pygame.K_4: 'green',
    pygame.K_5: 'blue',
    pygame.K_6: 'yellow',
    pygame.K_7: 'orange',
    pygame.K_8: 'purple',
    pygame.K_9: 'cyan',
    pygame.K_0: 'brown',
}

# UI 
def toolbar():
    screen.fill((220, 220, 220), (0, 0, W, TB)) # рисует серую полоску сверху
    pygame.draw.line(screen, (150, 150, 150), (0, TB), (W, TB)) # рисует границу между тулбаром и холстом
    # pygame.draw.line(surface, color, start_pos, end_pos, width)

    # Текущий режим и размер — слева
    label = font.render(f"Mode: {mode}  Size: {size}({radius}px)  Q=clear  Ctrl+S=save", True, (50, 50, 50))
    # font.render(text, antialias, color, background=None) antialias сглаживание текста
    screen.blit(label, (10, (TB - label.get_height()) // 2)) #нарисовать картинку на экран
    # X = 10 отступ слева Y = (TB - label.get_height()) // 2 центрируем текст по вертикали внутри тулбара

    # Палитра — справа
    for c, rect in palette_rects.items():
        pygame.draw.rect(screen, pygame.Color(c), rect) # закрашенный прямоугольник (квадрат цвета)
        if c == color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3) # Белая рамка толстая белая 
            # pygame.draw.rect(surface, color, rect, width) если width = 0 → залитый прямоугольник если width > 0 → только рамка
            pygame.draw.rect(screen, (0, 0, 0), rect, 1) #тонкая чёрная обводка
        else:
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)  # обычная серая рамка

def cp(pos):  #перевод координат мыши на canvas and убираем тулбар из координат
    return pos[0], pos[1] - TB

def inside(pos): # проверяет: где кликнули 
    return pos[1] >= TB
# pos[1] < TB → ты в тулбаре ❌
# pos[1] >= TB → ты на холсте ✔

 
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        # KEYBOARD
        if e.type == pygame.KEYDOWN:

            if text_on:
                if e.key == pygame.K_RETURN: #Enter
                    canvas.blit(font_big.render(text, True, pygame.Color(color)), text_pos)
                    text, text_on = "", False
                    # text = "" → очищаем буфер текста     text_on = False → выходим из режима текста
                elif e.key == pygame.K_BACKSPACE:
                    text = text[:-1] #удаляет последний символ
                elif e.key == pygame.K_ESCAPE:
                    text_on = False
                    text = ""
                elif e.unicode and e.unicode.isprintable():
                    text += e.unicode
                continue # если я в режиме текста — ВСЁ, больше ничего не делай
            # e.unicode → символ клавиши нажал A → "a" нажал 1 → "1"   isprintable() → проверяет: можно ли его напечатать

            if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL: #Сохранение
                # pygame.key.get_mods() возвращает, какие “дополнительные клавиши” зажаты     pygame.KMOD_CTRL проверяет зажат ли именно Ctrl
                # &  есть ли Ctrl среди зажатых клавиш
                name = f"canvas_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
                pygame.image.save(canvas, name)
                print(f"Сохранено: {name}")

            if e.key == pygame.K_q: #Очистка
                canvas.fill("white")

            # Инструменты
            keys = {
                pygame.K_p: "pen",
                pygame.K_l: "line",
                pygame.K_r: "rectangle",
                pygame.K_c: "circle",
                pygame.K_z: "square",
                pygame.K_t: "right_tri",
                pygame.K_u: "eq_tri",
                pygame.K_h: "rhombus",
                pygame.K_x: "text",
                pygame.K_f: "fill",
                pygame.K_e: "erase",
            }
            mode = keys.get(e.key, mode) # либо инструмент либо карандаш по дефолту


            if e.key == pygame.K_MINUS:
                size, radius = "small",  BRUSH["small"]
            if e.key == pygame.K_EQUALS:
                size, radius = "medium", BRUSH["medium"]
            if e.key == pygame.K_BACKQUOTE:
                size, radius = "large",  BRUSH["large"]

            # Цвета — клавиши 1-0
            if e.key in KEY_COLORS:
                color = KEY_COLORS[e.key]

        # MOUSE DOWN
        if e.type == pygame.MOUSEBUTTONDOWN:

            # Клик по тулбару — проверяем палитру
            if not inside(e.pos): #клик НЕ на canvas
                for c, rect in palette_rects.items(): #Проверка палитры
                    if rect.collidepoint(e.pos): #ты попал курсором в кнопку?
                        color = c
                continue # ВСЁ, дальше этот клик больше не обрабатываем

            p = cp(e.pos) #переводим мышь в координаты canvas

            if mode == "text":
                text_on = True
                text_pos = p #запоминаем место клика
                text = "" #очищаем строку
                continue #дальше НИЧЕГО не делаем (не рисуем)

            if mode == "fill": #Режим заливки
                tools.flood_fill(canvas, p, color)
                continue

            draw = True #начинаем рисовать
            prev = p #запоминаем точку старта

            if mode == "pen":
                pygame.draw.circle(canvas, pygame.Color(color), p, radius)

            if mode == "line":
                line_buf = canvas.copy() #создаётся копия текущего холста экран обновляется постоянно

        # MOUSE UP
        if e.type == pygame.MOUSEBUTTONUP: 
            draw = False #Остановка рисования
            if prev: # Проверка есть ли стартовая точка
                p = cp(e.pos) #получаем конечную точку (где отпустил мышь)

                if mode == "line" and line_buf:
                    canvas.blit(line_buf, (0, 0)) # Восстанавливаем старый рисунок
                    tools.draw_straight_line(canvas, prev, p, radius, color)
                elif mode == "rectangle":
                    tools.draw_rectangle(canvas, prev, p, radius, color)
                elif mode == "circle":
                    tools.draw_circle(canvas, prev, p, radius, color)
                elif mode == "square":
                    tools.draw_square(canvas, prev, p, radius, color)
                elif mode == "right_tri":
                    tools.draw_right_triangle(canvas, prev, p, radius, color)
                elif mode == "eq_tri":
                    tools.draw_equilateral_triangle(canvas, prev, p, radius, color)
                elif mode == "rhombus":
                    tools.draw_rhombus(canvas, prev, p, radius, color)
                #сбрасываешь память
                prev = None
                line_buf = None


        if e.type == pygame.MOUSEMOTION:
            p = cp(e.pos) # переводим координаты мыши в canvas (убираем toolbar)

            if draw:
                if mode == "pen":
                    tools.draw_line_bresenham(canvas, last, p, radius, color)
                elif mode == "erase":
                    tools.draw_line_bresenham(canvas, last, p, radius + 4, "white")
                elif mode == "line" and line_buf and prev: #есть ли снимок и старт
                    canvas.blit(line_buf, (0, 0))
                    tools.draw_straight_line(canvas, prev, p, radius, color)

            last = p


    toolbar()
    screen.blit(canvas, (0, TB))

    if text_on and text_pos:
        screen.blit(
            font_big.render(text + "|", True, pygame.Color(color)), #"|",визуальный курсор
            (text_pos[0], text_pos[1] + TB)
        )

    pygame.display.flip()
    clock.tick(FPS)