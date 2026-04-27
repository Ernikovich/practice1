# загрузка и сохранение настроек из settings.json

import json
import os

SETTINGS_FILE = "settings.json" # где хранятся настройки

DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 80],   # RGB
    "grid_overlay": False,
    "sound":        False,
}


def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE): #если файл есть читаем     нет → используем дефолт
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f) # превращает JSON → Python dict
            # Подставляем дефолты для отсутствующих ключей
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except Exception as e:
            print(f"[Settings] load error: {e}")
    return DEFAULT_SETTINGS.copy() # если ошибка


def save_settings(settings: dict): # сохранение настроек
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)  # превращает dict → JSON файл
    except Exception as e:
        print(f"[Settings] save error: {e}")