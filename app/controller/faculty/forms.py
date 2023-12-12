from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators

class FacultyForm(FlaskForm):
    facultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                   validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    facultyfirstName = StringField('First Name', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="Firstname should only contain letters, spaces, or hyphens")
    ])
    facultylastName = StringField('Last Name', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="Lastname should only contain letters, spaces, or hyphens")
    ])
    facultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    facultyRole = SelectField('Select Role', choices=[('Admin', 'Admin'), ('Chairperson', 'Chairperson'), ('Faculty', 'Faculty')])
    submit_add = SubmitField('Add Faculty')

class UpdateFacultyForm(FlaskForm):
    editFacultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                        validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    editFacultyfirstName = StringField('First Name', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="First Name should only contain letters, spaces, or hyphens")
    ])
    editFacultylastName = StringField('Last Name', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="Last Name should only contain letters, spaces, or hyphens")
    ])
    editFacultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    editFacultyRole = SelectField('Select Role', choices=[('Admin', 'Admin'), ('Chairperson', 'Chairperson'), ('Faculty', 'Faculty')])
    submit_update = SubmitField('Update Faculty')
