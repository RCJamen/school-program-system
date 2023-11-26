from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import classRecord
from app.controller.admin.controller import login_is_required

@classRecord.route("/class-record")
@login_is_required
def class_record():

    subject_code = request.args.get('subject_code')
    section_code = request.args.get('section_code')

    # Pass the data to the template
    return render_template('class-record.html', subject_code=subject_code, section_code=section_code)

@classRecord.route('/api/students')
def get_students():
    # Fetch students data from the database (you need to implement this)
    # Example: Fetch data using a database cursor
    # data = fetch_data_from_database()
    data = [
        {'id': 1, 'studentId': '2019-2093', 'lastname': 'Jamen','firstname': 'Ramel Cary'},
        {'id': 1, 'studentId': '2019-2093', 'lastname': 'Jamen', 'firstname': 'Ramel Cary'},
        # Add more student data as needed
    ]
    return jsonify(data)
# @classRecord.route("/class-record/add")
# @login_is_required
# def add_class_record():
#     # codes here 
#     return 