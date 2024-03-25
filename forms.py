from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired()])
    email = EmailField("Email", [validators.InputRequired()])
    phone = StringField("Phone Number", [validators.InputRequired()])
    message = CKEditorField("Message", [validators.InputRequired()])
    submit = SubmitField("Submit details")
