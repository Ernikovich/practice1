import pygame 
 
WIDTH, HEIGHT = 1200, 800  # ширина и высота окна
FPS = 90  # частота обновления экрана
draw = False   # флаг, указывающий рисуем ли сейчас           
radius = 2    # радиус кисти
color = 'blue'  # текущий цвет кисти         
mode = 'pen'    # режим рисования (ручка, круг, прямоугольник, ластик)               
 
pygame.init() 
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # создаём окно указанного размера
pygame.display.set_caption('Paint') # заголовок окна
clock = pygame.time.Clock() # управление временем
screen.fill(pygame.Color('white'))  # закрашиваем экран белым
font = pygame.font.SysFont('None', 60) # создаём шрифт для отображения текста
 
def drawLine(screen, start, end, width, color): 
    # извлекаем координаты начальной и конечной точки
    x1 = start[0] 
    x2 = end[0] 
    y1 = start[1] 
    y2 = end[1] 
    
    # считаем разницу по осям
    dx = abs(x1 - x2) 
    dy = abs(y1 - y2) 
    
    # коэффициенты уравнения прямой Ax + By + C = 0
    A = y2 - y1  
    B = x1 - x2  
    C = x2 * y1 - x1 * y2 
    
    # если линия больше горизонтальная
    if dx > dy: 
        if x1 > x2: 
            x1, x2 = x2, x1 
            y1, y2 = y2, y1 
        for x in range(x1, x2): 
            y = (-C - A * x) / B 
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width) 
    # если линия больше вертикальная
    else: 
        if y1 > y2: 
            x1, x2 = x2, x1 
            y1, y2 = y2, y1 
        for y in range(y1, y2): 
            x = (-C - B * y) / A 
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)

def drawCircle(screen, start, end, width, color): 
    # извлекаем координаты начальной и конечной точки
    x1 = start[0]  
    x2 = end[0]  
    y1 = start[1]  
    y2 = end[1]  
    
    # центр круга
    x = (x1 + x2) / 2  
    y = (y1 + y2) / 2  
    
    # радиус круга
    radius = abs(x1 - x2) / 2  
    
    # рисуем круг
    pygame.draw.circle(screen, pygame.Color(color), (x, y), radius, width)  

def drawRectangle(screen, start, end, width, color): 
    # извлекаем координаты начальной и конечной точки
    x1 = start[0]  
    x2 = end[0]  
    y1 = start[1]  
    y2 = end[1]  
    
    # ширина и высота прямоугольника
    widthr = abs(x1 - x2)  
    height = abs(y1 - y2)  
    
    # рисуем прямоугольник в зависимости от положения точек
    if x2 > x1 and y2 > y1: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, widthr, height), width)  
    if y2 > y1 and x1 > x2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, widthr, height), width)  
    if x1 > x2 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, widthr, height), width)  
    if x2 > x1 and y1 > y2: 
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, widthr, height), width)  

def drawSquare(screen, start, end, width, color):
    x1,y1=start
    x2,y2=end
    size = min(abs(x2 - x1), abs(y2 - y1))
    rect=pygame.Rect(min(x1,x2),min(y1,y2),size,size)
    pygame.draw.rect(screen, pygame.Color(color), rect, width)
    # min(x1, x2) и min(y1, y2) — выбираем верхний левый угол 
def drawRightTriangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(screen, pygame.Color(color), points) 

def drawEquilateralTriangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    base = abs(x2 - x1)
    height = (3 ** 0.5 / 2) * base
    points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
    pygame.draw.polygon(screen, pygame.Color(color), points, width)
    # ((x1 + x2) // 2, y2 - height) — верхняя точка (середина основания по X и поднятая вверх на высоту).

def drawRhombus(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    points = [((x1 + x2) // 2, y1), (x1, (y1 + y2) // 2), ((x1 + x2) // 2, y2), (x2, (y1 + y2) // 2)]
    pygame.draw.polygon(screen, pygame.Color(color), points, width)


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()  # выход из программы при закрытии окна
         
        # обработка клавиатуры
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_r: 
                mode = 'rectangle'  # режим прямоугольника
            if event.key == pygame.K_c: 
                mode = 'circle'  # режим круга
            if event.key == pygame.K_s:
                mode = 'square'
            if event.key == pygame.K_t:
                mode = 'right_tri'
            elif event.key == pygame.K_u:
                mode = 'eq_tri'
            elif event.key == pygame.K_h:
                mode = 'rhombus'
            if event.key == pygame.K_p: 
                mode = 'pen'  # режим ручки
            if event.key == pygame.K_e: 
                mode = 'erase'  # режим ластика
            if event.key == pygame.K_q: 
                screen.fill(pygame.Color('white'))  # очистка экрана
 
            # смена цвета
            if event.key == pygame.K_1: 
                color = 'black'  
            if event.key == pygame.K_2: 
                color = 'green'  
            if event.key == pygame.K_3: 
                color = 'red'  
            if event.key == pygame.K_4: 
                color = 'blue'  
            if event.key == pygame.K_5: 
                color = 'yellow'  
   
        if event.type == pygame.MOUSEBUTTONDOWN:  
            draw = True  # включаем рисование
            if mode == 'pen': 
                pygame.draw.circle(screen, pygame.Color(color), event.pos, radius)  
            prevPos = event.pos  # сохраняем позицию

        if event.type == pygame.MOUSEBUTTONUP:  
            if mode == 'pen':
                draw = False
            if mode == 'erase':
                draw = False
            if mode == 'rectangle': 
                drawRectangle(screen, prevPos, event.pos, radius, color)  
            elif mode == 'circle': 
                drawCircle(screen, prevPos, event.pos, radius, color)  
            elif mode == 'square':
                drawSquare(screen, prevPos, event.pos, color)
            elif mode == 'right_tri':
                drawRightTriangle(screen, prevPos, event.pos, color)
            elif mode == 'eq_tri':
                drawEquilateralTriangle(screen, prevPos, event.pos, radius, color)
            elif mode == 'rhombus':
                drawRhombus(screen, prevPos, event.pos, radius, color)
       
        if event.type == pygame.MOUSEMOTION:  
            if draw and mode == 'pen': 
                drawLine(screen, lastPos, event.pos, radius, color)  
            elif draw and mode == 'erase': 
                drawLine(screen, lastPos, event.pos, radius, 'white')  
            lastPos = event.pos  # обновляем позицию
 
    # индикатор радиуса
    pygame.draw.rect(screen, pygame.Color('white'), (10, 10, 150, 50))  
    renderRadius = font.render("Radius: " + str(radius), True, pygame.Color(color))  
    screen.blit(renderRadius, (20, 20))

    pygame.display.flip()  # обновляем экран
    clock.tick(FPS)  # ограничиваем FPS
