from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from app.controller.admin.controller import login_is_required
from app.models.classRecordModel import ClassRecord
from app.controller.classRecord.forms import classRecordForm
from app.controller.classRecord.forms import gradeDistributionForm

from . import classRecord

def classRecord_route(rule, **options):
    def decorator(f):
        @classRecord.route(rule, **options)
        @login_is_required
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator

@classRecord.route('/class_record/<string:subject_code>/<string:description>/<string:section_code>/<string:credits>/<string:sem>/<string:school_year>', methods =['GET', 'POST'])
def index(subject_code, section_code, description, credits ,sem, school_year):
    ClassDetails = [subject_code, description, section_code, credits, sem, school_year]
    ClassRecord.createClassRecordTable(subject_code, section_code, school_year, sem)
    ClassRecord.createGradeDistributionTable(subject_code, section_code, school_year, sem)
    Students = ClassRecord.getStudents(subject_code, section_code, school_year, sem)
    GradeDistributions = ClassRecord.getGradeDistribution(subject_code, section_code, school_year, sem)
    session['ClassDetails'] = ClassDetails
    flash_message = session.pop('flash_message', None)
    return render_template("class-record.html", ClassDetails=ClassDetails, Students=Students, GradeDistributions= GradeDistributions, flash_message=flash_message)

@classRecord.route("/class_record/create_student", methods=['POST','GET'])
def create_student():
    form = classRecordForm(request.form)
    ClassDetails = session.get('ClassDetails', None)
    subject_code, description, section_code, credits, sem, school_year = ClassDetails

    if request.method == "POST" and form.validate():
        studentID = form.studentID.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        coursecode = form.coursecode.data
        email = form.email.data

        result = ClassRecord.addStudent(subject_code, section_code, school_year, sem, studentID, firstname, lastname, coursecode, email)
        if "success" in result:
            credentials_message = f"<br>Student ID: <strong>{studentID}</strong><br>First Name: <strong>{firstname}</strong><br> Last Name: <strong>{lastname}</strong><br>Course Code: <strong>{coursecode}</strong><br>Email: <strong>{email}</strong>"
            flash_message = {"type": "success", "message": f"Subject created successfully:{credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"Failed to create Subject: {result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", subject_code=subject_code, description=description, section_code=section_code, credits=credits, sem=sem, school_year=school_year, message=flash_message))
    else:
        flash_message = {"type": "danger", "message": f"Failed to create Student. Please check the form for errors in the following:<br>* Student ID must be XXXX-XXXX<br>* Does not Accept Numericals in First Name and Last Name<br>* Only Accepts MSU-IIT Google Email"}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", subject_code=subject_code, description=description, section_code=section_code, credits=credits, sem=sem, school_year=school_year, message=flash_message))


@classRecord.route("/class_record/delete_student/<string:studentID>", methods=['POST'])
def delete_student(studentID):
    try:
        ClassDetails = session.get('ClassDetails', None)
        subject_code, description, section_code, credits, sem, school_year = ClassDetails
        result = ClassRecord.deleteStudent(subject_code, section_code, school_year, sem, studentID)
        flash_message = {"type": "success", "message": f"{result}"}
        session['flash_message'] = flash_message
        return jsonify({'success': True, 'message': 'Student deleted successfully', 'flash_message': flash_message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@classRecord.route("/grade_distribution/create_grade_distribution", methods=['POST','GET'])
def create_grade_distribution():
    form = gradeDistributionForm(request.form)
    ClassDetails = session.get('ClassDetails', None)
    subject_code, description, section_code, credits, sem, school_year = ClassDetails

    if request.method == "POST" and form.validate():
        name = form.name.data
        percentage = form.percentage.data

        result = ClassRecord.addGradeDistribution(subject_code, section_code, school_year, sem, name, percentage)
        if "success" in result:
            credentials_message = f"<br>Name: <strong>{name}</strong><br>Percentage: <strong>{percentage}</strong>"
            flash_message = {"type": "success", "message": f"Assessment Created successfully:{credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"Failed to create Assessment: {result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", subject_code=subject_code, description=description, section_code=section_code, credits=credits, sem=sem, school_year=school_year, message=flash_message))
    else:
        flash_message = {"type": "danger", "message": f"Failed to Add Assessment.<br>*  Make Sure Percentage will equate to 100%"}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", subject_code=subject_code, description=description, section_code=section_code, credits=credits, sem=sem, school_year=school_year, message=flash_message))