import psycopg2
from connect import connect

def run_sql_file(filename):
    conn = connect()
    try:
        with conn.cursor() as cur:
            with open(filename, "r") as f:
                sql = f.read()
                cur.execute(sql)
            conn.commit()
            print("✅ SQL file executed successfully")
    finally:
        conn.close()

if __name__ == "__main__":
    run_sql_file("procedures.sql")
