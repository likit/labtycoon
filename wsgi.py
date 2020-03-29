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


@app.template_filter('humanizedt')
def humanize_datetime(dt):
    dt = arrow.get(dt)
    return dt.humanize()
