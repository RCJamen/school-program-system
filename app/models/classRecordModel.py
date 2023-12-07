from app import mysql

class ClassRecordModel:
    def __init__(self, classRecordno, student_id, last_name, first_name, email):
        self.classRecordno = classRecordno
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.email = email

# def get_all_students():
#     cursor = mysql.connection.cursor()

#     cursor.execute("SELECT * FROM class_records")

#     students_data = cursor.fetchall()
#     students = [Student(classRecordno=row['classRecordno'], student_id=row['student_id'],
#                         last_name=row['last_name'], first_name=row['first_name'], email=row['email'])
#                 for row in students_data]

#     cursor.close()

#     return students
