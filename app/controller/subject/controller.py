from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subject
from app.controller.admin.controller import login_is_required
from app.models.subjectModel import SubjectList


@subject.route("/subjects")
@login_is_required
def index():
    subjectInfo = SubjectList.all()
    return render_template("subjectList.html", subjectInfo=subjectInfo)


# @subject.route("/subjects/update")
# @login_is_required
# def subject_update():
#     subjectInfo = SubjectList.all()
#     return "1"
