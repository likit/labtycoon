from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired, EqualTo
from wtforms_alchemy import model_form_factory
from app.auth.models import User

from app import db

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['pwdhash']


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


class PasswordForm(FlaskForm):
    password = PasswordField('Password', [InputRequired(),
                                          EqualTo('confirm', message='Password must match.')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


confirm = PasswordField('Confirm Password', [InputRequired()])
