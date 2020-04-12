import arrow
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app.main.models import Laboratory
from app import db
from . import lab_blueprint as lab
from .forms import *
from .models import *
from app.main.models import UserLabAffil


@lab.route('/<int:lab_id>')
@login_required
def landing(lab_id):
    affil = UserLabAffil.query.filter_by(lab_id=lab_id, user_id=current_user.id).first()
    if not affil or not affil.approved:
        flash('You do not have a permission to enter this lab.', 'danger')
        return redirect(url_for('main.index'))
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
            choice_set_id = request.form.get('choice_sets')
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
                choice_set_id=choice_set_id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(new_test)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new quantitative test',
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


@lab.route('/<int:lab_id>/qualtests/add', methods=['GET', 'POST'])
@login_required
def add_qual_test(lab_id):
    form = LabQualTestForm(lab_id=lab_id)
    choice_sets = [(c.id, c.name) for c in LabResultChoiceSet.query.filter_by(lab_id=lab_id)]
    form.choice_sets.choices = choice_sets
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get('name')
            detail = request.form.get('detail')
            choice_set_id = request.form.get('choice_sets')
            active = request.form.get('active')
            active = True if active else False
            new_test = LabQualTest(
                lab_id=lab_id,
                name=name,
                detail=detail,
                active=active,
                choice_set_id=choice_set_id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(new_test)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new qualitative test',
                detail=name,
                added_at=arrow.now('Asia/Bangkok').datetime,
            )
            db.session.add(activity)
            db.session.commit()
            flash('New test has been added.')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_qual_test.html', form=form)


@lab.route('/<int:lab_id>/customers')
@login_required
def list_patients(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/customer_list.html', lab=lab)


@lab.route('/<int:lab_id>/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient(lab_id):
    form = LabCustomerForm()
    lab = Laboratory.query.get(lab_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_customer = LabCustomer()
            form.populate_obj(new_customer)
            new_customer.lab_id = lab_id
            db.session.add(new_customer)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new patient',
                detail=new_customer.fullname,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(activity)
            db.session.commit()
            flash('New patient has been added.', 'success')
            return render_template('lab/customer_list.html', lab=lab)
        else:
            flash('Failed to add a new patient.', 'danger')
    return render_template('lab/new_customer.html', form=form)


@lab.route('/<int:lab_id>/patients/<int:customer_id>/orders/menu', methods=['GET', 'POST'])
@login_required
def add_test_order_menu(lab_id, customer_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/new_test_order.html', lab=lab, customer_id=customer_id)


@lab.route('/<int:lab_id>/patients/<int:customer_id>/orders/quant/tests/<int:test_id>/add', methods=['GET', 'POST'])
@login_required
def add_quan_test_order(lab_id, customer_id, test_id):
    test = LabQuanTest.query.get(test_id)
    if test:
        order = LabQuanTestOrder(
            lab_id=lab_id,
            customer_id=customer_id,
            test_id=test.id,
            ordered_at=arrow.now('Asia/Bangkok').datetime,
            ordered_by=current_user
        )
        db.session.add(order)
        activity = LabActivity(
            lab_id=lab_id,
            actor=current_user,
            message='Added an order for a quantitative test.',
            detail=test.name,
            added_at=arrow.now('Asia/Bangkok').datetime
        )
        db.session.add(activity)
        db.session.commit()
        flash('New order has been added.', 'success')
        return redirect(url_for('lab.list_test_orders', lab_id=lab_id))
    flash('Test does not exists.', 'danger')
    return redirect(request.referrer)


@lab.route('/<int:lab_id>/patients/<int:customer_id>/orders/qual/tests/<int:test_id>/add', methods=['GET', 'POST'])
@login_required
def add_qual_test_order(lab_id, customer_id, test_id):
    test = LabQualTest.query.get(test_id)
    if test:
        order = LabQualTestOrder(
            lab_id=lab_id,
            customer_id=customer_id,
            test_id=test.id,
            ordered_at=arrow.now('Asia/Bangkok').datetime,
            ordered_by=current_user
        )
        db.session.add(order)
        activity = LabActivity(
            lab_id=lab_id,
            actor=current_user,
            message='Added an order for a qualitative test.',
            detail=test.name,
            added_at=arrow.now('Asia/Bangkok').datetime
        )
        db.session.add(activity)
        db.session.commit()
        flash('New order has been added.', 'success')
        return redirect(url_for('lab.list_test_orders', lab_id=lab_id))
    flash('Test does not exists.', 'danger')
    return redirect(request.referrer)


@lab.route('/<int:lab_id>/orders', methods=['GET', 'POST'])
@login_required
def list_test_orders(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/quan_test_order_list.html', lab=lab)


@lab.route('/<int:lab_id>/orders/quan/<int:order_id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel_quan_test_order(lab_id, order_id):
    order = LabQuanTestOrder.query.get(order_id)
    order.cancelled_at = arrow.now('Asia/Bangkok').datetime
    order.cancelled_by = current_user
    db.session.add(order)
    activity = LabActivity(
        lab_id=lab_id,
        actor=current_user,
        message='Cancelled the quantitative test order.',
        detail=order.id,
        added_at=arrow.now('Asia/Bangkok').datetime
    )
    db.session.add(activity)
    db.session.commit()
    flash('The order has been cancelled.', 'success')
    if request.args.get('pending'):
        return redirect(url_for('lab.list_pending_orders', lab_id=lab_id))
    return redirect(url_for('lab.list_test_orders', lab_id=lab_id))


@lab.route('/<int:lab_id>/orders/quan/<int:order_id>/receive', methods=['GET', 'POST'])
@login_required
def receive_quan_test_order(lab_id, order_id):
    order = LabQuanTestOrder.query.get(order_id)
    order.received_at = arrow.now('Asia/Bangkok').datetime
    order.receiver = current_user
    db.session.add(order)
    activity = LabActivity(
        lab_id=lab_id,
        actor=current_user,
        message='Received the quantitative test order.',
        detail=order.id,
        added_at=arrow.now('Asia/Bangkok').datetime
    )
    db.session.add(activity)
    db.session.commit()
    flash('The order has been received.', 'success')
    return redirect(url_for('lab.list_test_orders', lab_id=lab_id))


@lab.route('/<int:lab_id>/orders/qual/<int:order_id>/cancel', methods=['GET', 'POST'])
@login_required
def cancel_qual_test_order(lab_id, order_id):
    order = LabQualTestOrder.query.get(order_id)
    order.cancelled_at = arrow.now('Asia/Bangkok').datetime
    order.cancelled_by = current_user
    db.session.add(order)
    activity = LabActivity(
        lab_id=lab_id,
        actor=current_user,
        message='Cancelled the qualitative test order.',
        detail=order.id,
        added_at=arrow.now('Asia/Bangkok').datetime
    )
    db.session.add(activity)
    db.session.commit()
    flash('The order has been cancelled.', 'success')
    if request.args.get('pending'):
        return redirect(url_for('lab.list_pending_orders', lab_id=lab_id))
    return redirect(url_for('lab.list_test_orders', lab_id=lab_id))


@lab.route('/<int:lab_id>/orders/qual/<int:order_id>/receive', methods=['GET', 'POST'])
@login_required
def receive_qual_test_order(lab_id, order_id):
    order = LabQualTestOrder.query.get(order_id)
    order.received_at = arrow.now('Asia/Bangkok').datetime
    order.receiver = current_user
    db.session.add(order)
    activity = LabActivity(
        lab_id=lab_id,
        actor=current_user,
        message='Received the qualitative test order.',
        detail=order.id,
        added_at=arrow.now('Asia/Bangkok').datetime
    )
    db.session.add(activity)
    db.session.commit()
    flash('The order has been received.', 'success')
    return redirect(url_for('lab.list_test_orders', lab_id=lab_id))


@lab.route('/<int:lab_id>/orders/pending', methods=['GET', 'POST'])
@login_required
def list_pending_orders(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/pending_orders.html', lab=lab)


@lab.route('/<int:lab_id>/activities')
@login_required
def list_activities(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/log.html', lab=lab)


@lab.route('/<int:lab_id>/orders/<int:order_id>/finish', methods=['POST', 'GET'])
@login_required
def finish_quan_test_order(lab_id, order_id):
    order = LabQuanTestOrder.query.get(order_id)
    if order:
        order.finished_at = arrow.now('Asia/Bangkok').datetime
        db.session.add(order)
        db.session.commit()
    else:
        flash('Order no longer exists.', 'danger')
        return redirect(request.referrer)

    record_set = LabQuanTestRecordSet.query.filter_by(order_id=order_id).first()
    if not record_set:
        record_set = LabQuanTestRecordSet(order_id=order_id)
        flash('New result record set has been created for the order.', 'success')
        db.session.add(record_set)
        db.session.commit()

    form = LabQuanTestRecordForm()
    if order.test.choice_set:
        choices = [(c.result, c.result) for c in order.test.choice_set.choice_items]
    else:
        choices = []
    form.result_choices.choices = choices
    if request.method == 'POST':
        if form.validate_on_submit():
            new_record = LabQuanTestRecord()
            form.populate_obj(new_record)
            new_record.record_set = record_set
            new_record.updated_at = arrow.now('Asia/Bangkok').datetime
            new_record.updator = current_user
            new_record.text_result = form.result_choices.data
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added the result for a test order.',
                detail=order.id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(new_record)
            db.session.add(activity)
            db.session.commit()
            flash('New result record has been saved.', 'success')
            return redirect(url_for('lab.list_pending_orders', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_quan_test_record.html', form=form, order=order)
