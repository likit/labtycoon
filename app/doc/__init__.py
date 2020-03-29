from flask import Blueprint

doc_blueprint = Blueprint('doc', __name__)

from . import views