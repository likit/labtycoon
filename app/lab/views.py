import arrow
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app.main.models import Laboratory
from app import db
from . import lab_blueprint as lab
from .forms import ChoiceItemForm
from .models import LabResultChoiceItem, LabActivity


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
            is_ref = request.form.getlist('ref', [])
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
