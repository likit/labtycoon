import arrow
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from app.main.models import Laboratory
from app import db
from . import lab_blueprint as lab
from .forms import *
from .models import *
from app.main.models import UserLabAffil
from wtforms_alchemy.fields import QuerySelectField


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
    form.choice_set.query = LabResultChoiceSet.query.filter_by(lab_id=lab_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_test = LabQuanTest()
            form.populate_obj(new_test)
            new_test.lab_id = lab_id
            db.session.add(new_test)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new quantitative test',
                detail=form.name.data,
                added_at=arrow.now('Asia/Bangkok').datetime,
            )
            db.session.add(activity)
            db.session.commit()
            flash('New quantative test has been added.')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_quan_test.html', form=form)


@lab.route('/<int:lab_id>/quantests/<int:test_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quan_test(lab_id, test_id):
    test = LabQuanTest.query.get(test_id)
    form = LabQuanTestForm(obj=test)
    form.choice_set.query = LabResultChoiceSet.query.filter_by(lab_id=lab_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(test)
            db.session.add(test)
            db.session.commit()
            flash('Data have been saved.', 'success')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash('An error occurred. Please contact the system administrator.', 'danger')
    return render_template('lab/new_quan_test.html', form=form, lab_id=lab_id)


@lab.route('/<int:lab_id>/qualtests/add', methods=['GET', 'POST'])
@login_required
def add_qual_test(lab_id):
    form = LabQualTestForm()
    form.choice_set.query = LabResultChoiceSet.query.filter_by(lab_id=lab_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_test = LabQualTest()
            form.populate_obj(new_test)
            new_test.lab_id = lab_id
            db.session.add(new_test)
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added a new qualitative test',
                detail=form.name.data,
                added_at=arrow.now('Asia/Bangkok').datetime,
            )
            db.session.add(activity)
            db.session.commit()
            flash('New qualitative test has been added.')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_qual_test.html', form=form)


@lab.route('/<int:lab_id>/qualtests/<int:test_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_qual_test(lab_id, test_id):
    test = LabQualTest.query.get(test_id)
    form = LabQualTestForm(obj=test)
    form.choice_set.query = LabResultChoiceSet.query.filter_by(lab_id=lab_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(test)
            db.session.add(test)
            db.session.commit()
            flash('Data have been saved.', 'success')
            return redirect(url_for('lab.list_tests', lab_id=lab_id))
        else:
            flash('An error occurred. Please contact the system administrator.', 'danger')
    return render_template('lab/new_qual_test.html', form=form, lab_id=lab_id)


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


@lab.route('/customers/<int:customer_id>/records')
@login_required
def show_customer_records(customer_id):
    customer = LabCustomer.query.get(customer_id)
    if customer:
        return render_template('lab/customer_records.html', customer=customer)


@lab.route('/customers/<int:customer_id>/quan/records/<int:recordset_id>')
@login_required
def show_customer_quan_recordset(customer_id, recordset_id):
    customer = LabCustomer.query.get(customer_id)
    recordset = LabQuanTestRecordSet.query.get(recordset_id)
    if customer and recordset:
        return render_template('lab/recordset_detail.html',
                               customer=customer, recordset=recordset, quan=True)


@lab.route('/customers/<int:customer_id>/qual/records/<int:recordset_id>')
@login_required
def show_customer_qual_recordset(customer_id, recordset_id):
    customer = LabCustomer.query.get(customer_id)
    recordset = LabQualTestRecordSet.query.get(recordset_id)
    if customer and recordset:
        return render_template('lab/recordset_detail.html',
                               customer=customer, recordset=recordset, quan=False)


@lab.route('/<int:lab_id>/quan/orders/<int:order_id>/finish', methods=['POST', 'GET'])
@login_required
def finish_quan_test_order(lab_id, order_id):
    order = LabQuanTestOrder.query.get(order_id)
    if not order:
        flash('Order no longer exists.', 'danger')
        return redirect(request.referrer)

    record_set = LabQuanTestRecordSet.query.filter_by(order_id=order_id).first()
    if not record_set:
        record_set = LabQuanTestRecordSet(order_id=order_id)
        flash('New result record set has been created for the order.', 'success')
        db.session.add(record_set)
        db.session.commit()

    form = LabQuanTestRecordForm()
    try:
        form.choice.query = order.test.choice_set.choice_items
    except AttributeError:
        form.choice.query = []

    if request.method == 'POST':
        if form.validate_on_submit():
            new_record = LabQuanTestRecord()
            form.populate_obj(new_record)
            new_record.record_set = record_set
            new_record.updated_at = arrow.now('Asia/Bangkok').datetime
            new_record.updator = current_user
            if form.choice.data:
                new_record.text_result = form.choice.data.result
            activity = LabActivity(
                lab_id=lab_id,
                actor=current_user,
                message='Added the result for a test order.',
                detail=order.id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            order.finished_at = arrow.now('Asia/Bangkok').datetime
            db.session.add(order)
            db.session.add(new_record)
            db.session.add(activity)
            db.session.commit()
            flash('New result record has been saved.', 'success')
            return redirect(url_for('lab.list_pending_orders', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_quan_test_record.html', form=form, order=order)


@lab.route('/<int:lab_id>/qual/orders/<int:order_id>/finish', methods=['POST', 'GET'])
@login_required
def finish_qual_test_order(lab_id, order_id):
    order = LabQualTestOrder.query.get(order_id)
    if not order:
        flash('Order no longer exists.', 'danger')
        return redirect(request.referrer)

    record_set = LabQualTestRecordSet.query.filter_by(order_id=order_id).first()
    if not record_set:
        record_set = LabQualTestRecordSet(order_id=order_id)
        flash('New result record set has been created for the order.', 'success')
        db.session.add(record_set)
        db.session.commit()

    form = LabQualTestRecordForm()
    if order.test.choice_set:
        choices = [(c.result, c.result) for c in order.test.choice_set.choice_items]
    else:
        choices = []
    form.result_choices.choices = choices
    if request.method == 'POST':
        if form.validate_on_submit():
            new_record = LabQualTestRecord()
            form.populate_obj(new_record)
            new_record.record_set = record_set
            new_record.updated_at = arrow.now('Asia/Bangkok').datetime
            new_record.updator = current_user
            if not new_record.text_result and choices:
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
            order.finished_at = arrow.now('Asia/Bangkok').datetime
            db.session.add(order)
            db.session.commit()
            flash('New result record has been saved.', 'success')
            return redirect(url_for('lab.list_pending_orders', lab_id=lab_id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/new_qual_test_record.html', form=form, order=order)


@lab.route('/customers/<int:customer_id>/quan/recordsets/<int:recordset_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_quan_record(customer_id, recordset_id):
    recordset = LabQuanTestRecordSet.query.get(recordset_id)
    def edit_quan_form_factory(choice_set_id, choice_item):
        class EditQuanForm(LabQuanTestRecordForm):
            choice = QuerySelectField('Choices',
                            query_factory=lambda:
                                LabResultChoiceItem.query.filter_by(choice_set_id=choice_set_id),
                            default=choice_item,
                            widget=Select(), validators=[Optional()])
        return EditQuanForm

    cur_record = sorted(recordset.records, key=lambda x: x.updated_at, reverse=True)[0]
    choice_set_id = recordset.order.test.choice_set_id
    choice_item = None
    if choice_set_id:
        for item in recordset.order.test.choice_set.choice_items:
            if item.result == cur_record.text_result:
                choice_item = item

        EditQuanForm = edit_quan_form_factory(choice_set_id, choice_item)
        form = EditQuanForm(obj=cur_record)
    else:
        form = LabQuanTestRecordForm(obj=cur_record)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_record = LabQuanTestRecord()
            form.populate_obj(new_record)
            new_record.updated_at = arrow.now('Asia/Bangkok').datetime
            new_record.updator = current_user
            new_record.record_set = recordset
            cur_record.cancelled = True
            if hasattr(form, 'choice'):
                new_record.text_result = form.choice.data.result
            activity = LabActivity(
                lab_id=recordset.order.lab.id,
                actor=current_user,
                message='Edited the result for a test order.',
                detail=new_record.id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(cur_record)
            db.session.add(new_record)
            db.session.add(activity)
            db.session.commit()
            flash('New result record has been saved.', 'success')
            return redirect(url_for('lab.show_customer_quan_recordset',
                                    customer_id=customer_id,
                                    recordset_id=recordset.id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/edit_quan_test_record.html', form=form, recordset=recordset)


@lab.route('/customers/<int:customer_id>/qual/recordsets/<int:recordset_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_qual_record(customer_id, recordset_id):
    recordset = LabQualTestRecordSet.query.get(recordset_id)
    choice_set_id = recordset.order.test.choice_set_id
    cur_record = sorted(recordset.records, key=lambda x: x.updated_at, reverse=True)[0]

    def edit_qual_form_factory(choice_set_id, choice_item):
        class EditQualForm(LabQualTestRecordForm):
            choice = QuerySelectField('Choices',
                            query_factory=lambda:
                                LabResultChoiceItem.query.filter_by(choice_set_id=choice_set_id),
                            default=choice_item,
                            widget=Select(), validators=[Optional()])
        return EditQualForm

    choice_item = None
    if choice_set_id:
        for item in recordset.order.test.choice_set.choice_items:
            if item.result == cur_record.text_result:
                choice_item = item
                break
        EditQualForm = edit_qual_form_factory(choice_set_id, choice_item)
        form = EditQualForm(obj=cur_record)
    else:
        form = LabQualTestRecordForm(obj=cur_record)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_record = LabQualTestRecord()
            form.populate_obj(new_record)
            new_record.updated_at = arrow.now('Asia/Bangkok').datetime
            new_record.updator = current_user
            new_record.record_set = recordset
            cur_record.cancelled = True
            if hasattr(form, 'choice'):
                new_record.text_result = form.choice.data.result
            activity = LabActivity(
                lab_id=recordset.order.lab.id,
                actor=current_user,
                message='Edited the result for a test order.',
                detail=new_record.id,
                added_at=arrow.now('Asia/Bangkok').datetime
            )
            db.session.add(cur_record)
            db.session.add(new_record)
            db.session.add(activity)
            db.session.commit()
            flash('New result record has been saved.', 'success')
            return redirect(url_for('lab.show_customer_qual_recordset',
                                    customer_id=customer_id,
                                    recordset_id=recordset.id))
        else:
            flash(form.errors, 'danger')
    return render_template('lab/edit_qual_test_record.html', form=form,
                           recordset=recordset, cur_record=cur_record)
