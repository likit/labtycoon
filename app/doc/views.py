from flask import render_template, url_for
from . import doc_blueprint as doc


@doc.route('/intro')
def intro():
    return render_template('doc/intro.html')


@doc.route('/components')
def components():
    return render_template('doc/components.html')


@doc.route('/data_management')
def data_management():
    return render_template('doc/data-management.html')
