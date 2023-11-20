from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subjectsHandled
from app.controller.admin.controller import login_is_required
from app.models.subjectModel import SubjectList


@subjectsHandled.route("/subjects-handled")
@login_is_required
def index():
    handlerName = session["name"]
    subjectsHandledList = SubjectList.getSubjectsHandled(handlerName)
    return render_template("subjectsHandled.html", subjectsHandledList=subjectsHandledList)
