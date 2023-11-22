from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from app.controller.admin.controller import login_is_required
from app.controller.subjects.forms import subjectForm
import app.models.subjectModel as subjectModel
from . import subject

def subject_route(rule, **options):
    def decorator(f):
        @subject.route(rule, **options)
        @login_is_required  
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator


@subject.route("/subjects")
def index():
    subjectInfo = subjectModel.Subjects.all()
    sectionInfo = subjectModel.Subjects.refer_section()
    handlerInfo = subjectModel.Subjects.refer_handler()
    return render_template("subjectList.html", subjectInfo=subjectInfo, sectionInfo=sectionInfo, handlerInfo=handlerInfo)

@subject.route("/subjects/create", methods=['POST','GET'])
def create_subject():
    form = subjectForm(request.form)
    if request.method == "POST" and form.validate():
        subjects = subjectModel.Subjects(code=form.subjectCode.data, section=form.section.data, description=form.section.data, credits=form.credits.data, handler=form.handler.data)
        print(subjects)
        subjects.add()
       
        # if "success" in result:
        #     credentials_message = f"Subject Code: <strong>{facultyID}</strong>, Name: <strong>{firstname} {lastname}</strong>, Email: <strong>{email}</strong>"
        #     flash_message = {"type": "success", "message": f"Faculty created successfully - {credentials_message}"}
        # else:
        #     flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}


        return redirect(url_for(".index"))
    return redirect(url_for(".index"))

@subject.route("/subjects/delete/<string:subjectCode>/<string:section>", methods=["POST"])
def delete_subject(subjectCode, section):
    try:
        result = subjectModel.Subjects.delete(subjectCode, section)
        print(result)
        return jsonify({'success': result == 'Subject deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})