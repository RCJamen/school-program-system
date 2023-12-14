from os import name
from . import faculty
from flask import render_template, request, jsonify, redirect, url_for,flash, session
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
            role = add_form.facultyRole.data

            result = faculty_model.create_faculty(facultyID, firstname, lastname, email, role)

            if "success" in result:
                credentials_message = f"ID: <strong>{facultyID}</strong>, Name: <strong>{firstname} {lastname}</strong>, Email: <strong>{email}</strong>, Role: <strong>{role}</strong>"
                flash_message = {"type": "success", "message": f"Faculty created successfully - {credentials_message}"}
            else:
                flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}

    faculties = faculty_model.get_faculty()
    
    

    return render_template("faculty.html", faculties=faculties, add_form=add_form, flash_message=flash_message, update_form=update_form)

@faculty.route("/faculty_data", methods=["GET"], endpoint="get_faculty_data")
@login_is_required
def get_faculty_data():
    faculty_id = request.args.get('faculty_id')
    print(faculty_id)
    faculty_data = faculty_model.get_assigned_subjects(faculty_id)
    print("faculty data:", faculty_data)
    # Return the faculty data as JSON
    return jsonify(faculty_data)


@faculty.route("/faculty/delete/<string:facultyID>", methods=["DELETE"])
def delete_faculty(facultyID):
    try:
        result = faculty_model.delete_faculty(facultyID)
        return jsonify({'success': result == 'Faculty deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@faculty.route("/faculty/edit/<string:facultyID>", methods=["POST"])
def edit_faculty(facultyID):
    try:
        form = UpdateFacultyForm(request.form)  # Create form instance and populate it with request data
        if form.validate_on_submit():  # Validate the form
            new_firstname = form.editFacultyfirstName.data
            new_lastname = form.editFacultylastName.data
            new_email = form.editFacultyEmail.data
            new_role = form.editFacultyRole.data
            result = faculty_model.update_faculty(facultyID, new_firstname, new_lastname, new_email, new_role)
            if result == "Faculty Information Updated Successfully":
                session["role"] = new_role
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


@faculty.route('/faculty_schedule', methods=["GET"])
def show_schedule():
    try:
        # Extract faculty ID from query parameters
        faculty_id = request.args.get('faculty_id')
        print("faculty_id:", faculty_id)  # Add this line for debugging

        # Assuming YourModel has a method get_schedule_by_day
        monday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Monday')
        tuesday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Tuesday')
        wednesday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Wednesday')
        thursday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Thursday')
        friday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Friday')
        saturday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Saturday')
        sunday_schedule = faculty_model.get_schedule_by_day(faculty_id, 'Sunday')
      
        print("Monday_sched:", monday_schedule)
       
        # Use jsonify to send JSON response
        return jsonify({"data": {"monday_schedule": monday_schedule, "tuesday_schedule": tuesday_schedule, "wednesday_schedule": wednesday_schedule, "friday_schedule": friday_schedule,
                                 "thursday_schedule": thursday_schedule, "saturday_schedule": saturday_schedule,"sunday_schedule": sunday_schedule }, "success": True})
    except Exception as e:
        return jsonify({"error": str(e), "success": False})



@faculty.route("/faculty/delete-schedule/<int:scheduleID>", methods=["DELETE"])
def delete_schedule(scheduleID):
    try:
        result = faculty_model.delete_schedule(scheduleID)
        if result == "Schedule deleted successfully":
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

