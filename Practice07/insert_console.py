import psycopg2
from config import load_config

def insert_contact_console():
    """ Вставка контакта через консольный ввод """
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    phone = input("Введите телефон: ")

    sql = """INSERT INTO phonebook(first_name, last_name, phone)
             VALUES(%s, %s, %s) RETURNING id;"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone))
                contact_id = cur.fetchone()[0] 
            conn.commit()  
            print(f" Contact inserted with id {contact_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(" Error:", error)

if __name__ == "__main__":
    insert_contact_console()
