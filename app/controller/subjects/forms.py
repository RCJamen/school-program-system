from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class subjectForm(FlaskForm):
    subjectCode = StringField("subjectCode", [validators.DataRequired()])
    old_subjectCode = StringField("editCodeInput")
    section = StringField("section", [validators.DataRequired()])
    description = StringField("description", [validators.DataRequired()])
    credits = StringField("credits", [validators.DataRequired()])
    handler = StringField("handler", [validators.DataRequired()])
    editHandlerInput = StringField("editHandlerInput")
    submit = SubmitField("Submit")
