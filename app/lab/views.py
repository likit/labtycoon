from . import lab_blueprint as lab
from flask import render_template, url_for
from app.main.models import Laboratory


@lab.route('/<int:lab_id>')
def landing(lab_id):
    lab = Laboratory.query.get(lab_id)
    return render_template('lab/index.html', lab=lab)
