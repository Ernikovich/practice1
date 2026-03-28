import psycopg2
from config import load_config

def get_one_contact():
    """ Получить одну запись из phonebook (fetchone) """
    sql = "SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                row = cur.fetchone()
                while row is not None:
                    print(row)
                    row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)


def get_all_contacts():
    """ Получить все записи из phonebook (fetchall) """
    sql = "SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                print("📋 Всего контактов:", cur.rowcount)
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)


def get_contacts_batch(size=2):
    """ Получить данные порциями (fetchmany) """
    sql = "SELECT id, first_name, last_name, phone FROM phonebook ORDER BY id"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                while True:
                    rows = cur.fetchmany(size)
                    if not rows:
                        break
                    for row in rows:
                        print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)


if __name__ == "__main__":
    print("🔎 Один контакт:")
    get_one_contact()

    print("\n📋 Все контакты:")
    get_all_contacts()

    print("\n📦 Контакты порциями:")
    get_contacts_batch(2)
