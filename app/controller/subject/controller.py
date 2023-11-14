from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subject
from app.controller.admin.controller import login_is_required
from app import mysql
import app.models.subject as subjectListModel


@subject.route("/subjects")
@login_is_required
def index():
    subjectInfo = subjectListModel.SubjectList.all()
    return render_template("subjectList.html", subjectInfo=subjectInfo)
