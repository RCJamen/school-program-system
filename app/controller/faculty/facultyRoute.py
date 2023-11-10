from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app.models.facultyModel import facultyModel
from app.controller.admin.controller import login_is_required

facultyRoute = Blueprint('faculty', __name__)
faculty_model = facultyModel()


class FacultyForm(FlaskForm):
    facultyIDInput = StringField('ID')
    facultyfirstName = StringField('First Name')
    faculylastName = StringField('Last Name')
    facultyEmail = StringField('MSU-IIT Email')
    submit = SubmitField('Add Faculty')

@facultyRoute.route("/faculty", methods=["GET", "POST"])
@login_is_required
def faculty():
    form = FacultyForm()
    flash_message = None
    if request.method == "POST":
        facultyID = request.form.get("facultyIDInput")
        firstname = request.form.get("facultyfirstName")
        lastname = request.form.get("faculylastName")
        email = request.form.get("facultyEmail")
        result = faculty_model.create_faculty(facultyID, firstname, lastname, email)
        if "success" in result:
            flash_message = {"type": "success", "message": "Faculty created successfully"}
        else:
            flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}

    faculties = faculty_model.get_faculty()
    
    return render_template("faculty.html", faculties=faculties, form=form, flash_message=flash_message)