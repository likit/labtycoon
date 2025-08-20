from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired, EqualTo


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', [InputRequired()])
    lastname = StringField('Last Name', [InputRequired()])
    license_id = StringField('License ID', [InputRequired()])
    email = StringField('Email', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(),
                                          EqualTo('confirm', message='Password must match.')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired()])
