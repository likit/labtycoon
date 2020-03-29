from . import auth_blueprint as auth
from app import db
from flask_login import login_required, login_user,  logout_user
from flask import render_template, request, flash, redirect, url_for
from .forms import LoginForm, RegistrationForm
from .models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            existing_username = User.query.filter_by(email=email).first()
            if not existing_username:
                flash('The email is not registered. Please register the email.', 'danger')
                return redirect(url_for('auth.register'))
            else:
                if existing_username.check_password(password):
                    return 'user has logged in.'
        else:
            flash(form.errors, 'danger')
    return render_template('/auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            existing_username = User.query.filter_by(email=email).first()
            if existing_username:
                flash('This email has been registered.', 'warning')
            else:
                user = User(firstname=firstname,
                            lastname=lastname,
                            email=email,
                            password=password)
                db.session.add(user)
                db.session.commit()
                flash('The account has been registered. Please log in.')
                return redirect(url_for('auth.login'))
        else:
            flash(form.errors, 'danger')

    return render_template('/auth/register.html', form=form)
