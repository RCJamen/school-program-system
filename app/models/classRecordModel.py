from app import mysql

class Student:
    def __init__(self, student_id, last_name, first_name):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name

def get_all_students():
    # Assuming you have a cursor set up for your MySQL connection
    cursor = mysql.connection.cursor()

    # Assuming you have a 'students' table in your database
    cursor.execute("SELECT * FROM students")

    # Fetch all rows
    students_data = cursor.fetchall()

    # Convert data to a list of Student objects
    students = [Student(student_id=row['student_id'], last_name=row['last_name'], first_name=row['first_name'])
                for row in students_data]

    # Close the cursor
    cursor.close()

    return students
