# COMP 3005 – Assignment 3, Question 1

**Name:** Manit Singh
**Student number:** 101360267

## Project structure

```
.
├── sql/
│   └── schema.sql      # creates the students table and inserts the initial data
├── app.py              # Python console app (connection, CRUD functions, menu)
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## Setup

1. **Install Python 3** (3.8 or newer).

2. **Install the dependencies** from the project folder with the following command:

   pip install -r requirements.txt

3. **Create the database and table in pgAdmin:**
   - Make sure PostgreSQL is running and connect to your server in pgAdmin.
   - Create a database (for example `Assignment3`).
   - Right-click the database, choose **Query Tool**, open `sql/schema.sql`, and run it.
   - The `students` table is created with the three initial students.
     The script starts with `DROP TABLE IF EXISTS`, so running it again resets the table.

4. **Create a `.env` file** in the project folder (next to `app.py`) with your connection details:

   ```
   DB_HOST=
   DB_PORT=
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   ```

   | Variable | Description |
   |---|---|
   | `DB_HOST` | Server address, e.g. `localhost` |
   | `DB_PORT` | PostgreSQL port, usually `5432` |
   | `DB_NAME` | Name of the database where you ran `schema.sql` |
   | `DB_USER` | PostgreSQL username |
   | `DB_PASSWORD` | Password for that user |

   `.env` is listed in `.gitignore`, so the password is never committed.

## How to run

Run with the following command:
python app.py

The app shows a menu:

| Option | What it does |
|---|---|
| `1` | Show all students (`get_all_students`) |
| `2` | Add a student: asks for first name, last name, email and enrollment date in `YYYY-MM-DD` format (blank for none) (`add_student`) |
| `3` | Update a student's email by id (`update_student_email`) |
| `4` | Delete a student by id (`delete_student`) |
| `0` | Exit |

Errors are handled with a clear message instead of crashing: duplicate email,
student id that does not exist, non-numeric id, invalid date, and a failed
database connection. Each successful change is committed; failed ones are rolled back.

## Table schema

| Column | Type | Constraints |
|---|---|---|
| `student_id` | `SERIAL` (integer) | Primary key, auto-increment |
| `first_name` | `TEXT` | Not null |
| `last_name` | `TEXT` | Not null |
| `email` | `TEXT` | Not null, unique |
| `enrollment_date` | `DATE` | Nullable |

## Demo video

Video link: https://youtu.be/YwNyd6GIw9Q
