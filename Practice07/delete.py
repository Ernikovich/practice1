import psycopg2
from config import load_config

def delete_contact(contact_id):
    sql = """DELETE FROM phonebook WHERE id = %s"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contact_id,))
            conn.commit() 
            print(f" Contact {contact_id} deleted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(" Error:", error)

if __name__ == "__main__":
    delete_contact(4)  # пример: удаляем контакт с id=4
