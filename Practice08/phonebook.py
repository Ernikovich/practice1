from connect import connect

def search_contact(pattern):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

def upsert_contact(first_name, last_name, phone):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s);", (first_name, last_name, phone))
        conn.commit()
    finally:
        conn.close()

def delete_contact(first_name, last_name):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s, %s);", (first_name, last_name))
        conn.commit()
    finally:
        conn.close()
        
if __name__ == "__main__":
    while True:
        print("\n📒 Phonebook Menu")
        print("1. Search contact")
        print("2. Add/Update contact")
        print("3. Delete contact")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            pattern = input("Enter search pattern: ")
            print(search_contact(pattern))
        elif choice == "2":
            first = input("First name: ")
            last = input("Last name: ")
            phone = input("Phone: ")
            upsert_contact(first, last, phone)
        elif choice == "3":
            first = input("First name: ")
            last = input("Last name: ")
            delete_contact(first, last)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice") 
