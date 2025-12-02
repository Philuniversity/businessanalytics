import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="examdb",
        user="postgres",
        password="Postgres123!",  # wie in db.py
        host="localhost",
        port="5432"
    )
    return conn
