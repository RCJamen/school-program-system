from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class FacultyForm(FlaskForm):
    
    facultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                   validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    facultyfirstName = StringField('First Name')
    facultylastName = StringField('Last Name')
    facultyEmail = StringField('MSU-IIT Email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message = "Only Accepts MSU-IIT Email")])
    submit = SubmitField('Add Faculty')
