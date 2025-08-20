from pytz import timezone
from wtforms import PasswordField
from wtforms.validators import Optional, EqualTo, ValidationError

from app import create_app, db, admin
from dotenv import load_dotenv
from flask import render_template, flash
from flask_admin.contrib.sqla import ModelView
import arrow

load_dotenv()

app = create_app()


class UserModelView(ModelView):
    column_searchable_list = ['email']
    form_excluded_columns = ['pwdhash']

    form_extra_fields = {
        'new_password': PasswordField(
            'New password',
            render_kw={'autocomplete': 'new-password'}
        ),
        'confirm_password': PasswordField(
            'Confirm password',
            validators=[EqualTo('new_password', message='Passwords must match')],
            render_kw={'autocomplete': 'new-password'}
        ),
    }

    def on_model_change(self, form, model, is_created):
        pwd = form.new_password.data
        if is_created and not pwd:
            # Require a password when creating a new user
            raise ValidationError('Password is required for new users.')
        if pwd:
            model.password = pwd  # hashes & stores into password_hash
            flash('Password updated.', 'success')
        return super().on_model_change(form, model, is_created)


from app.auth.models import *

admin.add_view(UserModelView(User, db.session, category='Users'))

from app.main.models import *

admin.add_view(ModelView(Laboratory, db.session, category='Labs'))

from app.lab.models import *

admin.add_view(ModelView(LabTest, db.session, category='Tests'))
admin.add_view(ModelView(LabTestOrder, db.session, category='Tests'))
admin.add_view(ModelView(LabTestRecord, db.session, category='Tests'))
admin.add_view(ModelView(LabResultChoiceSet, db.session, category='Tests'))
admin.add_view(ModelView(LabResultChoiceItem, db.session, category='Tests'))
admin.add_view(ModelView(LabActivity, db.session, category='Activities'))
admin.add_view(ModelView(LabCustomer, db.session, category='Customers'))
admin.add_view(ModelView(Announcement, db.session, category='Announcement'))
admin.add_view(ModelView(UserLabAffil, db.session, category='Labs'))


@app.route('/')
def index():
    announcements = Announcement.query.all()
    return render_template('index.html', announcements=announcements)


@app.template_filter('humanizedt')
def humanize_datetime(dt):
    if dt:
        dt = arrow.get(dt)
        return dt.humanize()
    else:
        return ''


@app.template_filter("localdatetime")
def local_datetime(dt):
    bangkok = timezone('Asia/Bangkok')
    datetime_format = '%d/%m/%Y %X'
    if dt:
        if dt.tzinfo:
            return dt.astimezone(bangkok).strftime(datetime_format)
    else:
        return None
