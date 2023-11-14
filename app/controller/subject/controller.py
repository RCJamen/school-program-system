from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import subject
from app.controller.admin.controller import login_is_required


@subject.route("/subjects")
@login_is_required
def index():
    return render_template("subjectList.html")
