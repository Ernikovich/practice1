import psycopg2
import csv
from config import load_config

def insert_contacts_from_csv(filename):

    sql = """INSERT INTO phonebook(first_name, last_name, phone)
             VALUES(%s, %s, %s)"""
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r') as f:
                    reader = csv.DictReader(f) 
                    for row in reader:
                        cur.execute(sql, (row['first_name'], row['last_name'], row['phone'])) 
            conn.commit()
            print("Contacts inserted from CSV successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(" Error:", error)

if __name__ == "__main__":
    insert_contacts_from_csv("data.csv")
# DictReader превращает каждую строку CSV в словарь.