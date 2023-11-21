from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from . import classRecord
from app.controller.admin.controller import login_is_required

@classRecord.route("/class-record")
@login_is_required
def class_record():
    return render_template("class-record.html")
