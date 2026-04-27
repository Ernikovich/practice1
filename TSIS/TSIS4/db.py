# работа с PostgreSQL через psycopg2

import psycopg2
import psycopg2.extras # дополнительные удобные инструменты DictCursor
from datetime import datetime

# Настройки подключения
DB_CONFIG = { 
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_db",
    "user":     "postgres",
    "password": "Koktem2008@",
    "client_encoding": "utf8",
}


def get_connection(): #каждый раз создаёт соединение с БД
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Создаёт таблицы, если их нет."""
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        return True
    except Exception as e:
        print(f"[DB] init_db error: {e}")
        return False


def get_or_create_player(username: str) -> int | None: # : что функция возвращает    int число (id игрока)   None → ничего (если ошибка)
    try:
        with get_connection() as conn:
            # открывается соединение с PostgreSQL
            # (автоматически закроется после блока)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) "
                    "ON CONFLICT (username) DO NOTHING", # если такой username уже есть
                    (username,)
                )
                cur.execute( # получить id игрока
                    "SELECT id FROM players WHERE username = %s",
                    (username,)
                )
                row = cur.fetchone() # получаем результат
                return row[0] if row else None
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        return None


def save_session(player_id: int, score: int, level: int): # сохраняет результат игры в базу данных
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) "
                    "VALUES (%s, %s, %s)",
                    (player_id, score, level)
                )
        return True # сохранение прошло успешно
    except Exception as e:
        print(f"[DB] save_session error: {e}")
        return False


def get_personal_best(player_id: int) -> int:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COALESCE(MAX(score), 0) FROM game_sessions "
                    "WHERE player_id = %s",
                    (player_id,)
                    # COALESCE(..., 0) если записей нет: вместо NULL вернёт 0
                )
                row = cur.fetchone()
                return row[0] if row else 0 # возвращаем результат
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0


def get_leaderboard(limit: int = 10) -> list[dict]: # топ игроков по очкам
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur: # DictCursor → строки будут как словари
                cur.execute(
                    """
                    SELECT p.username, gs.score, gs.level_reached,
                           gs.played_at
                    FROM game_sessions gs
                    JOIN players p ON p.id = gs.player_id
                    ORDER BY gs.score DESC
                    LIMIT %s
                    """,
                    (limit,)
                )
                rows = cur.fetchall() #берём ВСЕ строки
                return [dict(r) for r in rows] # каждый ряд превращается в словарь
    except Exception as e:
        print(f"[DB] get_leaderboard error: {e}")
        return []