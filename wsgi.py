from app import create_app, db, admin
from dotenv import load_dotenv
from flask_admin.contrib.sqla import ModelView


load_dotenv()

app = create_app()

from app.auth.models import *
admin.add_view(ModelView(User, db.session, category='Users'))
