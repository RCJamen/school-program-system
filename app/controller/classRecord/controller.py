# app/controller/classRecord/controller.py
from flask import Blueprint, render_template
from app.models.classRecordModel import Student

classRecord_bp = Blueprint('classRecord', __name__, url_prefix='/class-record')

@classRecord_bp.route('/class-record')
def show_class_record():
    # Fetch data from the database
    students = Student.query.all()

    return render_template('class-record.html', students=students)
