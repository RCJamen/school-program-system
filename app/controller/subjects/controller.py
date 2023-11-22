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
    flash_message = session.pop('flash_message', None)
    return render_template("subjectList.html", subjectInfo=subjectInfo, sectionInfo=sectionInfo, handlerInfo=handlerInfo, flash_message=flash_message)

@subject.route("/subjects/create", methods=['POST','GET'])
def create_subject():
    form = subjectForm(request.form)
    if request.method == "POST" and form.validate():
        code=form.subjectCode.data
        section=form.section.data
        description=form.description.data
        credits=form.credits.data
        handler=form.handler.data
        subjects = subjectModel.Subjects(code, section, description, credits, handler)
        result = subjects.add()
        if "success" in result:
            credentials_message = f"Subject Code: <strong>{code}</strong><br>Section: <strong>{section}</strong><br> Description: <strong>{description}</strong><br>Credits: <strong>{credits}</strong><br>Handler: <strong>{handler}</strong>"
            flash_message = {"type": "success", "message": f"Subject created successfully - {credentials_message}"}
            session['flash_message'] = flash_message
        else:
            flash_message = {"type": "danger", "message": f"Failed to create Subject: {result}"}
            session['flash_message'] = flash_message
        return redirect(url_for(".index", message=flash_message))
    return redirect(url_for(".index"))

@subject.route("/subjects/delete/<string:subjectCode>/<string:section>", methods=["POST"])
def delete_subject(subjectCode, section):
    try:
        result = subjectModel.Subjects.delete(subjectCode, section)
        print(result)
        return jsonify({'success': result == 'Subject deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})