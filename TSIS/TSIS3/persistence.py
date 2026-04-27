import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal"
}

# Settings 

def load_settings():
    if os.path.exists(SETTINGS_FILE): # если файл есть читаем
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f) # превращает файл в словарь Python
                # esли в старом файле нет новых настроек →добавляем дефолт
                for k, v in DEFAULT_SETTINGS.items():
                    data.setdefault(k, v)
                return data
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict): #сохраняет настройки игры в файл
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2) # записываем данные

#  Leaderboard 

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE): # если файла нет → сразу вернём пустой список
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f) # превращаем JSON в Python
        except Exception:
            pass
    return []

def save_score(name: str, score: int, distance: int, coins: int):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": distance, "coins": coins})
    lb.sort(key=lambda x: x["score"], reverse=True) # сортировка по очкам от большего к меньшему
    lb = lb[:10]  # оставляем только топ-10
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f, indent=2) #записываем обновлённый список обратно
    return lb