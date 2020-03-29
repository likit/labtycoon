from flask import render_template, url_for
from . import main_blueprint as main
from app.main.models import Laboratory


@main.route('/')
def index():
    labs = Laboratory.query.all()
    return render_template('main/index.html', labs=labs)