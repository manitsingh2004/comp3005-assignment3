DROP TABLE IF EXISTS students;

-- Students table (SERIAL gives an auto-incrementing id)
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Initial data
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('Manit', 'Singh', 'manit.singh@mail.com', '2026-09-01'),
('Matt', 'Smith', 'matt.smith@mail.com', '2026-09-01'),
('Bill', 'Xie-li', 'billy.xl@mail.com', '2026-09-02');
