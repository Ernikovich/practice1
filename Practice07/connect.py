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
# def check_tables():
#     config = load_config() # Загружаем параметры подключения (host, dbname, user, password, port)
#     conn = psycopg2.connect(**config)     # Устанавливаем соединение с PostgreSQL
#     cur = conn.cursor()   # Создаём курсор для выполнения SQL-запросов
    #   Курсор отправляет SQL‑команду в базу данных.
#     cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
#     rows = cur.fetchall() # Забираем все строки результата
#     for row in rows:
#         print(row)
#     cur.close()
#     conn.close()

if __name__ == "__main__":
    connect()
    # check_tables()