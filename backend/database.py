import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="examdb",#examdb
        user="postgres",
        password="12345",  # wie in db.py
        host="localhost",
        port="5432"
    )
    return conn

