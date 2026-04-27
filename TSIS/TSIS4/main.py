import pygame, sys
from config import *
from settings import load_settings, save_settings
from game import Game

try:
    import db as database # БАЗА ДАННЫХ
    DB_OK = database.init_db()
except Exception as e:
    print(f"[DB] No connection: {e}"); DB_OK = False

# UI helpers 

class Button:
    def __init__(self, rect, text, font, color=DARK_GRAY, hover=GRAY):
        self.rect  = pygame.Rect(rect)
        self.text  = text
        self.font = font
        self.color = color
        self.hover = hover # цвет при наведении

    def draw(self, surface):
        c = self.hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=6) # рисует прямоугольник
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6) # рамка
        s = self.font.render(self.text, True, WHITE)
        surface.blit(s, s.get_rect(center=self.rect.center)) # рисует текст по центру кнопки

    def clicked(self, event): # нажатие
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos)) # попадает ли мышь в прямоугольник
    # event.button == 1 левая кнопка мыши

def title(surface, text, font, y=30): #рисует текс
    s = font.render(text, True, WHITE) # превращает строку в картинку
    surface.blit(s, s.get_rect(centerx=WIDTH//2, y=y)) # размещение на экране

def mk_font(size, bold=False):
    return pygame.font.SysFont("Verdana", size, bold=bold)

#  Screens 
def screen_menu(surface, clock):
    F = mk_font(22)
    username = ""
    active = True
    btns = {
        'play': Button((WIDTH//2-100,240,200,42), "Play",        F),
        'lb':   Button((WIDTH//2-100,294,200,42), "Leaderboard", F),
        'set':  Button((WIDTH//2-100,348,200,42), "Settings",    F),
        'quit': Button((WIDTH//2-100,402,200,42), "Quit",        F, color=(100,30,30), hover=(160,50,50)),
    }
    inp = pygame.Rect(WIDTH//2-120, 178, 240, 36) # поле ввода
    while True:
        clock.tick(30)
        surface.fill(BG_COLOR)
        title(surface, "SNAKE", mk_font(32, bold=True))
        surface.blit(mk_font(18).render("Enter username:", True, LIGHT_GRAY), (inp.x, inp.y-22))
        pygame.draw.rect(surface, DARK_GRAY, inp, border_radius=5) # заливка поля ввода
        pygame.draw.rect(surface, GREEN if active else GRAY, inp, 2, border_radius=5) # рамку вокруг поля
        surface.blit(mk_font(18).render(username+("|" if active else ""), True, WHITE), (inp.x+8, inp.y+8)) # мигающий курсор
        for b in btns.values():
            b.draw(surface)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = inp.collidepoint(event.pos) #кликнули в поле → можно писать
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE: username = username[:-1] # удаляет последний символ
                elif event.key == pygame.K_RETURN:  active = False # отключает ввод
                elif len(username) < 20 and event.unicode.isprintable(): username += event.unicode # ввод букв
            for key, btn in btns.items(): # обработка кнопок
                if btn.clicked(event):
                    name = username.strip() or "Player"
                    if key == 'quit':
                        return None
                    return {'action': key, 'username': name} # возвращает словарь


def screen_gameover(surface, clock, score, level, best):
    F = mk_font(22)
    btns = {'retry': Button((WIDTH//2-110,330,200,44),"Retry",    F),
            'menu':  Button((WIDTH//2-110,386,200,44),"Main Menu",F)}
    while True:
        clock.tick(30)
        surface.fill(BG_COLOR)
        title(surface, "GAME OVER", mk_font(34,bold=True), y=60)
        if score >= best: # если игрок побил рекорд
            surface.blit(mk_font(18).render("New Personal Best!", True, YELLOW),
                         mk_font(18).render("x",True,WHITE).get_rect(centerx=WIDTH//2, y=155))
        for i,(t,c) in enumerate([(f"Score: {score}",WHITE),(f"Level: {level}",WHITE), # вывод статистики
                                   (f"Best:  {best}", YELLOW if score>=best else LIGHT_GRAY)]):
            s = F.render(t,True,c) # нарисуй текст как картинку
            surface.blit(s,s.get_rect(centerx=WIDTH//2, y=200+i*38)) # kаждая строка ниже предыдущей
        for b in btns.values():
            b.draw(surface) # pоказывает Retry и Menu
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for key, btn in btns.items():
                if btn.clicked(event):
                    return key
                
def screen_leaderboard(surface, clock):
    F  = mk_font(17)#чуть больше
    Fs = mk_font(15) # мелкий текст таблицы
    btn_back = Button((WIDTH//2-80, HEIGHT-60, 160,40), "Back", F) #кнопка назад
    rows = database.get_leaderboard(10) if DB_OK else [] # загрузка данных из БД
    COL_X = [30,80,280,360,430] # позиции столбцов таблицы
    while True:
        clock.tick(30)
        surface.fill(BG_COLOR)
        title(surface, "Leaderboard", mk_font(28,bold=True), y=20)
        if not rows: # если нет данных
            s = F.render("No records yet." if DB_OK else "DB not connected.", True, GRAY)
            surface.blit(s, s.get_rect(centerx=WIDTH//2, y=200))
        else:
            for hdr,cx in zip(["#","Player","Score","Level","Date"], COL_X):
                surface.blit(Fs.render(hdr,True,YELLOW),(cx,68))
            pygame.draw.line(surface, GRAY, (25,86),(WIDTH-25,86)) #разделяет заголовок и таблицу
            for i, row in enumerate(rows): #перебор игроков
                col = YELLOW if i==0 else (WHITE if i<3 else LIGHT_GRAY) #цвет строки смотря на медаль     
                date = row['played_at'].strftime("%m/%d") if row.get('played_at') else "-" # дата
                for val,cx in zip([str(i+1), row.get('username','?')[:14], # вывод ячеек
                                   str(row.get('score',0)), str(row.get('level_reached',0)), date], COL_X):
                    surface.blit(Fs.render(val,True,col),(cx, 95+i*28))
        btn_back.draw(surface)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.clicked(event):
                return


def screen_settings(surface, clock, settings):
    F = mk_font(20) #шрифт для текста в меню настроек
    COLORS = [("Green",(0,200,80)),("Blue",(50,130,255)),
              ("Orange",(255,140,0)),("Pink",(240,80,160)),("White",(230,230,230))] #список цветов
    cur_color = tuple(settings['snake_color']) #цвет змейки
    grid_on   = settings['grid_overlay'] #включена ли сетка
    sound_on  = settings['sound']
    btn_save  = Button((WIDTH//2-100,HEIGHT-65,200,44),"Save & Back",F,color=(20,100,40),hover=(30,150,60)) #Save & Back → сохранить и выйти
    btn_grid  = Button((WIDTH-140,170,80,30),"Toggle",F)# Toggle Grid → включить/выключить сетку 
    btn_sound = Button((WIDTH-140,220,80,30),"Toggle",F) #Toggle Sound → включить/выключить звук

    while True:
        clock.tick(30)
        surface.fill(BG_COLOR)
        title(surface,"Settings",mk_font(26,bold=True),y=25)
        surface.blit(F.render("Snake color:",True,LIGHT_GRAY),(60,90))
        swatches = []
        for i,(name,rgb) in enumerate(COLORS): #выбор цвета
            r = pygame.Rect(60+i*80,120,60,30)
            pygame.draw.rect(surface,rgb,r,border_radius=5)
            if rgb == cur_color: #белая рамка = выбранный цвет
                pygame.draw.rect(surface,WHITE,r,3,border_radius=5)
            swatches.append((r,rgb)) #сохраняем кликабельные зоны:
        surface.blit(F.render(f"Grid: {'ON' if grid_on else 'OFF'}",True,WHITE),(60,175))
        surface.blit(F.render(f"Sound: {'ON' if sound_on else 'OFF'}",True,WHITE),(60,225))
        btn_grid.draw(surface)
        btn_sound.draw(surface)
        btn_save.draw(surface)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #именно клик мыши левая кнопка (1)
                for r,rgb in swatches:
                    if r.collidepoint(event.pos): #если кликнули по цвету
                        cur_color = rgb
            if btn_grid.clicked(event): #toggle сетки
                grid_on  = not grid_on
            if btn_sound.clicked(event): #toggle звук
                sound_on = not sound_on
            if btn_save.clicked(event): #сохранение настроек
                settings.update({'snake_color':list(cur_color),'grid_overlay':grid_on,'sound':sound_on})
                save_settings(settings)
                return settings

#  Music 
MUSIC_PATH = "assests/sound/snake_music.mp3"
def apply_music(settings):
    if settings.get('sound'):
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(MUSIC_PATH)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"[Music] Could not load: {e}")
    else:
        pygame.mixer.music.stop()

#  Entry point 

def main():
    #инициализация Pygame
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake 4")
    clock = pygame.time.Clock()
    settings = load_settings() #читается settings.json
    player_id = None
    best = 0

    apply_music(settings) #включает музыку если sound = True

    while True:
        result = screen_menu(surface, clock) #показывает меню и ждёт выбор
        if result is None:
            pygame.quit()
            sys.exit()
        # что нажал игрок
        username = result['username']
        action   = result['action']

        if action == 'lb': #открыть таблицу рекордов
            screen_leaderboard(surface, clock); continue
        if action == 'set': #settings
            settings = screen_settings(surface, clock, settings)
            apply_music(settings); continue

        if DB_OK: # работа с БД
            player_id = database.get_or_create_player(username) # создать игрока
            best = database.get_personal_best(player_id) if player_id else 0

        next_action = 'retry'
        while next_action == 'retry': #запуск игры
            score, level = Game(surface, settings, player_id, best).run()
            if score > best: #обновление рекорда
                best = score
            if DB_OK and player_id:  #если база работает И игрок существует
                database.save_session(player_id, score, level) #сохранение в БД
            next_action = screen_gameover(surface, clock, score, level, best)

if __name__ == "__main__":
    main()