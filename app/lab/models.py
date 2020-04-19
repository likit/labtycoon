from app import db
from app.main.models import Laboratory
from app.auth.models import User


class LabCustomer(db.Model):
    __tablename__ = 'lab_customers'
    # id is used as an HN
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(), info={'label': 'Title',
                                                  'choices': [(t,t) for t in ['นาย',
                                                                              'นาง',
                                                                              'นางสาว',
                                                                              'เด็กหญิง',
                                                                              'เด็กชาย',
                                                                              'พระภิกษุ',
                                                                              'สามเณร']]})
    firstname = db.Column('firstname', db.String(), info={'label': 'First Name'})
    lastname = db.Column('lastname', db.String(), info={'label': 'Last Name'})
    dob = db.Column('dob', db.Date(), info={'label': 'Date of Birth'})
    gender = db.Column('gender', db.String(), info={'label': 'Gender',
                                                    'choices': [(g, g) for g in ['ชาย', 'หญิง']]})
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('customers'))

    @property
    def fullname(self):
        return '{}{} {}'.format(self.title, self.firstname, self.lastname)

    def __str__(self):
        return self.fullname

    @property
    def pending_qual_test_orders(self):
        return [order for order in self.qual_test_orders if not order.finished_at and not order.cancelled_at]

    @property
    def pending_quan_test_orders(self):
        return [order for order in self.quan_test_orders if not order.finished_at and not order.cancelled_at]


class LabActivity(db.Model):
    __tablename__ = 'lab_activities'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    actor_id = db.Column('actor_id', db.ForeignKey('user.id'))
    actor = db.relationship(User, backref=db.backref('activities'))
    message = db.Column('message', db.String(), nullable=False)
    detail = db.Column('detail', db.String())
    added_at = db.Column('added_at', db.DateTime(timezone=True))
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('member_activities'))


class LabResultChoiceSet(db.Model):
    __tablename__ = 'lab_result_choice_set'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String())
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('choice_sets'))
    reference = db.Column('reference', db.String())

    def __str__(self):
        return self.name


class LabResultChoiceItem(db.Model):
    __tablename__ = 'lab_result_choice_item'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    result = db.Column('result', db.String(), nullable=False)
    choice_set_id = db.Column('choices_id', db.ForeignKey('lab_result_choice_set.id'))
    choice_set = db.relationship(LabResultChoiceSet,
                                 backref=db.backref('choice_items',
                                                    cascade='all, delete-orphan'))
    interpretation = db.Column('interpretation', db.String())
    ref = db.Column('ref', db.Boolean(), default=False)

    def __str__(self):
        return self.result


class LabQuanTest(db.Model):
    __tablename__ = 'lab_quan_tests'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': 'Name'})
    detail = db.Column('detail', db.Text(), info={'label': 'Detail'})
    # for numeric results
    min_value = db.Column('min_value', db.Numeric(), default=0.0, info={'label': 'Min value'})
    max_value = db.Column('max_value', db.Numeric(), info={'label': 'Max value'})
    min_ref_value = db.Column('min_ref_value', db.Numeric(), info={'label': 'Min ref value'})
    max_ref_value = db.Column('max_ref_value', db.Numeric(), info={'label': 'Max ref value'})
    # choices for results in text
    choice_set_id = db.Column('choice_set', db.ForeignKey('lab_result_choice_set.id'))
    choice_set = db.relationship(LabResultChoiceSet)
    active = db.Column('active', db.Boolean(), default=True)
    added_at = db.Column('added_at', db.DateTime(timezone=True))
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('quant_tests'))

    def __str__(self):
        return self.name


class LabQuanTestRecordSet(db.Model):
    __tablename__ = 'lab_quan_result_sets'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column('order_id', db.ForeignKey('lab_quan_test_orders.id'))
    order = db.relationship('LabQuanTestOrder',
                                backref=db.backref('result_record_set',
                                                    uselist=False,
                                                    cascade='all, delete-orphan'))


class LabQuanTestRecord(db.Model):
    __tablename__ = 'lab_quan_result_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    record_set_id = db.Column('record_set_id', db.ForeignKey('lab_quan_result_sets.id'))
    record_set = db.relationship(LabQuanTestRecordSet,
                        backref=db.backref('records', cascade='all, delete-orphan'))
    num_result = db.Column('num_result', db.Numeric(),
                           info={'label': 'Numeric Result'})
    text_result = db.Column('text_result', db.String())
    comment = db.Column('comment', db.Text(),
                        info={'label': 'Comment'})
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    cancelled = db.Column('cancelled', db.Boolean(), default=False)
    updator_id = db.Column('updator_id', db.ForeignKey('user.id'))
    updator = db.relationship(User, backref=db.backref('updated_quan_result_records'))


class LabQuanTestOrder(db.Model):
    __tablename__ = 'lab_quan_test_orders'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('quan_test_orders'))
    customer_id = db.Column('customer_id', db.ForeignKey('lab_customers.id'))
    customer = db.relationship(LabCustomer, backref=db.backref('quan_test_orders'))
    test_id = db.Column('test_id', db.ForeignKey('lab_quan_tests.id'))
    test = db.relationship(LabQuanTest, backref=db.backref('orders', cascade='all, delete-orphan'))
    ordered_at = db.Column('ordered_at', db.DateTime(timezone=True))
    ordered_by_id = db.Column('ordered_by_id', db.ForeignKey('user.id'))
    ordered_by = db.relationship(User,
                                 backref=db.backref('quan_test_orders'),
                                 foreign_keys=[ordered_by_id])
    cancelled_at = db.Column('cancelled_at', db.DateTime(timezone=True))
    reject_record_id = db.Column('reject_record_id', db.ForeignKey('lab_order_reject_records.id'))
    reject_record = db.relationship('LabOrderRejectRecord', backref=db.backref('quan_orders'))
    received_at = db.Column('received_at', db.DateTime(timezone=True))
    finished_at = db.Column('finished_at', db.DateTime(timezone=True))
    receiver_id = db.Column('receiver_id', db.ForeignKey('user.id'))
    receiver = db.relationship(User,
                               backref=db.backref('received_quan_orders'),
                               foreign_keys=[receiver_id])


class LabQualTest(db.Model):
    __tablename__ = 'lab_qual_tests'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': 'Name'})
    detail = db.Column('detail', db.Text(), info={'label': 'Detail'})
    # choices for results in text
    choice_set_id = db.Column('choice_set', db.ForeignKey('lab_result_choice_set.id'))
    choice_set = db.relationship(LabResultChoiceSet)
    active = db.Column('active', db.Boolean(), default=True)
    added_at = db.Column('added_at', db.DateTime(timezone=True))
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('qual_tests'))

    def __str__(self):
        return self.name


class LabQualTestOrder(db.Model):
    __tablename__ = 'lab_qual_test_orders'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    lab_id = db.Column('lab_id', db.ForeignKey('labs.id'))
    lab = db.relationship(Laboratory, backref=db.backref('qual_test_orders'))
    customer_id = db.Column('customer_id', db.ForeignKey('lab_customers.id'))
    customer = db.relationship(LabCustomer, backref=db.backref('qual_test_orders'))
    test_id = db.Column('test_id', db.ForeignKey('lab_qual_tests.id'))
    test = db.relationship(LabQualTest, backref=db.backref('orders', cascade='all, delete-orphan'))
    ordered_at = db.Column('ordered_at', db.DateTime(timezone=True))
    ordered_by_id = db.Column('ordered_by_id', db.ForeignKey('user.id'))
    ordered_by = db.relationship(User,
                                 backref=db.backref('qual_test_orders'),
                                 foreign_keys=[ordered_by_id])
    cancelled_at = db.Column('cancelled_at', db.DateTime(timezone=True))
    reject_record_id = db.Column('reject_record_id', db.ForeignKey('lab_order_reject_records.id'))
    reject_record = db.relationship('LabOrderRejectRecord', backref=db.backref('qual_orders'))
    received_at = db.Column('received_at', db.DateTime(timezone=True))
    finished_at = db.Column('finished_at', db.DateTime(timezone=True))
    receiver_id = db.Column('receiver_id', db.ForeignKey('user.id'))
    receiver = db.relationship(User,
                               backref=db.backref('received_qual_orders'),
                               foreign_keys=[receiver_id])


class LabQualTestRecordSet(db.Model):
    __tablename__ = 'lab_qual_result_sets'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column('order_id', db.ForeignKey('lab_qual_test_orders.id'))
    order = db.relationship(LabQualTestOrder,
                    backref=db.backref('result_record_set',
                                    uselist=False,
                                    cascade='all, delete-orphan'))


class LabQualTestRecord(db.Model):
    __tablename__ = 'lab_qual_result_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    record_set_id = db.Column('record_set_id', db.ForeignKey('lab_qual_result_sets.id'))
    record_set = db.relationship(LabQualTestRecordSet,
                                    backref=db.backref('records', cascade='all, delete-orphan'))
    text_result = db.Column('text_result', db.String())
    comment = db.Column('comment', db.Text(),
                        info={'label': 'Comment'})
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    cancelled = db.Column('cancelled', db.Boolean(), default=False)
    updator_id = db.Column('updator_id', db.ForeignKey('user.id'))
    updator = db.relationship(User, backref=db.backref('updated_qual_result_records'))


class LabOrderRejectRecord(db.Model):
    __tablename__ = 'lab_order_reject_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime(timezone=True), nullable=False)
    creator_id = db.Column('creator_id', db.ForeignKey('user.id'))
    reason = db.Column('reason', db.String(), nullable=False, info={'label': 'สาเหตุ',
                        'choices': [(c, c) for c in ['สิ่งส่งตรวจไม่เหมาะสมกับการทดสอบ',
                                                        'สิ่งส่งตรวจไม่เพียงพอ',
                                                        'คุณภาพของสิ่งส่งตรวจไม่ดี',
                                                        'ภาชนะรั่วหรือแตก',
                                                        'ไม่มีรายการตรวจ',
                                                        'ข้อมูลคนไข้ไม่ตรงกัน', 'อื่นๆ']
                                                        ]
                                                    })
    detail = db.Column('detail', db.Text(), info={'label': 'รายละเอียด โปรดระบุ'})