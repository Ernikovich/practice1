import psycopg2
from config import load_config

def insert_contact(first_name, last_name, phone):
    """ Insert a new contact into the phonebook table """
    sql = """INSERT INTO phonebook(first_name, last_name, phone)
             VALUES(%s, %s, %s) RETURNING id;"""
    contact_id = None
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone))
                rows = cur.fetchone()
                if rows:
                    contact_id = rows[0]
                conn.commit()
                print(f"✅ Contact inserted with id {contact_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)

    return contact_id


def insert_many_contacts(contact_list):
    """ Insert multiple contacts into the phonebook table """
    sql = """INSERT INTO phonebook(first_name, last_name, phone)
             VALUES(%s, %s, %s)"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, contact_list)
            conn.commit()
            print("✅ Multiple contacts inserted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)


if __name__ == '__main__':
    # Вставка одной записи
    insert_contact("John", "Doe", "123456789")

    # Вставка нескольких записей
    insert_many_contacts([
        ("Alice", "Smith", "987654321"),
        ("Bob", "Johnson", "555555555"),
        ("Charlie", "Brown", "111222333")
    ])
