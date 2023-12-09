from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

class classRecordForm(FlaskForm):
    studentID = StringField('studentID', validators=[validators.DataRequired(), validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])
    firstname = StringField("firstname", [validators.DataRequired()])
    lastname = StringField("lastname", [validators.DataRequired()])
    coursecode = StringField("coursecode", [validators.DataRequired()])
    email = StringField('email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    submit = SubmitField("Submit")
