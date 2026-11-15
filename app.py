import os
from datetime import date

import psycopg2
from psycopg2 import errors
from dotenv import load_dotenv

# Load DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD from the .env file
load_dotenv()


def connect():
    # Open a conection to PostgreSQL, or return None if it fails
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


def add_student(conn, first_name, last_name, email, enrollment_date):
    # Insert a new student; %s placeholders keep user input out of the SQL text
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        print(f"Added student with id {new_id}.")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"Error: the email '{email}' is already in use.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: could not add student ({e.pgerror or e}).")


def update_student_email(conn, student_id, new_email):
    # Change the email of one student
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s",
                (new_email, student_id),
            )
            # rowcount is 0 when no studnet has this id
            if cur.rowcount == 0:
                conn.rollback()
                print(f"Error: no student with id {student_id}.")
                return
        conn.commit()
        print(f"Updated email for student {student_id}.")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"Error: the email '{new_email}' is already in use.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: could not update email ({e.pgerror or e}).")


def delete_student(conn, student_id):
    # Remove one student by id
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            # rowcount is 0 when no student has this id
            if cur.rowcount == 0:
                conn.rollback()
                print(f"Error: no student with id {student_id}.")
                return
        conn.commit()
        print(f"Deleted student {student_id}.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: could not delete student ({e.pgerror or e}).")


def ask_required(prompt):
    # Keep asking untill the user types something (name and email are NOT NULL)
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")


def ask_id(prompt):
    # Return the id as an int, or None if it is not a number
    value = input(prompt).strip()
    if not value.isdigit():
        print("Error: student id must be a whole number.")
        return None
    return int(value)


def ask_date(prompt):
    # Blank means no date; otherwise it must be YYYY-MM-DD
    while True:
        value = input(prompt).strip()
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Error: invalid date, use YYYY-MM-DD (e.g. 2023-09-01).")


def menu(conn):
    # Simple numbered menu so each function can be demoed
    while True:
        print("\n--- Student Menu ---")
        print("1. Show all students")
        print("2. Add a student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            get_all_students(conn)
        elif choice == "2":
            first = ask_required("First name: ")
            last = ask_required("Last name: ")
            email = ask_required("Email: ")
            enrolled = ask_date("Enrollment date (YYYY-MM-DD, blank for none): ")
            add_student(conn, first, last, email, enrolled)
        elif choice == "3":
            student_id = ask_id("Student id: ")
            if student_id is not None:
                new_email = ask_required("New email: ")
                update_student_email(conn, student_id, new_email)
        elif choice == "4":
            student_id = ask_id("Student id: ")
            if student_id is not None:
                delete_student(conn, student_id)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option, choose 0-4.")


if __name__ == "__main__":
    conn = connect()
    if conn:
        try:
            menu(conn)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
        finally:
            conn.close()
