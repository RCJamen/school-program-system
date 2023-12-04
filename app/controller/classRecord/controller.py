from os import name
from flask import render_template, redirect, request, jsonify, flash, session
from flask.helpers import url_for
from app.controller.admin.controller import login_is_required
from app.models.classRecordModel import ClassRecordModel
from . import classRecord

def classRecord_route(rule, **options):
    def decorator(f):
        @classRecord.route(rule, **options)
        @login_is_required  
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator


@classRecord.route('/class_record/<string:subject_code>/<string:section_code>', methods=['GET'])
def index(subject_code, section_code):
    return render_template("class-record.html", subject_code=subject_code, section_code=section_code)

