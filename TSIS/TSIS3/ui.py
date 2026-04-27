import pygame, sys
from persistence import load_leaderboard, save_settings

BG_DARK, BG_MID = (15,18,30), (25,30,50)
ACCENT, ACCENT2  = (255,200,40), (80,180,255) #основной цвет (жёлтый) второй акцент (синий)
WHITE, GREY      = (240,240,255), (130,140,160) # текст
RED_LIGHT        = (255,80,80) # ошибки or кнопка выхода
SW, SH           = 400, 600

def draw_bg(surf): # рисует фон (сетку)
    surf.fill(BG_DARK)
    for y in range(0, SH, 40): pygame.draw.line(surf, BG_MID, (0,y), (SW,y)) #оризонтальные линии
    for x in range(0, SW, 40): pygame.draw.line(surf, BG_MID, (x,0), (x,SH)) #вертикальные линии

def draw_panel(surf, rect, color=BG_MID, alpha=220): # полупрозрачные окна   0 → полностью прозрачный   255 → полностью непрозрачный
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA) #SRCALPHA поддержка прозрачности
    s.fill((*color, alpha))
    surf.blit(s, rect.topleft) #накладывает эту панель на экран
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=10) #рисует рамку

def blit_c(surf, img, cx, cy): # рисует картинку/текст по центру
    surf.blit(img, img.get_rect(center=(cx, cy)))

class Button:
    _font = None # переменная класса
    def __init__(self, text, center, width=220, height=44, color=ACCENT, text_color=BG_DARK):
        if Button._font is None: # создаётся 1 раз на все кнопки
            Button._font = pygame.font.SysFont("Consolas", 20, bold=True)
        self.rect = pygame.Rect(0,0,width,height); self.rect.center = center
        self.text, self.color, self.text_color, self.hovered = text, color, text_color, False #hovered = False (курсор не наведен)

    def draw(self, surf): #рисует кнопку
        c = tuple(min(255,v+30) for v in self.color) if self.hovered else self.color #навели мышку кнопка становится светлее
        pygame.draw.rect(surf, c, self.rect, border_radius=8) #рисует залитую кнопку
        pygame.draw.rect(surf, WHITE, self.rect, 1, border_radius=8) # рамку
        blit_c(surf, Button._font.render(self.text, True, self.text_color), *self.rect.center) #рисует текст по центру кнопки

    def handle(self, event): #брабатывает события мыши
        if event.type == pygame.MOUSEMOTION: #мышка над кнопкой или нет
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN: #кликнули по кнопке возвращает True
            return self.rect.collidepoint(event.pos)
        return False

# Username 
def username_screen(surf, clock):
    f32 = pygame.font.SysFont("Consolas", 32, bold=True) # заголовок
    f18 = pygame.font.SysFont("Consolas", 18) # подсказки
    f26 = pygame.font.SysFont("Consolas", 26, bold=True) # вводимое имя
    btn = Button("START RACE", (SW//2, 430))
    name, cur_vis, cur_t = "", True, 0 
    #cur_vis → мигающий курсор (|)  name → текст игрока cur_t → таймер для мигания

    while True:
        dt = clock.tick(60); cur_t += dt
        if cur_t > 500: # каждые ~0.5 сек курсор включается/выключается
            cur_vis, cur_t = not cur_vis, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # Ввод с клавиатуры
                if   event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif len(name) < 14 and event.unicode.isprintable(): # event.unicode.isprintable() можно ли этот символ нормально напечатать
                    name += event.unicode # добавить символ к строке name
            if btn.handle(event) and name.strip(): # можно нажать мышкой вместо Enter
                return name.strip()
        draw_bg(surf) #фон
        blit_c(surf, f32.render("ENTER YOUR NAME", True, ACCENT), SW//2, 160)
        blit_c(surf, f18.render("Your name will appear on the leaderboard", True, GREY), SW//2, 200)
        #серое окно для ввода
        box = pygame.Rect(60, 260, 280, 52)
        draw_panel(surf, box)
        blit_c(surf, f26.render(name+("|" if cur_vis else " "), True, WHITE), *box.center) #имя + мигающий курсор
        if not name.strip():
            blit_c(surf, f18.render("Type your name to continue", True, RED_LIGHT), SW//2, 330)
        btn.draw(surf)
        pygame.display.flip()

# Main Menu 
def main_menu(surf, clock):
    f46 = pygame.font.SysFont("Consolas", 46, bold=True)
    f14 = pygame.font.SysFont("Consolas", 14)
    btns = { # словарь кнопок
        "play": Button(" PLAY", (SW//2, 260)),
        "leaderboard": Button(" LEADERBOARD", (SW//2, 320), color=ACCENT2, text_color=BG_DARK),
        "settings": Button(" SETTINGS", (SW//2, 380), color=GREY,    text_color=WHITE),
        "quit": Button(" QUIT", (SW//2, 440), color=RED_LIGHT, text_color=WHITE),
    }
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            for k, b in btns.items():
                if b.handle(event): # мышка кликнула по кнопке
                    return k # возвращает ключ кнопки
        draw_bg(surf)
        blit_c(surf, f46.render("RACER", True, ACCENT), SW//2, 140)
        blit_c(surf, f14.render("TSIS 3 — Advanced Edition", True, GREY), SW//2, 185) # подзаголовок
        for x in [100,200,300]: # красивые линии
            pygame.draw.line(surf, (*GREY,60), (x,210), (x,230), 2)
        for b in btns.values():  #рисуем кнопки
            b.draw(surf)
        pygame.display.flip()

#  Settings 
def settings_screen(surf, clock, settings):
    f30 = pygame.font.SysFont("Consolas", 30, bold=True) # заголовки
    f18 = pygame.font.SysFont("Consolas", 18) # подписи
    CAR_RGB   = {"red":(220,50,50),"blue":(50,100,220),"green":(50,200,80),"yellow":(240,200,30)}
    COLORS    = list(CAR_RGB.keys())
    DIFFS     = ["easy","normal","hard"]
    save_btn  = Button("SAVE", (SW//2, 490), color=ACCENT, text_color=BG_DARK)
    back_btn  = Button(" BACK", (SW//2, 540), color=GREY,   text_color=WHITE)
    local     = settings.copy() # локальная копия настроек     менять настройки временно   и сохранить только если нажали SAVE

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return settings # выйти без сохранения
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if pygame.Rect(250,168,100,34).collidepoint(mx,my):
                    local["sound"] = not local["sound"] # переключает ON/OFF
                for i,col in enumerate(COLORS): # меняется car_color
                    if pygame.Rect(60+i*65,258,44,44).collidepoint(mx,my): local["car_color"] = col
                for i,d in enumerate(DIFFS): # выбираешь easy / normal / hard
                    if pygame.Rect(50+i*105,358,90,36).collidepoint(mx,my): local["difficulty"] = d
            if save_btn.handle(event): # кнопка SAVE
                save_settings(local)
                return local
            if back_btn.handle(event): # BACK
                return settings
        draw_bg(surf)
        blit_c(surf, f30.render("SETTINGS", True, ACCENT), SW//2, 60)
        surf.blit(f18.render("Sound:", True, WHITE), (60,175))
        pygame.draw.rect(surf, (80,220,80) if local["sound"] else RED_LIGHT, (250,168,100,34), border_radius=6) #кнопка ON/OFF:
        blit_c(surf, f18.render("ON" if local["sound"] else "OFF", True, BG_DARK), 300, 185) # екст внутри кнопки
        surf.blit(f18.render("Car Color:", True, WHITE), (60,235))
        for i,col in enumerate(COLORS): # рисуются квадраты цветов:
            cr = pygame.Rect(60+i*65,258,44,44)
            pygame.draw.rect(surf, CAR_RGB[col], cr, border_radius=6)  #сам цветной квадрат
            if local["car_color"] == col: # сли выбран → белая рамка
                pygame.draw.rect(surf, WHITE, cr, 3, border_radius=6)
        surf.blit(f18.render("Difficulty:", True, WHITE), (60,335))
        for i,d in enumerate(DIFFS): # рисуются кнопки
            dr = pygame.Rect(50+i*105,358,90,36)
            active = local["difficulty"]==d
            pygame.draw.rect(surf, ACCENT if active else BG_MID, dr, border_radius=6) #если выбрано
            pygame.draw.rect(surf, WHITE, dr, 1, border_radius=6)
            blit_c(surf, f18.render(d.upper(), True, BG_DARK if active else WHITE), *dr.center) # текст внутри кнопки
        save_btn.draw(surf) # SAVE и BACK
        back_btn.draw(surf)
        pygame.display.flip()

#  Game Over 
def game_over_screen(surf, clock, score, distance, coins):  # экран "игра окончена"
    f40 = pygame.font.SysFont("Consolas", 40, bold=True)     # большой шрифт (GAME OVER)
    f22 = pygame.font.SysFont("Consolas", 22, bold=True)     # средний шрифт (значения)
    f16 = pygame.font.SysFont("Consolas", 16)                # маленький шрифт (подписи)
    retry_btn = Button(" RETRY", (SW//2, 440), color=ACCENT, text_color=BG_DARK)  # кнопка "заново"
    menu_btn  = Button(" MAIN MENU", (SW//2, 495), color=GREY, text_color=WHITE)   # кнопка в меню
    while True:  # бесконечный цикл экрана
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():  # обработка событий
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()  # закрытие окна
            if retry_btn.handle(event): return "retry"  # если нажали retry перезапуск
            if menu_btn.handle(event):  return "menu"   # если нажали menu в меню
        draw_bg(surf)  # рисуем фон
        blit_c(surf, f40.render("GAME OVER", True, RED_LIGHT), SW//2, 120)  # надпись GAME OVER
        draw_panel(surf, pygame.Rect(60,180,280,220))  # полупрозрачная панель
        for i,(lbl,val) in enumerate([  # список статистики
            ("SCORE", str(score)), # очки
            ("DISTANCE", f"{distance} m"), # дистанция
            ("COINS", str(coins)) # монеты
        ]):
            y = 210 + i*60  # вертикальное смещение строк     строки идут вниз с одинаковым шагом
            surf.blit(f16.render(lbl, True, GREY), (90, y))       # подпись (SCORE)
            surf.blit(f22.render(val, True, ACCENT), (90, y+20))  # значение (1000)
        retry_btn.draw(surf)  # рисуем кнопку retry
        menu_btn.draw(surf)   # рисуем кнопку menu

        pygame.display.flip()  # обновляем экран
#  Leaderboard 
def leaderboard_screen(surf, clock):
    f30  = pygame.font.SysFont("Consolas", 30, bold=True) #заголовок
    f16  = pygame.font.SysFont("Consolas", 16) # обычные значения
    f14  = pygame.font.SysFont("Consolas", 14, bold=True) #  заголовки таблицы
    back = Button(" BACK", (SW//2, 555), color=GREY, text_color=WHITE) # кнопка вернуться назад
    lb   = load_leaderboard() # агружает список рекордов (из файла )
    MEDALS = {0:(255,215,0), 1:(192,192,192), 2:(184,115,51)} # цвета мест
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back.handle(event): # назад
                return
        draw_bg(surf)
        blit_c(surf, f30.render("LEADERBOARD", True, ACCENT), SW//2, 40)
        for txt,x in zip(["#","NAME","SCORE","DIST","COINS"],[30,70,180,270,350]): #заголовки колонок
            surf.blit(f14.render(txt,True,GREY),(x,80))
        pygame.draw.line(surf, GREY, (20,97),(380,97)) # разделяет заголовок и таблицу
        if not lb: # если нет данных
            blit_c(surf, f16.render("No scores yet — play a game!", True, GREY), SW//2, 300)
        else:
            for i,e in enumerate(lb[:10]): # берёт ТОП-10 игроков
                y, col = 108+i*42, MEDALS.get(i,WHITE) #каждая строка ниже предыдущей     цвет места
                for txt,x in zip([str(i+1),e["name"][:10],str(e["score"]),f'{e["distance"]}m',str(e["coins"])],[30,70,180,270,350]): # вывод данных
                    surf.blit(f16.render(txt,True,col if x<180 else (ACCENT if x==180 else (WHITE if x==270 else GREY))),(x,y))
                if i<9:
                    pygame.draw.line(surf,BG_MID,(20,y+30),(380,y+30)) # разделительную линию между строками
        back.draw(surf)
        pygame.display.flip()