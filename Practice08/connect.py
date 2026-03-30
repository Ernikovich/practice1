import psycopg2
from config import load_config

def connect():
    try:
        config = load_config() # загружаем параметры подключения из database.ini
        with psycopg2.connect(**config) as conn:# устанавливаем соединение
            print("✅ Connected to PostgreSQL")
            return conn
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    connect()