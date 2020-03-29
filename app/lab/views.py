import arrow
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app.main.models import Laboratory
from app import db
from . import lab_blueprint as lab
from .forms import ChoiceItemForm, ChoiceSetForm, LabQuanTestForm
from .models import LabResultChoiceItem, LabActivity, LabResultChoiceSet, LabQuanTest


@lab.route('/<int:lab_id>')
@login_required
def landing(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/index.html', lab=lab)


@lab.route('/<int:lab_id>/tests')
@login_required
def list_tests(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/test_list.html', lab=lab)


@lab.route('/<int:lab_id>/choice_sets')
@login_required
def list_choice_sets(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/choice_set_list.html', lab=lab)


@lab.route('/<int:lab_id>/choice_sets/<int:choice_set_id>/items', methods=['GET', 'POST'])
@login_required
def add_choice_item(lab_id, choice_set_id):
    form = ChoiceItemForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            result = request.form.get('result')
            interpret = request.form.get('interpretation')
            is_ref = request.form.get('ref')
            ref = True if is_ref else False
            new_item = LabResultChoiceItem(
                choice_set_id=choice_set_id,
                result=result,
                interpretation=interpret,
                ref=ref,
            )
            db.session.add(new_item)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added result choice item',
                detail=result,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(activity)
            db.session.commit()
            flash('New choice has been added.', 'success')
        else:
            flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('lab.list_choice_sets', lab_id=lab_id))
    return render_template('lab/new_choice_item.html', form=form)


@lab.route('/<int:lab_id>/choice_sets/<int:choice_set_id>/items/<int:choice_item_id>/remove')
@login_required
def remove_choice_item(lab_id, choice_set_id, choice_item_id):
    item = LabResultChoiceItem.query.get(choice_item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Choice has been deleted.', 'success')
    else:
        flash('Choice not found.', 'danger')
    return redirect(url_for('lab.list_choice_sets', lab_id=lab_id))


@lab.route('/<int:lab_id>/choice_sets/add', methods=['GET', 'POST'])
@login_required
def add_choice_set(lab_id):
    form = ChoiceSetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            reference = request.form.get('reference')
            new_choice_set = LabResultChoiceSet(lab_id=lab_id, name=name, reference=reference)
            db.session.add(new_choice_set)
            activity = LabActivity(
                lab_id=lab_id,
                message='Added a new choice set',
                detail=name,
                added_at=arrow.now('Asia/Bangkok').datetime,
                actor=current_user
            )
            db.session.add(activity)
            db.session.commit()
            flash('New choice set has been added.', 'success')
        else:
            flash('Error occurred while adding a new choice set.', 'danger')
        return redirect(url_for('lab.list_choice_sets', lab_id=lab_id))
    return render_template('lab/new_choice_set.html', form=form)


@lab.route('/<int:lab_id>/choice_sets/<int:choice_set_id>/remove')
@login_required
def remove_choice_set(lab_id, choice_set_id):
    choiceset = LabResultChoiceSet.query.get(choice_set_id)
    if choiceset:
        db.session.delete(choiceset)
        db.session.commit()
        flash('The choice set has been removed.', 'success')
    else:
        flash('The choice set does not exist.', 'warning')
    return redirect(url_for('lab.list_choice_sets', lab_id=lab_id))


@lab.route('/<int:lab_id>/quantests/add', methods=['GET', 'POST'])
@login_required
def add_quan_test(lab_id):
    form = LabQuanTestForm(lab_id=lab_id)
    choice_sets = [(c.id, c.name) for c in LabResultChoiceSet.query.filter_by(lab_id=lab_id)]
    form.choice_sets.choices = choice_sets
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            detail = request.form.get('detail')
            min_value = request.form.get('min_value')
            max_value = request.form.get('max_value')
            min_ref_value = request.form.get('min_ref_value')
            max_ref_value = request.form.get('max_ref_value')
            active = request.form.get('active')
            min_value = float(min_value) if min_value else None
            max_value = float(max_value) if max_value else None
            min_ref_value = float(min_ref_value) if min_ref_value else None
            max_ref_value = float(max_ref_value) if max_ref_value else None
            active = True if active else False
            new_test = LabQuanTest(
                lab_id=lab_id,
                name=name,
                detail=detail,
                min_value=min_value,
                max_value=max_value,
                min_ref_value=min_ref_value,
                max_ref_value=max_ref_value,
                active=active,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(new_test)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new test',
                detail=name,
                added_at=arrow.now('Asia/Bangkok').datetime,
            )
            db.session.add(activity)
            db.session.commit()
            flash('New test has been added.')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_quan_test.html', form=form)