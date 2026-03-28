import psycopg2
from config import load_config

def delete_contact(contact_id):
    """ Delete a contact by id """
    sql = """DELETE FROM phonebook WHERE id = %s"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contact_id,))
            conn.commit() #Подтверждает изменения в базе (без этого удаление не сохранится).
            print(f"✅ Contact {contact_id} deleted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("❌ Error:", error)
# Exception — общий класс ошибок в Python.
# psycopg2.DatabaseError — конкретные ошибки, 
# связанные с PostgreSQL (например, нарушение уникальности, ошибка подключения, неверный запрос).
# Сохраняет объект ошибки в переменную error
if __name__ == "__main__":
    delete_contact(4)  # пример: удаляем контакт с id=4
