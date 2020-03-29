from app import create_app, db, admin
from dotenv import load_dotenv
from flask_admin.contrib.sqla import ModelView
import arrow


load_dotenv()

app = create_app()

from app.auth.models import *
admin.add_view(ModelView(User, db.session, category='Users'))

from app.main.models import *
admin.add_view(ModelView(Laboratory, db.session, category='Labs'))

from app.lab.models import *
admin.add_view(ModelView(LabQuanTest, db.session, category='Tests'))
admin.add_view(ModelView(LabQuanTestRecordSet, db.session, category='Tests'))
admin.add_view(ModelView(LabQuanTestRecord, db.session, category='Tests'))
admin.add_view(ModelView(LabResultChoiceSet, db.session, category='Tests'))
admin.add_view(ModelView(LabResultChoiceItem, db.session, category='Tests'))
admin.add_view(ModelView(LabActivity, db.session, category='Activities'))
admin.add_view(ModelView(LabCustomer, db.session, category='Customers'))


@app.template_filter('humanizedt')
def humanize_datetime(dt):
    dt = arrow.get(dt)
    return dt.humanize()
