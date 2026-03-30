import psycopg2
from config import load_config

def create_tables():
    """ Create phonebook table in PostgreSQL """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE NOT NULL
        )
        """,
    )
    try:
        config = load_config() #загружает параметры подключения из файла database.ini
        with psycopg2.connect(**config) as conn:   #устанавливает соединение с PostgreSQL.
            with conn.cursor() as cur: #создаёт курсор для выполнения SQL‑команд.
                for command in commands:
                    cur.execute(command) #выполняет SQL‑команду (создание таблицы).  Курсор отправляет команду в базу.
            print("✅ Table 'phonebook' created successfully")
    except (psycopg2.DatabaseError, Exception) as error:
        print("❌ Error:", error)

if __name__ == '__main__':
    create_tables()


# Курсор — это объект,
# который создаётся внутри соединения с 
# базой данных и служит «инструментом 
# общения» между твоим Python‑кодом и PostgreSQ

# Благодаря with соединение автоматически закроется, когда мы выйдем из блока (даже если произойдёт ошибка).
# Это защита от утечек ресурсов: не нужно вручную писать conn.close().
# Курсор — это инструмент, через который отправляются SQL‑команды и получаются результаты.

# Благодаря with курсор тоже автоматически закроется после выхода из блока.
# 👉 Это защита от ошибок: не нужно вручную писать cur.close().