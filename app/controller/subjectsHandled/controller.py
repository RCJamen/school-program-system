from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subjectsHandled
from app.controller.admin.controller import login_is_required
from app.models.subjectModel import Subjects


@subjectsHandled.route("/subjects-handled")
@login_is_required
def index():
    # handlerGoogleID = session["google_id"]
    userEmail = session["email"]
    # Subjects.setGoogleID(handlerGoogleID, userEmail)
    # subjectsHandledList = Subjects.getSubjectsHandled(handlerGoogleID)
    subjectsHandledList = Subjects.getSubjectsHandled(userEmail)
    return render_template("subjectsHandled.html", subjectsHandledList=subjectsHandledList)
