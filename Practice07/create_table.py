import psycopg2
from config import load_config

def create_tables():
    """ Create phonebook table in PostgreSQL """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE NOT NULL
        )
        """,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:   
            with conn.cursor() as cur: 
                for command in commands:
                    cur.execute(command) 
            print("Table 'phonebook' created successfully")
    except (psycopg2.DatabaseError, Exception) as error:
        print(" Error:", error)

if __name__ == '__main__':
    create_tables()

