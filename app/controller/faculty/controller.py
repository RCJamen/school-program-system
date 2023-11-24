from os import name
from . import faculty
from flask import render_template, request, jsonify, redirect, url_for,flash
from app.controller.faculty.forms import FacultyForm, UpdateFacultyForm
from app.models.facultyModel import facultyModel
from app.controller.admin.controller import login_is_required

faculty_model = facultyModel()


@faculty.route("/faculty", methods=["GET", "POST"], endpoint="add_faculty")
@login_is_required
def add_faculty():
    add_form = FacultyForm()
    update_form = UpdateFacultyForm()
    flash_message = None

    # Check if faculty_id is present in the request parameters
    

    if request.method == "POST":
        if add_form.validate_on_submit():
            facultyID = add_form.facultyIDInput.data
            firstname = add_form.facultyfirstName.data
            lastname = add_form.facultylastName.data
            email = add_form.facultyEmail.data

            result = faculty_model.create_faculty(facultyID, firstname, lastname, email)

            if "success" in result:
                credentials_message = f"ID: <strong>{facultyID}</strong>, Name: <strong>{firstname} {lastname}</strong>, Email: <strong>{email}</strong>"
                flash_message = {"type": "success", "message": f"Faculty created successfully - {credentials_message}"}
            else:
                flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}

    faculties = faculty_model.get_faculty()
    
    

    return render_template("faculty.html", faculties=faculties, add_form=add_form, flash_message=flash_message, update_form=update_form)

@faculty.route("/faculty_data", methods=["GET"], endpoint="get_faculty_data")
@login_is_required
def get_faculty_data():
    faculty_id = request.args.get('faculty_id')
    faculty_data = faculty_model.get_assigned_subjects(faculty_id)

    # Return the faculty data as JSON
    return jsonify(faculty_data)


@faculty.route("/faculty/delete/<string:facultyID>", methods=["DELETE"])
def delete_faculty(facultyID):
    try:
        result = faculty_model.delete_faculty(facultyID)
        return jsonify({'success': result == 'Faculty deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
# @faculty.route("/faculty/edit/<string:facultyID>", methods=["POST"])
# def edit_faculty(facultyID):
#     try:
#         new_firstname = request.form.get("editFacultyfirstName")
#         new_lastname = request.form.get("editFacultylastName")
#         new_email = request.form.get("editFacultyEmail")  # Corrected key
#         result = faculty_model.update_faculty(facultyID, new_firstname, new_lastname, new_email)
#         return jsonify({"success": result == "Faculty Information Updated Successfully"})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

@faculty.route("/faculty/edit/<string:facultyID>", methods=["POST"])
def edit_faculty(facultyID):
    try:
        form = UpdateFacultyForm(request.form)  # Create form instance and populate it with request data
        if form.validate_on_submit():  # Validate the form
            new_firstname = form.editFacultyfirstName.data
            new_lastname = form.editFacultylastName.data
            new_email = form.editFacultyEmail.data
            result = faculty_model.update_faculty(facultyID, new_firstname, new_lastname, new_email)
            return jsonify({"success": result == "Faculty Information Updated Successfully"})
        else:
            # Handle the case where form validation fails
            errors = {field: form.errors[field][0] for field in form.errors}
            return jsonify({"success": False, "errors": errors})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@faculty.route("/faculty/add-schedule", methods=["POST"])
def add_schedule():
    try:
        subject_id = request.form.get("subject-id")
        section_id = request.form.get("section-id")
        day = request.form.get("day")
        time_start = request.form.get("time-start")
        time_end = request.form.get("time-end")

        result = faculty_model.create_schedule(subject_id, section_id, day, time_start, time_end)
        return jsonify({"success": result == "Schedule created successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
