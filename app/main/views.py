import arrow
from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from . import main_blueprint as main
from app.main.models import Laboratory, UserLabAffil
from app import db


@main.route('/')
@login_required
def index():
    labs = Laboratory.query.all()
    return render_template('main/index.html', labs=labs)


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/labs/<int:lab_id>/members')
@login_required
def list_members(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('main/lab_members.html', lab=lab)


@main.route('/labs/<int:lab_id>/join')
@login_required
def request_join_lab(lab_id):
    existing_affil_record = UserLabAffil.query.filter_by(lab_id=lab_id, user_id=current_user.id).first()
    lab = Laboratory.query.get(lab_id)
    if existing_affil_record:
        if not existing_affil_record.approved:
            return 'you are already sent a request.'
        else:
            return 'you are already affiliated with this lab.'
    else:
        affil_record = UserLabAffil(
            user=current_user,
            lab=lab,
            joined_at=arrow.now('Asia/Bangkok').datetime
        )
        db.session.add(affil_record)
        db.session.commit()
        return render_template('main/lab_members.html', lab=lab)


@main.route('/labs/<int:lab_id>/approve/user/<int:user_id>')
@login_required
def approve_member(lab_id, user_id):
    affil_record = UserLabAffil.query.filter_by(user_id=user_id,
                                                lab_id=lab_id
                                                ).first()
    lab = Laboratory.query.get(lab_id)
    if current_user == lab.creator:
        if not affil_record.approved:
            affil_record.approved = True
            db.session.add(affil_record)
            db.session.commit()
            flash('The user has been approved to join the lab.', 'success')
        else:
            flash('The user has already been approved.')
    else:
        flash('You do not have a permission to approve a user.', 'danger')
    return redirect(url_for('main.list_members', lab_id=lab_id))
