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


@classRecord.route('/class_record/<string:subject_code>/<string:description>/<string:section_code>/<string:credits>/<string:sem>/<string:school_year>', methods =['GET', 'POST'])
def index(subject_code, section_code, description, credits ,sem, school_year):
    ClassDetails = [subject_code, description, section_code, credits, sem, school_year]
    return render_template("class-record.html", ClassDetails=ClassDetails)