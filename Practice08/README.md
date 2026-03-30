Practice08 — Phonebook with PostgreSQL and Python
🔹 Overview
This project implements a simple Phonebook application using:

PostgreSQL as the database

SQL functions and procedures for search, insert/update (upsert), and delete operations

Python (psycopg2) for database interaction

It demonstrates how to combine SQL logic with Python scripts to build a small but functional CRUD application.

🔹 Project Structure
Practice08/
├── phonebook.py       # Main script to interact with the phonebook
├── functions.sql      # SQL functions (e.g., search by pattern)
├── procedures.sql     # SQL procedures (insert/update/delete)
├── config.py          # Loads connection parameters from database.ini
├── connect.py         # get_connection() function for PostgreSQL connection
└── database.ini       # Database connection settings (host, dbname, user, password)
🔹 Setup
Install dependencies:

bash
pip install psycopg2
Create a database.ini file with your PostgreSQL credentials:

ini
[postgresql]
host=localhost
database=phonebook_db
user=postgres
password=your_password

🔹 Features
Search contacts by name pattern (get_contacts_by_pattern)

Add or update contacts (upsert_contact)

Delete contacts (delete_contact)

🔹 Example Usage
Inside phonebook.py you can call:

upsert_contact("Bob", "Marley", "+77771234567")
print(search_contact("Bob"))
delete_contact("Bob", "Marley")
Or run the script directly to use an interactive menu.

🔹 Interactive Menu (optional)
You can extend phonebook.py with a console menu:

📒 Phonebook Menu
1. Search contact
2. Add/Update contact
3. Delete contact
4. Exit
This makes the phonebook behave like a small CLI application.