import psycopg2
from config import load_config #твоя функция, которая читает database.ini

def connect():
    try:
        config = load_config() 
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL")
            return conn
    except Exception as e:
        print(" Connection failed:", e)


if __name__ == "__main__":
    connect()

# with ... as conn
# создаёт соединение
# автоматически управляет ресурсами

# psycopg2.connect(**config)
# Это “распаковка словаря