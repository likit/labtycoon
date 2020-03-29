from flask import Blueprint

lab_blueprint = Blueprint('lab', __name__)

from . import views