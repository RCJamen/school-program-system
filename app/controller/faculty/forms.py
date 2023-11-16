from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class FacultyForm(FlaskForm):
    
    facultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                   validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    facultyfirstName = StringField('First Name')
    facultylastName = StringField('Last Name')
    facultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    submit_add = SubmitField('Add Faculty')  # Unique name for add faculty submit button

    # editFacultyIDInput = StringField('ID', validators=[validators.DataRequired(),
    #                                                     validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    # editFacultyfirstName = StringField('First Name')
    # editFacultylastName = StringField('Last Name')
    # editFacultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    # submit_update = SubmitField('Update Faculty')  # Unique name for update faculty submit button

class UpdateFacultyForm(FlaskForm):
    editFacultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                        validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    editFacultyfirstName = StringField('First Name')
    editFacultylastName = StringField('Last Name')
    editFacultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    submit_update = SubmitField('Update Faculty')