from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Email, InputRequired, EqualTo


class RegistrationForm(FlaskForm):
    firstname = TextField('First Name', [
        InputRequired()
    ])
    lastname = TextField('Last Name', [
        InputRequired()
    ])
    license_id = TextField('License ID', [
        InputRequired()
    ])
    email = TextField('Email', [
        InputRequired(),
        Email()
    ])
    password = PasswordField('Password', [
        InputRequired(),
        EqualTo('confirm', message='Password must match.'),
    ])
    confirm = PasswordField('Confirm Password', [
        InputRequired(),
    ])


class LoginForm(FlaskForm):
    email = TextField('Email', [
        InputRequired(),
        Email()
    ])
    password = PasswordField('Password', [
        InputRequired(),
    ])
