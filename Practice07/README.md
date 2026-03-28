# PhoneBook App (Python + PostgreSQL)

A simple educational project demonstrating how to build a CRUD (Create, Read, Update, Delete) application using Python and PostgreSQL.  
The app manages a phonebook database and includes examples of inserting, selecting, updating, and deleting contacts.

---

## 📂 Project Structure
- `config.py` — loads database connection parameters from `database.ini`
- `database.ini` — configuration file with PostgreSQL credentials
- `connect.py` — tests connection to the database
- `create_table.py` — creates the `phonebook` table
- `insert.py` — inserts a single contact
- `insert_console.py` — inserts a contact via console input
- `insert_csv.py` — inserts contacts from a CSV file
- `select.py` — retrieves contacts (fetchone, fetchall, fetchmany)
- `update.py` — updates existing contacts
- `delete.py` — deletes contacts by ID
- `data.csv` — sample CSV file with contacts
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

---

## ⚙️ Requirements
- Python 3.10+
- PostgreSQL 18+
- psycopg2 library

Install dependencies:
```bash
pip install -r requirements.txt
