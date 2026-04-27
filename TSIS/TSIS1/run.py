# run_sql.py
# Запускает SQL файлы через Python — не нужен psql в командной строке.
# Использование: python run_sql.py

import psycopg2
from connect import connect

def run_sql_file(filename):
    conn = connect()
    try:
        with conn.cursor() as cur:
            with open(filename, "r", encoding="utf-8") as f:
                sql = f.read()
                cur.execute(sql)
        conn.commit()
        print(f"  ✅ {filename} — выполнен успешно")
    except Exception as e:
        print(f"  ❌ {filename} — ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Инициализация базы данных...\n")
    run_sql_file("schema.sql")      # сначала таблицы
    run_sql_file("procedures.sql")  # потом процедуры
    print("\n✅ База данных готова! Теперь запускай: python phonebook.py")