from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, StringField, TextField, DecimalField, SelectField
from wtforms.fields import BooleanField
from wtforms.widgets import Select
from wtforms.validators import InputRequired, Optional
from wtforms_alchemy import model_form_factory, QuerySelectField
from wtforms_alchemy.fields import QuerySelectField

from .models import LabQuanTest, LabResultChoiceSet
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


class LabQuanTestForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired()
    ])
    detail = TextField('Detail')
    min_value = DecimalField('Min Value', default=0.0)
    max_value = DecimalField('Max Value', validators=[Optional()])
    min_ref_value = DecimalField('Min Reference Value', validators=[Optional()])
    max_ref_value = DecimalField('Max Reference Value', validators=[Optional()])
    choice_sets = SelectField('Choice Sets', coerce=int)
    active = BooleanField('Active', default='checked')


