import os

import psycopg2
from dotenv import load_dotenv

# Load DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD from the .env file
load_dotenv()


def connect():
    # Open a connection to PostgreSQL, or return None if it fails
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        return None


def get_all_students(conn):
    # Read every row from the students table, ordered by id
    with conn.cursor() as cur:
        cur.execute(
            "SELECT student_id, first_name, last_name, email, enrollment_date "
            "FROM students ORDER BY student_id"
        )
        rows = cur.fetchall()

    if not rows:
        print("No students found.")
        return

    print(f"{'ID':<4} {'First':<12} {'Last':<12} {'Email':<28} {'Enrolled'}")
    for student_id, first, last, email, enrolled in rows:
        print(f"{student_id:<4} {first:<12} {last:<12} {email:<28} {enrolled or ''}")


if __name__ == "__main__":
    conn = connect()
    if conn:
        get_all_students(conn)
        conn.close()
