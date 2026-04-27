import json
import csv
from connect import connect

def print_rows(rows):
    if not rows:
        print("No results")
        return
    for r in rows:
        print(r)

def search_all():
    q = input("Search: ")
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        print_rows(cur.fetchall())
    conn.close()
    # cur.fetchall() забирает все результаты из PostgreSQL

def filter_by_group():
    conn = connect() #открываем соединение с PostgreSQL
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY name")
        groups = cur.fetchall()

    print("Groups:")
    for gid, gname in groups:
        print(f"  {gid}. {gname}")

    choice = input("Enter group name or id: ")

    with conn.cursor() as cur:
        if choice.isdigit():
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, g.name
                FROM contacts c
                JOIN groups g ON c.group_id = g.id
                WHERE g.id = %s
            """, (int(choice),))
        else:
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, g.name
                FROM contacts c
                JOIN groups g ON c.group_id = g.id
                WHERE g.name ILIKE %s
            """, (choice,))
        print_rows(cur.fetchall())
    conn.close()

#     cur.execute(query, params)
#     query (обязательный аргумент)
#     params (необязательный) это данные, которые вставляются в %s

def search_by_email():
    email = input("Email fragment: ")
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT first_name, last_name, email
            FROM contacts
            WHERE email ILIKE %s
        """, (f"%{email}%",))
        print_rows(cur.fetchall())
    conn.close()


def list_sorted():
    print("Sort by: 1-Name  2-Birthday  3-Date added")
    choice = input(">> ")
    order = {
        "1": "first_name, last_name",
        "2": "birthday NULLS LAST", #сначала нормальные даты, потом пустые
        "3": "created_at"
    }.get(choice, "first_name")

    # если ничего не ввёл по умолчанию:first_name
    # dict.get(key, default)

    conn = connect()
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT first_name, last_name, email, birthday
            FROM contacts
            ORDER BY {order}
        """)
        print_rows(cur.fetchall())
    conn.close()


def paginated():
    offset = 0
    conn = connect()
    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (3, offset))
            rows = cur.fetchall()
        print_rows(rows)
        cmd = input("next / prev / quit: ")
        if cmd == "next":
            offset += 3
        elif cmd == "prev":
            offset = max(0, offset - 3)
        else:
            break
    conn.close()


def add_phone():
    name  = input("Contact name: ")
    phone = input("Phone number: ")
    ptype = input("Type (home/work/mobile): ")
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Phone added!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def move_group():
    name  = input("Contact name: ")
    group = input("Group name: ")
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"Moved to '{group}'!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def export_json():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email,
                   c.birthday::TEXT, g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.id
        """) 
        # c.birthday::TEXT превращаем дату в текст
        cols = [d[0] for d in cur.description]
        # cur.description 👉 это информация о колонках результата d[0] берёт только имена колонок
        contacts = [dict(zip(cols, row)) for row in cur.fetchall()]
        # превратить таблицу из кортежей в список словарей
        # было (плохо):
        # (1, "Ali", "gmail")
        # стало (удобно):
        # {"id": 1, "name": "Ali"}

        for c in contacts:
            cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (c['id'],))
            c['phones'] = [{'phone': r[0], 'type': r[1]} for r in cur.fetchall()]
            # мы добавляем телефоны к каждому контакту

    with open("contacts.json", "w", encoding="utf-8") as f: #encoding="utf-8" → чтобы нормально писать кириллицу     with автоматически закрывает файл после работы
        json.dump(contacts, f, ensure_ascii=False, indent=2) #запиши данные contacts в файл f
        # ensure_ascii=False  чтобы не ломались символы
        # без него: \u0410\u043b\u0438
        # с ним: Али
    conn.close()
    print(f"Exported {len(contacts)} contacts → contacts.json")

def import_json():
    with open("contacts.json", "r", encoding="utf-8") as f: #encoding="utf-8" → чтобы нормально читать кириллицу
        data = json.load(f) #читает JSON файл и превращает его в Python объект

    conn = connect()
    for c in data: #c — это один контакт
        with conn.cursor() as cur: #это “инструмент” для выполнения SQL
            cur.execute("SELECT id FROM contacts WHERE first_name ILIKE %s", (c['first_name'],))
            exists = cur.fetchone() #берёт одну строку результата

        if exists:
            ans = input(f"Duplicate '{c['first_name']}'. [s]kip / [o]verwrite? ")
            if ans != 'o':
                print("  Skipped")
                continue
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE contacts SET last_name=%s, email=%s, birthday=%s
                    WHERE first_name ILIKE %s RETURNING id 
                """, (c.get('last_name'), c.get('email'), c.get('birthday'), c['first_name']))
                contact_id = cur.fetchone()[0]
                cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,)) #удаляем старые телефоны
                # RETURNING id👉 возвращает id обновлённого контакта
        else: #если контакт НЕ найден в базе
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO contacts(first_name, last_name, email, birthday)
                    VALUES(%s, %s, %s, %s) RETURNING id
                """, (c['first_name'], c.get('last_name'), c.get('email'), c.get('birthday')))
                contact_id = cur.fetchone()[0]

        with conn.cursor() as cur: #после создания/обновления контакта мы добавляем ему телефоны
            for p in c.get('phones', []): #если телефонов нет → пустой список []
                cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                    (contact_id, p['phone'], p.get('type', 'mobile')))
        conn.commit()
        print(f"  Imported: {c['first_name']}")
    conn.close()


def import_csv():
    conn = connect()
    try:
        with open("contacts.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f) #каждая строка = словарь
            with conn.cursor() as cur:
                for row in reader:
                    # Найти group_id
                    group_id = None #по умолчанию у контакта нет группы
                    if row.get('group'):
                        cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (row['group'],))
                        g = cur.fetchone()
                        if g:
                            group_id = g[0]

                    cur.execute("""
                        INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                        VALUES(%s, %s, %s, %s, %s) RETURNING id
                    """, (row['first_name'], row['last_name'],
                          row.get('email'), row.get('birthday'), group_id))
                    contact_id = cur.fetchone()[0] #fetchone() даёт (10,), а [0] вытаскивает из него просто 10

                    if row.get('phone'):
                        cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                            (contact_id, row['phone'], row.get('phone_type', 'mobile')))
        conn.commit()
        print("CSV imported!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def main():
    while True:
        print("""
1. Search (name/email/phone)
2. Filter by group
3. Search by email
4. Sort
5. Pages (next/prev/quit)
6. Add phone
7. Move to group
8. Export JSON
9. Import JSON
10. Import CSV
0. Exit
""")
        c = input(">> ")
        if   c == "1":  search_all()
        elif c == "2":  filter_by_group()
        elif c == "3":  search_by_email()
        elif c == "4":  list_sorted()
        elif c == "5":  paginated()
        elif c == "6":  add_phone()
        elif c == "7":  move_group()
        elif c == "8":  export_json()
        elif c == "9":  import_json()
        elif c == "10": import_csv()
        elif c == "0":  break
        else: print("Invalid")

if __name__ == "__main__":
    main()