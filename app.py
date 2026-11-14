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


if __name__ == "__main__":
    conn = connect()
    if conn:
        print("Connected to the database.")
        conn.close()
