from os import name
from flask import render_template, redirect, request, jsonify, flash, session, current_app, send_file
from flask.helpers import url_for
from app.controller.admin.controller import login_is_required
from app.models.classRecordModel import ClassRecord
from app.controller.classRecord.forms import classRecordForm, gradeDistributionForm, activityForm
from app.controller.classRecord.utils import Utils
from . import classRecord

def classRecord_route(rule, **options):
    def decorator(f):
        @classRecord.route(rule, **options)
        @login_is_required
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator

@classRecord.route("/<string:classrecordid>", methods =['GET', 'POST'])
def index(classrecordid):
    ClassDetails = ClassRecord.getClassRecordData(classrecordid)
    Students = Utils.sortStudent(ClassRecord.getClassRecordStudents(classrecordid))
    Assessments = ClassRecord.getGradeDistribution(classrecordid)
    # print(Assessments)
    assessmentIDs = Utils.getAssessmentID(Assessments)
    finalscores = []
    for assessment_id in assessmentIDs:
        scores_for_assessment = ClassRecord.get_student_scores(classrecordid, assessment_id)
        finalscores.extend(scores_for_assessment)

    assessment_activities = {}
    for assessment_id in assessmentIDs:
        print(assessment_id)
        # Fetch activities for the current assessment
        activities = ClassRecord.get_activities_for_assessment(assessment_id)

        assessment_activities[assessment_id] = activities

        # Print activities for debugging
        # for entry in activities:
        #     print(entry)

    # Print all activities outside the loop for debugging
    print(assessment_activities)
    flash_message = session.get('flash_message')
    session.pop('flash_message', None)
    return render_template("class-record.html", ClassRecordID=classrecordid, ClassDetails=ClassDetails, Students=Students, Assessments=Assessments, flash_message=flash_message, finalscores=finalscores, assessment_activities=assessment_activities, activities=activities)


@classRecord.route("/<string:classrecordid>/create_student", methods =['GET', 'POST'])
def create_student(classrecordid):
    form = classRecordForm(request.form)
    if request.method == "POST" and form.validate():
        studentID = form.studentID.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        coursecode = form.coursecode.data
        email = form.email.data
        result = ClassRecord.postStudentToClassRecord(classrecordid, studentID, firstname, lastname, coursecode, email)
        if "success" in result:
            credentials_message = f"<br>Student ID: <strong>{studentID}</strong><br>First Name: <strong>{firstname}</strong><br> Last Name: <strong>{lastname}</strong><br>Course Code: <strong>{coursecode}</strong><br>Email: <strong>{email}</strong>"
            flash_message = {"type": "success", "message": f"Subject created successfully:{credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"Failed to create Subject: {result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))
    else:
        flash_message = {"type": "danger", "message": f"<strong>Failed to create Student</strong><br>* Student ID must be XXXX-XXXX<br>* Does not accept numericals in First Name and Last Name<br>* Only accepts MSU-IIT google email"}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))


@classRecord.route("/<string:classrecordid>/delete_student/<string:studentID>", methods=['POST'])
def delete_student(classrecordid, studentID):
    try:
        classID = ClassRecord.getstudentclassID(classrecordid, studentID)
        result = ClassRecord.deleteStudentFromClassRecord(classrecordid, studentID, classID)
        flash_message = {"type": "success", "message": f"{result}"}
        session['flash_message'] = flash_message
        return jsonify({'success': True, 'message': 'Student deleted successfully', 'flash_message': flash_message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@classRecord.route("/<string:classrecordid>/create_grade_distribution", methods=['POST','GET'])
def create_grade_distribution(classrecordid):
    form = gradeDistributionForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        percentage = form.percentage.data
        result = ClassRecord.postGradeDistribution(classrecordid, name, percentage)
        if "success" in result:
            asessmentID = ClassRecord.getAssessmentID(classrecordid, name)
            studentsID = Utils.getClassID(ClassRecord.getClassRecordStudents(classrecordid))
            ClassRecord.postCreateFinalScore(asessmentID, studentsID)
            credentials_message = f"<br>Name: <strong>{name}</strong><br>Percentage: <strong>{percentage}</strong>"
            flash_message = {"type": "success", "message": f"Assessment Created successfully:{credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"<strong>Failed to create Assessment:</strong><br>{result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))
    else:
        flash_message = {"type": "danger", "message": f"<strong>Failed to Add Assessment</strong><br>*  Make Sure Percentage will equate to 100%<br>*  Make Sure Percentage is not Negative"}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))


@classRecord.route("/<string:classrecordid>/delete_grade_distribution/<string:assessmentname>", methods=['POST'])
def delete_grade_distribution(classrecordid, assessmentname):
    try:
        result = ClassRecord.deleteGradeDistribution(classrecordid, assessmentname)
        flash_message = {"type": "success", "message": f"{result}"}
        session['flash_message'] = flash_message
        return jsonify({'success': True, 'message': 'Assessment Deleted Successfully', 'flash_message': flash_message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@classRecord.route('/<string:classrecordid>/upload', methods=['POST'])
def upload_file(classrecordid):
    try:
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            ClassRecord.truncate_classrecord(classrecordid)
            result = ClassRecord.upload_csv(file, classrecordid)
            if 'success' in result["type"]:
                flash_message = {"type": "success", "message": f"{file.filename} uploaded successfully."}
            else:
                flash_message = {"type": "danger", "message": f"Error: {result['message']}"}
            session['flash_message'] = flash_message
            return redirect(url_for(".index", classrecordid=classrecordid))
        else:
            raise Exception("Invalid file format. Please upload a CSV file.")
    except Exception as e:
        flash_message = {"type": "danger", "message": f"Error: {str(e)}"}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))


@classRecord.route('/download/classrecord')
def download_classrecord_file():
    file_path = current_app.root_path + '/static/csv-files/class-record.csv'
    return send_file(file_path, as_attachment=True, download_name='class-record.csv')

@classRecord.route("/<string:classrecordid>/create_activity", methods=['POST','GET'])
def create_activity (classrecordid):
    form = activityForm(request.form)
    if request.method == "POST" and form.validate():
        assessmentID = form.Assessment.data
        activityname = form.activityname.data
        scorelimit = form.scorelimit.data
        studentsID = Utils.getClassID(ClassRecord.getClassRecordStudents(classrecordid))
        result = ClassRecord.addActivity(assessmentID, activityname, scorelimit, studentsID)
        if "success" in result:
            credentials_message = f"<br>Activity Name: <strong>{activityname}</strong><br>Score Limit: <strong>{scorelimit}</strong>"
            flash_message = {"type": "success", "message": f"Activity Created successfully:{credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"Failed to create Assessment: {result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))
    else:
        flash_message = {"type": "danger", "message": f"Failed to Add Activity. Please check the form for errors."}
        session['flash_message'] = flash_message
        return redirect(url_for(".index", classrecordid=classrecordid))


@classRecord.route("/get_modal_data/<string:class_record_id>/<string:student_id>", methods =['GET'])
def get_indiv_scores (student_id, class_record_id):
    print(student_id, class_record_id)
    classID = ClassRecord.getstudentclassID(class_record_id, student_id)
    Assessments = ClassRecord.getGradeDistribution(class_record_id)
    AssessmentIDs = Utils.getAssessmentID(Assessments)
    ActivityScores = ClassRecord.getActivityScores(classID, AssessmentIDs)
    print(ActivityScores)
    return jsonify(ActivityScores)


@classRecord.route("/get_activities/<string:assessment_id>", methods=['GET'])
def get_activities(assessment_id):
    try:
        # print("assessment", assessment_id)
        activities = ClassRecord.get_activities_for_assessment(assessment_id)
        # print("act", activities)
        return jsonify({'activities': activities})
    except Exception as e:
        # Handle exceptions and return an appropriate response
        return jsonify({'error': str(e)}), 500
