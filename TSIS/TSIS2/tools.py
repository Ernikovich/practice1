import pygame
from collections import deque


def draw_line_bresenham(screen, start, end, width, color):
    """Рисует линию через пиксели (алгоритм из Practice 10)."""
    x1, y1 = int(start[0]), int(start[1])
    x2, y2 = int(end[0]), int(end[1])
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    if dx > dy:
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for x in range(x1, x2):
            if B != 0:
                y = (-C - A * x) / B
                pygame.draw.circle(screen, pygame.Color(color), (x, int(y)), width)
    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for y in range(y1, y2):
            if A != 0:
                x = (-C - B * y) / A
                pygame.draw.circle(screen, pygame.Color(color), (int(x), y), width)


def draw_straight_line(screen, start, end, width, color):
    """Рисует прямую линию pygame.draw.line."""
    pygame.draw.line(screen, pygame.Color(color), start, end, width)


def draw_circle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    radius = abs(x1 - x2) / 2
    if radius > 0:
        pygame.draw.circle(screen, pygame.Color(color), (int(cx), int(cy)), int(radius), width)


def draw_rectangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    w = abs(x1 - x2)
    h = abs(y1 - y2)
    rx = min(x1, x2)
    ry = min(y1, y2)
    pygame.draw.rect(screen, pygame.Color(color), (rx, ry, w, h), width)


def draw_square(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    size = min(abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(screen, pygame.Color(color), (min(x1, x2), min(y1, y2), size, size), width)


def draw_right_triangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(screen, pygame.Color(color), points, width)


def draw_equilateral_triangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    base = abs(x2 - x1)
    height = (3 ** 0.5 / 2) * base
    points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, int(y2 - height))]
    pygame.draw.polygon(screen, pygame.Color(color), points, width)


def draw_rhombus(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    points = [
        ((x1 + x2) // 2, y1),
        (x1, (y1 + y2) // 2),
        ((x1 + x2) // 2, y2),
        (x2, (y1 + y2) // 2)
    ]
    pygame.draw.polygon(screen, pygame.Color(color), points, width)


def flood_fill(screen, pos, fill_color_str):
    """BFS flood fill по пикселям."""
    fill_color = pygame.Color(fill_color_str) #превращаем текст в цвет pygame
    x, y = int(pos[0]), int(pos[1])
    w, h = screen.get_size() #чтобы не выйти за границы

    # Цвет пикселя в точке клика
    target_color = screen.get_at((x, y))

    # Если уже такого цвета — ничего не делать
    if target_color == fill_color:
        return

    queue = deque() # создаём “список задач”, куда будем добавлять пиксели
    queue.append((x, y)) #кладём первую точку (где кликнули)
    visited = set() # список уже обработанных пикселей
    visited.add((x, y))

    while queue: 
        cx, cy = queue.popleft()#чтобы не обрабатывать дважды чтобы двигаться дальше
        if screen.get_at((cx, cy)) != target_color: # если цвет пикселя НЕ такой, как мы хотим — пропусти его
            continue
        screen.set_at((cx, cy), fill_color)
        for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]: #берём 4 соседние точки вокруг текущей
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited: #Не выйти за пределы экрана
                visited.add((nx, ny))
                queue.append((nx, ny))

# set_at — это команда Pygame, которая закрашивает один конкретный пиксель на экране
# cx+1 → вправо
# cx-1 → влево
# cy+1 → вниз
# cy-1 → вверх