from os import name
from . import faculty
from flask import render_template, request, jsonify, redirect, url_for,flash
from app.controller.faculty.forms import FacultyForm
from app.models.facultyModel import facultyModel
from app.controller.admin.controller import login_is_required

faculty_model = facultyModel()

@faculty.route("/faculty", methods=["GET", "POST"])
@login_is_required
def add_faculty():
    
    form = FacultyForm()
    flash_message = None
    single_faculty = None
    if request.method == "POST":
        if form.validate_on_submit():
            facultyID = form.facultyIDInput.data
            firstname = form.facultyfirstName.data
            lastname = form.facultylastName.data
            email = form.facultyEmail.data

            result = faculty_model.create_faculty(facultyID, firstname, lastname, email)
            # single_faculty = faculty_model.get_single_faculty(facultyID)
            if "success" in result:
                flash_message = {"type": "success", "message": "Faculty created successfully"}
            else:
                flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}
        # else:
        #     flash_message = {"type": "danger", "message": "Form validation failed. Please check your inputs."}

    faculties = faculty_model.get_faculty()
    
    return render_template("faculty.html", faculties=faculties, form=form, flash_message=flash_message)

@faculty.route("/faculty/delete/<string:facultyID>", methods=["DELETE"])
def delete_faculty(facultyID):
    try:
        result = faculty_model.delete_faculty(facultyID)
        return jsonify({'success': result == 'Faculty deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
