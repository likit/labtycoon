import arrow
from flask import render_template, url_for, flash, redirect, request, make_response
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
            flash('You already sent a request. Please wait to be approved.', 'warning')
            return redirect(url_for('main.index'))
        else:
            flash('You already affiliate with this lab.', 'success')
            return redirect(url_for('lab.landing', lab_id=lab_id))
    else:
        affil_record = UserLabAffil(
            user=current_user,
            lab=lab,
            joined_at=arrow.now('Asia/Bangkok').datetime
        )
        db.session.add(affil_record)
        db.session.commit()
        return render_template('main/lab_members.html', lab=lab)


@main.route('/labs/<int:lab_id>/approve/user/<int:user_id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def approve_member(lab_id, user_id):
    affil_record = UserLabAffil.query.filter_by(user_id=user_id,
                                                lab_id=lab_id
                                                ).first()
    lab = Laboratory.query.get(lab_id)
    if current_user != lab.creator:
        flash('You do not have a permission to approve a user.', 'danger')

    if request.method == 'GET':
        if current_user == lab.creator:
            if not affil_record.approved:
                affil_record.approved = True
                db.session.add(affil_record)
                db.session.commit()
                flash('The user has been approved to join the lab.', 'success')
            else:
                flash('The user has already been approved.')
    elif request.method == 'DELETE':
        affil_record.deactivated_at = arrow.now('Asia/Bangkok').datetime
        db.session.add(affil_record)
        db.session.commit()
        flash('The user has been deactivated for this lab.', 'success')
        resp = make_response()
        resp.headers['HX-Refresh'] = 'true'
        return resp
    elif request.method == 'POST':
        affil_record.deactivated_at = None
        db.session.add(affil_record)
        db.session.commit()
        flash('The user has been activated for this lab.', 'success')
        resp = make_response()
        resp.headers['HX-Refresh'] = 'true'
        return resp

    return redirect(url_for('main.list_members', lab_id=lab_id))

