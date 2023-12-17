from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.validators import InputRequired, ValidationError

class AdminLoginForm(FlaskForm):
    adminEmail = StringField('Email', validators=[InputRequired(), validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])
    adminPassword = PasswordField('Password')
    adminLoginButton = SubmitField('Login')

    # def validate_adminEmail(self, field):
    #     if field.data != "admin@g.msuiit.edu.ph":
    #         raise ValidationError("Invalid email")

    def validate_adminPassword(self, field):
        if field.data != "admin":
            raise ValidationError("Invalid password")