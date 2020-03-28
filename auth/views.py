from . import auth_blueprint as auth


@auth.route('/')
def index():
    return 'auth index.'