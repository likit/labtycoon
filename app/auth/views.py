from . import auth_blueprint as auth
from flask_login import login_required, login_user,  logout_user
from flask import render_template
from .forms import LoginForm, RegistrationForm


@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('/auth/login.html', form=form)


@auth.route('/register')
def register():
    form = RegistrationForm()
    return render_template('/auth/register.html', form=form)
