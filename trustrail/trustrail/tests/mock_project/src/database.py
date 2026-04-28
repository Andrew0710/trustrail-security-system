# Database connection
import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="secretpassword123"
    )
    return conn
