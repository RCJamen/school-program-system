
from flask import Blueprint, render_template
from app.models.classRecordModel import Student
from app import mysql 

classRecord = Blueprint('classRecord', __name__)

@classRecord.route('/class-record')
def show_class_record():

    conn = mysql.connection
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("SELECT * FROM class_records")
        students = cursor.fetchall()
    except Exception as e:

        print(f"Error fetching data from the database: {e}")
        students = []


    cursor.close()

    return render_template('class-record.html', students=students)
