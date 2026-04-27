import pygame, sys, random
from racer import Player, Enemy, Coin, Obstacle, NitroStrip, PowerUp, Background, LANE_CENTERS, SCREEN_WIDTH, SCREEN_HEIGHT, asset
from ui import main_menu, username_screen, settings_screen, game_over_screen, leaderboard_screen
from persistence import load_settings, save_score

# Init 
pygame.init()
pygame.mixer.init()
SURF  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RACER 3")
CLOCK = pygame.time.Clock()

# Sounds 
try:
    crash_sound = pygame.mixer.Sound(asset("sounds/crash.wav"))
except:
    crash_sound = None

def set_music(sound_on):
    try:
        pygame.mixer.music.set_volume(0.5 if sound_on else 0.0) # если звук включён 0.5 = половина громкости
    except: pass

def play_music(sound_on):
    try:
        pygame.mixer.music.load(asset("sounds/background.wav"))
        pygame.mixer.music.play(-1) # бесконечный цикл
        set_music(sound_on)
    except: pass

ACCENT  = (255, 200,  40) # жёлтый
ACCENT2 = (80,  180, 255) #голубой
RED     = (220,  50,  50)
GREY    = (130, 140, 160)
WHITE   = (240, 240, 255)
PU_COL  = {"nitro": (255,200,0), "shield": (80,180,255), "repair": (80,220,80)}

DIFF = {
    "easy": {"base_speed": 4, "enemy_interval": 2200, "obs_interval": 3000, "pu_interval": 6000},
    "normal": {"base_speed": 5, "enemy_interval": 1600, "obs_interval": 2200, "pu_interval": 7000},
    "hard": {"base_speed": 7, "enemy_interval": 1000, "obs_interval": 1500, "pu_interval": 9000},
}

font_hud = pygame.font.SysFont("Consolas", 17, bold=True) #берёт системный шрифт компьютера

# HUD Head-Up Display интерфейс в игре, который показывает важные данные
def draw_hud(surf, score, coins, distance, hp, pu, pu_left):
    pygame.draw.rect(surf, (10, 12, 24), (0, 0, SCREEN_WIDTH, 52)) # панель интерфейса
    pygame.draw.line(surf, ACCENT, (0, 52), (SCREEN_WIDTH, 52), 1) # тонкая линия отделяет интерфейс от игры
    surf.blit(font_hud.render(f"Score {score}", True, ACCENT),       (8,  6))
    surf.blit(font_hud.render(f"Coins {coins}", True, (255,215,0)),  (8, 28))
    surf.blit(font_hud.render(f"{distance}m",   True, ACCENT2),      (200, 6))
    for i in range(3): # рисует 3 сердечка
        pygame.draw.circle(surf, RED if i < hp else GREY, (290 + i*28, 18), 10) #если i < hp → красное иначе → серое
    if pu: #если активен бонус 
        label = f"{pu.upper()} {pu_left:.1f}s" if pu_left > 0 else pu.upper() #  показывает либо название бонуса с оставшимся временем, либо только название
        s = font_hud.render(label, True, PU_COL.get(pu, WHITE))
        surf.blit(s, s.get_rect(center=(SCREEN_WIDTH // 2, 38)))

# спавнер объектов + сразу регистрирует
def spawn(cls, group, all_sprites, **kw):
    obj = cls(**kw) # вызывает класс передаёт параметры
    group.add(obj)
    all_sprites.add(obj)
    return obj

def spawn_enemy(enemies, all_sprites, speed, player):
    e = Enemy(speed=speed)
    for _ in range(5): # защита от несправедливого спавна
        if abs(e.rect.centerx - player.rect.centerx) > 60: break #если расстояние > 60 → ок
        e.rect.centerx = random.choice(LANE_CENTERS) #если слишком близко меняем полосу
    enemies.add(e) # участвует в логике
    all_sprites.add(e) #рисуется на экране

# Game loop 
def run_game(username, settings):
    p = DIFF[settings.get("difficulty", "normal")]
    speed = base = p["base_speed"]
    bg = Background() #создаём объекты
    player = Player(car_color=settings.get("car_color", "red"))

    enemies = pygame.sprite.Group()
    coins_g = pygame.sprite.Group()
    obs_g= pygame.sprite.Group()
    strips= pygame.sprite.Group()
    pups = pygame.sprite.Group()
    all_spr = pygame.sprite.Group(player)

    # переменные игры
    score = coins = distance = 0
    hp = 3
    active_pu = None
    pu_end    = 0
    
     #  таймеры 
    E, C, O, S, P, D = [pygame.USEREVENT + i for i in range(1, 7)]
    pygame.time.set_timer(E, p["enemy_interval"]) # каждые X миллисекунд → создаётся событие E
    pygame.time.set_timer(C, 1200)
    pygame.time.set_timer(O, p["obs_interval"])
    pygame.time.set_timer(S, 5000)
    pygame.time.set_timer(P, p["pu_interval"])
    pygame.time.set_timer(D, 8000)

    sound_on = settings.get("sound", True) # берёт настройку звука
    set_music(sound_on) # применяет её (включает или выключает музыку)

    def hit(sound=True):
        nonlocal hp
        if sound and sound_on and crash_sound: crash_sound.play()
        hp -= 1

    running = True
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get(): #сам создаёт события и кладёт их в очередь
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == E:
                spawn_enemy(enemies, all_spr, speed, player)
            elif event.type == C:
                spawn(Coin, coins_g, all_spr, speed=speed)
            elif event.type == O:
                spawn(Obstacle,  obs_g,   all_spr, speed=speed)
            elif event.type == S:
                spawn(NitroStrip, strips, all_spr, speed=speed)
            elif event.type == P: 
                #если НЕТ других power-up на экране чтобы не было спама бонусов
                if not pups: spawn(PowerUp, pups, all_spr, kind=random.choice(["nitro","shield","repair"]), speed=speed)
            elif event.type == D: # Усложнение игры каждые 8 секунд
                speed = min(speed + 0.5, base + 8)
                pygame.time.set_timer(E, max(500, p["enemy_interval"] - int((speed-base)*100))) #ускоряем спавн врагов

        now = pygame.time.get_ticks() # сколько миллисекунд прошло с запуска игры

        # проверка: закончился ли бонус
        if active_pu and now >= pu_end:
            if active_pu == "nitro": 
                player.nitro_mult, player.nitro_active = 1.0, False
            elif active_pu == "shield": 
                player.shield_active = False
            active_pu = None
        pu_left = max(0.0, (pu_end - now) / 1000) if active_pu else 0.0

        # Update
        player.move(speed / 5.0) # движение игрока
        for g in (enemies, coins_g, obs_g, strips, pups):  #обновление всех объектов
            g.update()
        bg.update(speed)
        distance = int(distance + speed * 0.05)
        score    = distance + coins * 10

        # Collisions — coins
        for c in pygame.sprite.spritecollide(player, coins_g, True):
            coins += c.value

        # Collisions — power-ups
        for pu in pygame.sprite.spritecollide(player, pups, True):
            active_pu = pu.kind
            if   pu.kind == "nitro": 
                player.nitro_mult, player.nitro_active, pu_end = 1.6, True, now+4000
            elif pu.kind == "shield":
                player.shield_active, pu_end = True, now+999999
            elif pu.kind == "repair":
                hp, active_pu = min(3, hp+1), None

        # Collisions — nitro strip
        if pygame.sprite.spritecollide(player, strips, True) and active_pu != "nitro":
            player.nitro_mult, player.nitro_active = 1.4, True #включение эффекта скорость игрока × 1.4
            active_pu, pu_end = "nitro", now + 2000 #через 2000 мс (2 секунды) закончится

        # Collisions — enemies
        if pygame.sprite.spritecollide(player, enemies, True):
            if player.shield_active:
                player.shield_active = active_pu = None  # если есть щит
            else: hit(); running = hp > 0

        # Collisions — obstacles
        for obs in pygame.sprite.spritecollide(player, obs_g, True):
            if player.shield_active: 
                player.shield_active = active_pu = None  #если есть щит
            elif obs.kind == "oil":
                player.nitro_mult, active_pu, pu_end = 0.5, "nitro", now+1500 #бонус “обратный нитро” временное замедление/эффект нитро длится 1.5 сек
            else:
                hit()
                running = hp > 0 #если HP = 0 → игра заканчивается

        # Draw
        bg.draw(SURF) #рисуется дорога/фон
        for spr in all_spr: #все объекты кроме игрока
            if spr is not player: SURF.blit(spr.image, spr.rect)
        player.draw(SURF) #игрок рисуется последним
        draw_hud(SURF, score, coins, distance, hp, active_pu, pu_left) #интерфейс
        pygame.display.flip()

    for evt in (E, C, O, S, P, D):  #очистка перед выходом
        pygame.time.set_timer(evt, 0) #останавливаем все игровые события:
    return {"score": score, "distance": distance, "coins": coins} #игра закончилась → отдаём статистику

# App 
def main():
    settings = load_settings() # читается файл настроек
    play_music(settings.get("sound", True))
    username = None # игрок ещё не ввёл имя

    while True:
        choice = main_menu(SURF, CLOCK)
        if   choice == "quit":
             pygame.quit()
             sys.exit()
        elif choice == "leaderboard":
            leaderboard_screen(SURF, CLOCK)
        elif choice == "settings":
            new = settings_screen(SURF, CLOCK, settings) # пользователь меняет настройки
            if new.get("sound") != settings.get("sound"): # если звук поменялся → обновляем музыку
                set_music(new["sound"])
            settings = new # cохраняем настройки в память
        elif choice == "play":
            if not username: username = username_screen(SURF, CLOCK)
            while True:
                r = run_game(username, settings)
                save_score(username, r["score"], r["distance"], r["coins"]) # получаем результат:
                if game_over_screen(SURF, CLOCK, r["score"], r["distance"], r["coins"]) == "menu": # если нажали “menu” → выходим в главное меню
                    break

if __name__ == "__main__":
    main()