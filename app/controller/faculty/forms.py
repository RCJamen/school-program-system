from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class FacultyForm(FlaskForm):
    # Define a regex pattern for facultyIDInput
    
    facultyIDInput = StringField('ID', validators=[validators.DataRequired(),
                                                   validators.Regexp(regex=r'^\d{4}-\d{4}$',
                                                    message='Invalid format. Use ####-####')])
    facultyfirstName = StringField('First Name')
    facultylastName = StringField('Last Name')
    facultyEmail = StringField('MSU-IIT Email')
    submit = SubmitField('Add Faculty')
