from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, StringField, TextField, DecimalField, SelectField
from wtforms.fields import BooleanField
from wtforms.widgets import Select
from wtforms.validators import InputRequired, Optional
from wtforms_alchemy import model_form_factory, QuerySelectField
from wtforms_alchemy.fields import QuerySelectField

from .models import *
from app import db

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ChoiceSetForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired()
    ])
    reference = StringField('Reference')


class ChoiceItemForm(FlaskForm):
    result = StringField('Result', validators=[
        InputRequired()
    ])
    interpretation = StringField('Interpretation', validators=[
        InputRequired()
    ])
    ref = BooleanField('Is this a reference value?')


class LabQuanTestForm(ModelForm):
    class Meta:
        model = LabQuanTest
    choice_set = QuerySelectField('Choice Set',
                                  widget=Select(),
                                  allow_blank=True,
                                  blank_text='เลือกชุดคำตอบ',
                                  validators=[Optional()]
                                 )


class LabQualTestForm(ModelForm):
    class Meta:
        model = LabQualTest
    choice_set = QuerySelectField('Choice Set',
                                  widget=Select(),
                                  allow_blank=True,
                                  blank_text='เลือกชุดคำตอบ',
                                  validators=[Optional()]
                                 )


class LabCustomerForm(ModelForm):
    class Meta:
        model = LabCustomer


class LabQuanTestRecordForm(ModelForm):
    class Meta:
        model = LabQuanTestRecord
    choice = QuerySelectField('Result choices',
                                  widget=Select(),
                                  allow_blank=False,
                                  validators=[Optional()]
                                 )


class LabQualTestRecordForm(ModelForm):
    class Meta:
        model = LabQualTestRecord
    choice = QuerySelectField('Result choices',
                                  widget=Select(),
                                  allow_blank=False,
                                  validators=[Optional()]
                                 )