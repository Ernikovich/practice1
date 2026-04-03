import psycopg2
from config import load_config

def update_contact(contact_id, new_phone):
    """ Update phone number of a contact by id """
    updated_row_count = 0
    sql = """ UPDATE phonebook
              SET phone = %s
              WHERE id = %s"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_phone, contact_id))
                updated_row_count = cur.rowcount
            conn.commit()
            print(f"Updated {updated_row_count} row(s)")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

    return updated_row_count

if __name__ == "__main__":
    update_contact(3, "777888999")  
