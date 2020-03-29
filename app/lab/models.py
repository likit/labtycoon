from app import db
from app.main.models import Laboratory
from app.auth.models import User


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

    def __str__(self):
        return self.name


class LabResultChoiceItem(db.Model):
    __tablename__ = 'lab_result_choice_item'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    result = db.Column('result', db.String(), nullable=False)
    choice_set_id = db.Column('choices_id', db.ForeignKey('lab_result_choice_set.id'))
    choice_set = db.relationship(LabResultChoiceSet, backref=db.backref('choice_items'))
    interpretation = db.Column('interpretation', db.String())
    ref = db.Column('ref', db.Boolean(), default=False)

    def __str__(self):
        return self.result


class LabQuanTest(db.Model):
    __tablename__ = 'lab_quan_tests'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False)
    detail = db.Column('detail', db.Text())
    # for numeric results
    min_value = db.Column('min_value', db.Numeric(), default=0.0)
    max_value = db.Column('max_value', db.Numeric())
    min_ref_value = db.Column('min_ref_value', db.Numeric())
    max_ref_value = db.Column('max_ref_value', db.Numeric())
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
    test_id = db.Column('test_id', db.ForeignKey('lab_quan_tests.id'))
    test = db.relationship(LabQuanTest, backref=db.backref('result_record_sets'))


class LabQuanTestRecord(db.Model):
    __tablename__ = 'lab_quan_result_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    record_set_id = db.Column('record_set_id', db.ForeignKey('lab_quan_result_sets.id'))
    record_set = db.relationship(LabQuanTestRecordSet, backref=db.backref('records'))
    num_result = db.Column('num_result', db.Numeric())
    text_result = db.Column('text_result', db.String())
    comment = db.Column('comment', db.Text())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    cancelled = db.Column('cancelled', db.Boolean(), default=False)
    updated_by = db.Column('updator_id', db.ForeignKey('user.id'))
    updator = db.relationship(User, backref=db.backref('updated_result_records'))

